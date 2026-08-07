import unittest
import pytest
from selenium.webdriver.common.by import By
from pages import AdminLoginPage, RegisterPage


class PrestaShopAuthTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_class_fixtures(self, browser, base_url):
        self.driver = browser
        self.base_url = base_url

    @pytest.mark.order(6)
    def test_06_admin_login_logout(self):
        """Тест проверяет вход и выход админа"""
        admin_page = AdminLoginPage(self.driver, self.base_url)
        admin_page.open()

        admin_page.login_as_admin()

        avatar = admin_page.get_admin_profile_img()
        self.assertTrue(avatar.is_displayed(), "Вход в админку не зафиксирован")
        avatar.click()

        admin_page.logout()

        self.assertTrue(admin_page.wait_for_element(admin_page.LOGIN_BOX).is_displayed(),
                        "Форма логина не появилась после выхода")

    @pytest.mark.order(12)
    def test_12_customer_registration(self):
        """Тест успешной регистрации нового клиента в магазине"""
        register_page = RegisterPage(self.driver, self.base_url)

        register_page.open()

        import random
        random_id = random.randint(1000, 9999)
        first_name = "Тестовый"
        last_name = f"Тест"
        user_email = f"test_{random_id}@example.com"
        user_password = "SecurePassword123!"

        register_page.register_new_user(first_name, last_name, user_email, user_password)


        user_profile_link = (By.XPATH,
                             f"//a[contains(@class, 'account')]//*[contains(text(), '{first_name}')] | //a[contains(@class, 'account') and contains(., '{first_name}')]")

        self.assertTrue(register_page.wait_for_element(user_profile_link).is_displayed(),
                        f"Регистрация не удалась, имя пользователя '{first_name}' не появилось в шапке сайта")
