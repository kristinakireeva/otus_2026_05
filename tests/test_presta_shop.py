import unittest

import pytest

from pages import AdminLoginPage, CatalogPage, MainPage, ProductPage, RegisterPage
from selenium import webdriver


class PrestaShopPresenceTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_class_fixtures(self, browser, base_url):
        self.driver = browser
        self.base_url = base_url


    def test_01_main_page_elements(self):
        page = MainPage(self.driver, self.base_url)
        self.driver.get(page.base_url + page.URL)
        self.assertTrue(page.wait_for_element(*page.LOGO))
        self.assertTrue(page.wait_for_element(*page.SEARCH_INPUT))
        self.assertTrue(page.wait_for_element(*page.CART_BUTTON))
        self.assertTrue(page.wait_for_element(*page.SLIDER))
        self.assertTrue(page.wait_for_element(*page.CONTACT_LINK))

    def test_02_catalog_page_elements(self):
        page = CatalogPage(self.driver)
        self.driver.get(page.base_url + page.URL)
        self.assertTrue(page.wait_for_element(*page.BREADCRUMBS))
        self.assertTrue(page.wait_for_element(*page.PRODUCTS_GRID))
        self.assertTrue(page.wait_for_element(*page.SORT_DROPDOWN))
        self.assertTrue(page.wait_for_element(*page.FILTER_BLOCK))
        self.assertTrue(page.wait_for_element(*page.CATEGORY_TITLE))

    def test_03_product_page_elements(self):
        page = ProductPage(self.driver)
        self.driver.get(page.base_url + page.URL)
        self.assertTrue(page.wait_for_element(*page.PRODUCT_NAME))
        self.assertTrue(page.wait_for_element(*page.ADD_TO_CART_BTN))
        self.assertTrue(page.wait_for_element(*page.PRODUCT_PRICE))
        self.assertTrue(page.wait_for_element(*page.PRODUCT_COVER))
        self.assertTrue(page.wait_for_element(*page.QUANTITY_INPUT))

    def test_04_admin_login_elements(self):
        page = AdminLoginPage(self.driver)
        self.driver.get(page.base_url + page.URL)
        self.assertTrue(page.wait_for_element(*page.LOGIN_BOX))
        self.assertTrue(page.wait_for_element(*page.EMAIL_INPUT))
        self.assertTrue(page.wait_for_element(*page.PASSWORD_INPUT))
        self.assertTrue(page.wait_for_element(*page.SUBMIT_BTN))
        self.assertTrue(page.wait_for_element(*page.FORGOT_PASSWORD))

    def test_05_registration_page_elements(self):
        page = RegisterPage(self.driver)
        self.driver.get(page.base_url + page.URL)
        self.assertTrue(page.wait_for_element(*page.GENDER_RADIO))
        self.assertTrue(page.wait_for_element(*page.FIRSTNAME_INPUT))
        self.assertTrue(page.wait_for_element(*page.LASTNAME_INPUT))
        self.assertTrue(page.wait_for_element(*page.EMAIL_INPUT))
        self.assertTrue(page.wait_for_element(*page.SAVE_BUTTON))

    def test_06_admin_login_logout(self):
        page = AdminLoginPage(self.driver)
        self.driver.get(page.base_url + page.URL)

        page.wait_for_element(*page.EMAIL_INPUT).send_keys("admin@otus.ru")
        page.wait_for_element(*page.PASSWORD_INPUT).send_keys("OtusPassword2026!")
        page.wait_for_element(*page.SUBMIT_BTN).click()
        avatar = page.wait_for_clickable(*page.ADMIN_PROFILE_IMG)
        self.assertTrue(avatar.is_displayed(), "Вход в админку не зафиксирован")
        avatar.click()
        logout = page.wait_for_clickable(*page.LOGOUT_LINK)
        logout.click()

        self.assertTrue(page.wait_for_element(*page.LOGIN_BOX).is_displayed())

    def test_07_add_to_cart_random_product(self):
        main_page = MainPage(self.driver)
        product_page = ProductPage(self.driver)

        self.driver.get(main_page.base_url + main_page.URL)
        main_page.wait_for_element(*main_page.RANDOM_PRODUCT_LINK).click()
        product_page.wait_for_element(*product_page.ADD_TO_CART_BTN).click()
        modal_title = product_page.wait_for_element(*product_page.CART_MODAL_CHECK)
        self.assertIn("Товар добавлен в корзину", modal_title.text)

    def test_08_currency_change_main_page(self):
        page = MainPage(self.driver)
        self.driver.get(page.base_url + page.URL)

        initial_prices = page.wait_for_elements(*page.PRODUCT_PRICES)
        old_price_text = initial_prices[0].text
        page.wait_for_element(*page.CURRENCY_DROP_DOWN).click()
        usd_option = page.wait_for_clickable(*page.ANY_CURRENCY_OPTION)
        usd_option.click()

        updated_prices = page.wait_for_elements(*page.PRODUCT_PRICES)
        self.assertNotEqual(old_price_text, updated_prices[0].text)

    def test_09_currency_change_catalog_page(self):
        page = CatalogPage(self.driver)
        self.driver.get(page.base_url + page.URL)

        initial_prices = page.wait_for_elements(*page.CATALOG_PRODUCT_PRICES)
        old_price_text = initial_prices[0].text
        page.wait_for_element(*page.CURRENCY_DROP_DOWN).click()
        usd_option = page.wait_for_clickable(*page.ANY_CURRENCY_OPTION)
        usd_option.click()

        updated_prices = page.wait_for_elements(*page.CATALOG_PRODUCT_PRICES)
        self.assertNotEqual(old_price_text, updated_prices[0].text)


if __name__ == "__main__":
    unittest.main()
