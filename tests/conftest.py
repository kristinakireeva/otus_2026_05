import os
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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

    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        # Запуск Chrome на весь экран
        options.add_argument("--start-maximized")
        driver_instance = webdriver.Chrome(options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        # Настройка разрешения для Firefox
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver_instance = webdriver.Firefox(options=options)
        driver_instance.maximize_window()

    elif browser_name == 'safari':
        # Safari запустится только на macOS
        driver_instance = webdriver.Safari()
        driver_instance.maximize_window()

    else:
        raise ValueError(
            f"Браузер '{browser_name}' не поддерживается! "
            f"Используйте: chrome, firefox или safari"
        )

    yield driver_instance

    if driver_instance is not None:
        driver_instance.quit()
