import allure
import logging

from pyexpat.errors import messages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class BasePage:
    def __init__(self, driver, base_url="http://localhost:8081"):
        self.driver = driver
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Инициализирован класс страницы {self.__class__.__name__}")

    def open(self):
        base = self.base_url.rstrip('/')
        relative = self.URL.lstrip('/')
        full_url = f"{base}/{relative}"

        message = f"открытие страницы по URL: {full_url}"
        self.logger.info(message)

        with allure.step(f"Открытие страницы по относительному пути: {self.URL}"):
            self.driver.get(full_url)

    def wait_for_element(self, locator, timeout=10):
        self.logger.debug(f"жидание присутствия элемента {locator} (timeout={timeout}s)")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=15):
        self.logger.debug(f"Ожидание кликабельности элемента {locator} (timeout={timeout}s)")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_elements(self, locator, timeout=10):
        self.logger.debug(f"жидание спсика элементов {locator} (timeout={timeout}s)")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click_element(self, locator):
        """Ожидает кликабельности элемента и кликает по нему"""
        self.logger.info(f"Клик по элементу с локатором {locator}")
        self.wait_for_clickable(locator).click()

    def enter_text(self, locator, text):
        """Ожидает элемент, очищает поле через горячие клавиши и вводит текст"""
        log_text = "*********" if "password" in str(locator).lower() else text
        self.logger.info(f"Ввод текста {log_text} в элемент {locator}")

        element = self.wait_for_element(locator)
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(text)

    def get_element_text(self, locator):
        """Ожидает появление элемента и возвращает его текст"""
        text = self.wait_for_element(locator).text
        self.logger.info(f"Получен текст {text} из элемент {locator}")
        return self.wait_for_element(locator).text
