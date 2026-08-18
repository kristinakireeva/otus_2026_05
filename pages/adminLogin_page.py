import allure
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminLoginPage(BasePage):
    """Страница авторизации в панели администратора PrestaShop"""
    URL = "/administration/"

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "passwd")
    SUBMIT_BTN = (By.NAME, "submitLogin")
    ADMIN_PROFILE_IMG = (By.ID, "employee_infos")

    LOGOUT_LINK = (By.ID, "header_logout")
    LOGIN_BOX = (By.ID, "login_form")

    @allure.step("Ввод учетных данных для пользователя: {username}")
    def login_as_admin(self, username, password):
        self.logger.info(f"Авторизация в админке {username}")

        self.enter_text(self.EMAIL_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.SUBMIT_BTN)

    @allure.step("Проверка успешного входа и открытие меню профиля")
    def get_admin_profile_img(self):
        self.logger.info("Ожидание отображения и кликабельности иконки профиля админа")
        return self.wait_for_clickable(self.ADMIN_PROFILE_IMG)

    @allure.step("Выполнение выхода из системы (Log out)")
    def logout(self):
        self.click_element(self.ADMIN_PROFILE_IMG)
        self.click_element(self.LOGOUT_LINK)
