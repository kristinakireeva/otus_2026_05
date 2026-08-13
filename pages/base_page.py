import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, base_url="http://localhost:8081"):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        base = self.base_url.rstrip('/')
        relative = self.URL.lstrip('/')
        full_url = f"{base}/{relative}"

        with allure.step(f"Открытие страницы по относительному пути: {self.URL}"):
            self.driver.get(full_url)

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click_element(self, locator):
        """Ожидает кликабельности элемента и кликает по нему (Замечание 6)"""
        self.wait_for_clickable(locator).click()

    def enter_text(self, locator, text):
        """Ожидает элемент, очищает поле через горячие клавиши и вводит текст (Замечание 6)"""
        element = self.wait_for_element(locator)
        element.click()
        from selenium.webdriver.common.keys import Keys
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(text)

    def get_element_text(self, locator):
        """Ожидает появление элемента и возвращает его текст (Замечание 6)"""
        return self.wait_for_element(locator).text
