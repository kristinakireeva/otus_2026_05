import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Каталог"""
    URL = "/3-clothes"

    BREADCRUMBS = (By.XPATH, "//nav[@class='breadcrumb']")
    PRODUCTS_GRID = (By.XPATH, "//*[@id='js-product-list']")
    SORT_DROPDOWN = (By.XPATH, "//div[contains(@class, 'products-sort-order')]")
    FILTER_BLOCK = (By.XPATH, "//div[@id='search_filters']")
    CATEGORY_TITLE = (By.XPATH, "//h1[contains(@class, 'h1')]")
    CURRENCY_DROP_DOWN = (By.XPATH, "//div[@id='_desktop_currency_selector']//button")
    ANY_CURRENCY_OPTION = (By.XPATH,
                           "//ul[contains(@class, 'dropdown-menu')]//a[contains(text(), 'USD') or contains(text(), '$')]")
    CATALOG_PRODUCT_PRICES = (By.XPATH, "//div[@id='js-product-list']//span[@class='price']")

    @allure.step("Выбор валюты USD в раскрывающемся списке")
    def change_currency_to_usd(self):
        self.click_element(self.CURRENCY_DROP_DOWN)
        self.click_element(self.ANY_CURRENCY_OPTION)

    @allure.step("Получение обновленных цен товаров / старых цен товаров")
    def get_catalog_product_prices_text(self):
        self.logger.info("Сбор текстовых значений цен со всех товаров в каталоге")

        price_elements = self.wait_for_elements(self.CATALOG_PRODUCT_PRICES)
        prices = [element.text for element in price_elements]

        self.logger.info(f"Успешно собрано цен: {len(prices)}. Значения: {prices}")
        return prices
