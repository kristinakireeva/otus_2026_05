import pytest
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
def browser(request):
    browser_name = request.config.getoption("browser").lower()
    headless = request.config.getoption("headless")

    driver_instance = None

    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver_instance = webdriver.Chrome(options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver_instance = webdriver.Firefox(options=options)

    elif browser_name == 'safari':
        # Safari запустится только на macOS
        driver_instance = webdriver.Safari()

    else:
        raise ValueError(
            f"Браузер '{browser_name}' не поддерживается! "
            f"Используйте: chrome, firefox или safari"
        )

    yield driver_instance

    if driver_instance is not None:
        driver_instance.quit()
