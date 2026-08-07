import unittest
import pytest
import random

from pages import AdminLoginPage, AdminProductsPage


class PrestaShopAdminCatalogTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_class_fixtures(self, browser, base_url, admin_creds):
        self.driver = browser
        self.base_url = base_url
        self.admin_creds = admin_creds

    @pytest.mark.order(10)
    def test_10_add_new_product_by_admin(self):
        """Тест создания товара через админа с проверкой в списке"""
        admin_login_page = AdminLoginPage(self.driver, self.base_url)

        admin_login_page.open()
        admin_login_page.login_as_admin(
            username=self.admin_creds["email"],
            password=self.admin_creds["password"]
        )
        self.assertTrue(admin_login_page.get_admin_profile_img().is_displayed(),
                        "Вход в админку не зафиксирован")

        admin_products_page = AdminProductsPage(self.driver, self.base_url)
        admin_products_page.open_via_menu()


        admin_products_page.click_new_product()
        admin_products_page.click_confirm_add_product()

        product_name = f"Test T-Shirt {random.randint(1000, 9999)}"
        admin_products_page.create_simple_product(product_name)

        self.assertTrue(admin_products_page.is_creation_success_visible(),
                        "Уведомление 'Обновление завершено' не появилось")


        admin_products_page.go_back_to_products_list()

        self.assertTrue(admin_products_page.is_product_present_in_list(product_name),
                        f"Созданный товар '{product_name}' не найден в общем списке каталога")


    @pytest.mark.order(10)
    def test_11_delete_product_by_admin(self):
        """Тест создания товара через админа с проверкой в списке"""
        admin_login_page = AdminLoginPage(self.driver, self.base_url)

        admin_login_page.open()
        admin_login_page.login_as_admin(
            username=self.admin_creds["email"],
            password=self.admin_creds["password"]
        )
        self.assertTrue(admin_login_page.get_admin_profile_img().is_displayed(),
                        "Вход в админку не зафиксирован")

        admin_products_page = AdminProductsPage(self.driver, self.base_url)
        admin_products_page.open_via_menu()

        admin_products_page.click_first_product_actions()
        admin_products_page.click_delete_product()
        admin_products_page.confirm_product_deletion()

        self.assertTrue(admin_products_page.is_deletion_success_visible(),
                        "Уведомление 'Удаление завершено' не появилось")
