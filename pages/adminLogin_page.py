import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminLoginPage(BasePage):
    """Страница авторизации в панели администратора PrestaShop"""
    URL = "/administration/"

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "passwd")
    SUBMIT_BTN = (By.NAME, "submitLogin")
    ADMIN_PROFILE_IMG = (By.XPATH, "//li[@id='employee_infos']")

    LOGOUT_LINK = (By.ID, "header_logout")
    LOGIN_BOX = (By.ID, "login_form")

    def login_as_admin(self, username, password):
        email_field = self.wait_for_element(self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(username)

        pass_field = self.wait_for_element(self.PASSWORD_INPUT)
        pass_field.clear()
        pass_field.send_keys(password)

        self.wait_for_clickable(self.SUBMIT_BTN).click()
        time.sleep(1)

    def get_admin_profile_img(self):
        return self.wait_for_clickable(self.ADMIN_PROFILE_IMG)
