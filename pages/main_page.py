import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная"""
    URL = "/"

    LOGO = (By.XPATH, "//div[@id='_desktop_logo']")
    SEARCH_INPUT = (By.XPATH, "//input[@name='s']")
    CART_BUTTON = (By.XPATH, "//div[@id='_desktop_cart']")
    SLIDER = (By.XPATH, "//div[contains(@class, 'carousel')]")
    CONTACT_LINK = (By.XPATH, "//div[@id='contact-link']//a")
    RANDOM_PRODUCT_LINK = (By.XPATH,
                           "//div[@class='products']//article[contains(@class, 'product-miniature')]//a[@class='thumbnail product-thumbnail'] | //a[contains(@class, 'product-thumbnail')]")
    CURRENCY_DROP_DOWN = (By.XPATH, "//div[@id='_desktop_currency_selector']//button")
    ANY_CURRENCY_OPTION = (By.XPATH,
                           "//ul[contains(@class, 'dropdown-menu')]//a[contains(text(), 'USD') or contains(text(), '$')]")
    PRODUCT_PRICES = (By.XPATH, "//section[@class='featured-products clearfix']//span[@class='price']")

    @allure.step("Выбор случайного товара")
    def click_random_product(self):
        self.click_element(self.RANDOM_PRODUCT_LINK)

    @allure.step("Выбор валюты USD в раскрывающемся списке")
    def change_currency_to_usd(self):
        self.click_element(self.CURRENCY_DROP_DOWN)
        self.click_element(self.ANY_CURRENCY_OPTION)

    @allure.step("Получение обновленных цен товаров")
    def get_product_prices_text(self):
        self.logger.info("Сбор цен со всех продуктов на главной странице")
        price_elements = self.wait_for_elements(self.PRODUCT_PRICES)
        prices = [element.text for element in price_elements]
        self.logger.info(f"Успешно собрано цен: {len(prices)}")
        return prices
