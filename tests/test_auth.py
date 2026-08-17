import pytest
import allure
import random
from pages import AdminLoginPage, RegisterPage


@pytest.mark.order(6)
@allure.title("Авторизация и выход из учетной записи администратора")
def test_06_admin_login_logout(browser, base_url, admin_creds):
    admin_page = AdminLoginPage(browser, base_url)
    admin_page.open()
    # Обязательная передача аргументов (Замечание 1)
    admin_page.login_as_admin(username=admin_creds["email"], password=admin_creds["password"])

    avatar = admin_page.get_admin_profile_img()
    assert avatar.is_displayed(), "Вход в админку не зафиксирован"

    # Метод содержит исправленный клик по меню (Замечание 2)
    admin_page.logout()
    assert admin_page.wait_for_element(admin_page.LOGIN_BOX).is_displayed(), "Форма логина не появилась после выхода"


@pytest.mark.order(12)
@allure.title("Регистрация нового пользователя в магазине")
def test_12_customer_registration(browser, base_url):
    register_page = RegisterPage(browser, base_url)
    register_page.open()

    random_id = random.randint(1000, 9999)
    first_name = "Тестовый"
    last_name = "Тест"
    user_email = f"test_{random_id}@example.com"
    user_password = "SecurePassword123!"

    # Метод теперь выбирает пол внутри себя (Замечание 3)
    register_page.register_new_user(first_name, last_name, user_email, user_password)
    assert register_page.is_user_logged_in(first_name), f"Имя пользователя '{first_name}' не появилось в шапке"

