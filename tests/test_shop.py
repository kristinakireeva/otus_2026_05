import unittest
import pytest
from pages import MainPage, CatalogPage, ProductPage


class PrestaShopFeaturesTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_class_fixtures(self, browser, base_url):
        self.driver = browser
        self.base_url = base_url

    @pytest.mark.order(7)
    def test_07_add_to_cart_random_product(self):
        """Тест добавления в корзину случайного товара с главной страницы и проверка, что он появился в корзине"""
        main_page = MainPage(self.driver, self.base_url)
        product_page = ProductPage(self.driver, self.base_url)

        main_page.open()
        main_page.click_random_product()
        product_page.click_add_to_cart()

        modal_title = product_page.get_cart_modal_title()
        self.assertIn("Товар добавлен в корзину", modal_title.text)

    @pytest.mark.order(8)
    def test_08_currency_change_main_page(self):
        """Тест переключения валюты цены на товары на главной"""
        main_page = MainPage(self.driver, self.base_url)

        main_page.open()
        old_prices = main_page.get_product_prices_text()
        old_price_text = old_prices[0]

        main_page.change_currency_to_usd()

        new_prices = main_page.get_product_prices_text()
        self.assertNotEqual(old_price_text, new_prices[0], "Цена не изменилась после смены валюты!")

    @pytest.mark.order(9)
    def test_09_currency_change_catalog_page(self):
        """Тест переключения валюты цены на товары в каталоге"""
        catalog_page = CatalogPage(self.driver, self.base_url)

        catalog_page.open()
        old_prices = catalog_page.get_catalog_product_prices_text()
        old_price_text = old_prices[0]

        catalog_page.change_currency_to_usd()

        new_prices = catalog_page.get_catalog_product_prices_text()
        self.assertNotEqual(old_price_text, new_prices[0], "Цена в каталоге не изменилась после смены валюты!")
