import os
import pytest
import yaml
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pages.adminLogin_page import AdminLoginPage
from logging_config import setup_logging


@pytest.fixture(scope="session", autouse=True)
def init_logging():
    """Фикстура запускается один раз на всю сессию и настраивает формат логов"""
    setup_logging()


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Браузер для тестов: chrome, firefox, safari"
    )
    parser.addoption(
        "--browser_version",
        default="120.0",
        help="Версия браузера для запуска на удаленном сервере"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Запуск браузера без графического интерфейса (только для локального режима)"
    )
    parser.addoption(
        "--url",
        default="http://prestashop:80",
        help="Базовый URL сайта"
    )
    parser.addoption(
        "--executor",
        default="http://selenoid:4444/wd/hub",
        help="Адрес Selenoid"
    )




@pytest.fixture
def base_url(request):
    url = os.getenv("URL", request.config.getoption("url"))
    return url.rstrip('/')


@pytest.fixture
def admin_creds():
    """Читает переменные окружения PrestaShop напрямую из docker-compose.yaml"""
    compose_path = "docker-compose.yaml"

    if not os.path.exists(compose_path):
        compose_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker-compose.yaml")

    with open(compose_path, "r", encoding="utf-8") as f:
        compose_data = yaml.safe_load(f)

    env_vars = compose_data["services"]["prestashop"]["environment"]

    return {
        "email": env_vars["ADMIN_MAIL"],
        "password": env_vars["ADMIN_PASSWD"]
    }


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("browser").lower()
    browser_version = request.config.getoption("browser_version")
    headless = request.config.getoption("headless")

    # Сначала проверяем переменные из Jenkins (env), если их нет — берём флаг из терминала
    executor = os.getenv("EXECUTOR", request.config.getoption("executor"))

    driver_instance = None

    execution_mode = f"Selenoid ({executor})" if executor != "local" else "LOCAL"
    step_msg = f"Предусловие: Запуск браузера {browser_name.upper()} в режиме {execution_mode}"

    with allure.step(step_msg):
        # 1. Готовим опции для Chrome
        if browser_name == 'chrome':
            options = ChromeOptions()
            if headless and executor == "local":
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")

        # 2. Готовим опции для Firefox
        elif browser_name == 'firefox':
            options = FirefoxOptions()
            if headless and executor == "local":
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        # 3. Safari поддерживается только локально
        elif browser_name == 'safari':
            if executor != "local":
                raise ValueError("Safari не поддерживается для удаленного запуска на Selenoid!")
            options = None
        else:
            raise ValueError(
                f"Браузер '{browser_name}' не поддерживается! "
                f"Используйте: chrome, firefox или safari"
            )

        if executor == "local":
            if browser_name == 'chrome':
                driver_instance = webdriver.Chrome(options=options)
            elif browser_name == 'firefox':
                driver_instance = webdriver.Firefox(options=options)
                driver_instance.maximize_window()
            elif browser_name == 'safari':
                driver_instance = webdriver.Safari()
                driver_instance.maximize_window()
        else:
            selenoid_capabilities = {
                "browserName": browser_name,
                "browserVersion": browser_version,
                "selenoid:options": {
                    "enableVNC": True,
                    "enableVideo": False
                }
            }
            for key, value in selenoid_capabilities.items():
                options.set_capability(key, value)

            # Инициализируем удаленный веб-драйвер
            driver_instance = webdriver.Remote(
                command_executor=executor,
                options=options
            )

    if request.node is not None:
        request.node.driver = driver_instance

    yield driver_instance

    if driver_instance is not None:
        with allure.step(f"Постусловие: Закрытие сессии браузера {browser_name.upper()}"):
            driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для автоматического снятия скриншота при падении теста"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            web_driver = getattr(item, "driver", None)

            if web_driver:
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="Скриншот при падении теста",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот для Allure: {e}")


@pytest.fixture
def admin_session(browser, base_url, admin_creds):
    """Фикстура для автоматического создания авторизованной сессии админа"""
    admin_login_page = AdminLoginPage(browser, base_url)

    with allure.step("Предусловие: Авторизация в панели администратора"):
        admin_login_page.open()
        admin_login_page.login_as_admin(
            username=admin_creds["email"],
            password=admin_creds["password"]
        )
        assert admin_login_page.get_admin_profile_img().is_displayed(), "Не удалось войти в админку"

    return browser
