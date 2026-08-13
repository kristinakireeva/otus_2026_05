import os
import pytest
import yaml
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pages.adminLogin_page import AdminLoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Браузер для тестов: chrome, firefox, safari"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Запуск браузера без графического интерфейса"
    )
    parser.addoption(
        "--url",
        default="http://localhost:8081",
        help="Базовый URL сайта"
    )


@pytest.fixture
def base_url(request):
    url = request.config.getoption("url")
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
    headless = request.config.getoption("headless")

    driver_instance = None

    with allure.step(f"Предусловие: Запуск браузера {browser_name.upper()} (headless={headless})"):
        if browser_name == 'chrome':
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")  # Актуальный headless-режим для Chrome
            options.add_argument("--start-maximized")
            driver_instance = webdriver.Chrome(options=options)

        elif browser_name == 'firefox':
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            driver_instance = webdriver.Firefox(options=options)
            driver_instance.maximize_window()

        elif browser_name == 'safari':
            driver_instance = webdriver.Safari()
            driver_instance.maximize_window()

        else:
            raise ValueError(
                f"Браузер '{browser_name}' не поддерживается! "
                f"Используйте: chrome, firefox или safari"
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

    # Проверяем, что упал именно сам тест
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
    """Фикстура для автоматического создания авторизованной сессии админа (Замечание 7)"""
    admin_login_page = AdminLoginPage(browser, base_url)

    with allure.step("Предусловие: Авторизация в панели администратора"):
        admin_login_page.open()
        admin_login_page.login_as_admin(
            username=admin_creds["email"],
            password=admin_creds["password"]
        )
        assert admin_login_page.get_admin_profile_img().is_displayed(), "Не удалось войти в админку"

    return browser
