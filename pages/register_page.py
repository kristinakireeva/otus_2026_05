import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Страница регистрации нового пользователя в магазине PrestaShop"""
    URL = "/registration"

    FIRSTNAME_INPUT = (By.NAME, "firstname")
    LASTNAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")  # Фокус на этом поле (Замечание 3)

    GDPR_CHECKBOX = (By.XPATH, "//input[@name='psgdpr']")
    NEWSLETTER_CHECKBOX = (By.XPATH, "//input[@name='newsletter']")
    PRIVACY_CHECKBOX = (By.XPATH, "//input[@name='customer_privacy']")

    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'form-control-submit')]")

    @allure.step("Создание и заполнение формы нового пользователя")
    def register_new_user(self, firstname, lastname, email, password):
        self.logger.info(f"Начало регистрации пользователя: {firstname} {lastname} ({email})")

        self.enter_text(self.FIRSTNAME_INPUT, firstname)
        self.enter_text(self.LASTNAME_INPUT, lastname)
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)

        self.logger.info("Проставление обязательных чекбоксов")
        self.wait_for_element(self.GDPR_CHECKBOX).send_keys(Keys.SPACE)
        self.wait_for_element(self.NEWSLETTER_CHECKBOX).send_keys(Keys.SPACE)
        self.wait_for_element(self.PRIVACY_CHECKBOX).send_keys(Keys.SPACE)

        self.click_element(self.SAVE_BUTTON)
        return self

    @allure.step("Проверка автоматического входа")
    def is_user_logged_in(self, firstname):
        user_profile_locator = (By.XPATH,
                                f"//a[contains(@class, 'account')]//*[contains(text(), '{firstname}')] | "
                                f"//a[contains(@class, 'account') and contains(., '{firstname}')]"
                                )
        self.logger.info(f"Проверка: отображается ли профиль вошедшего пользователя для '{firstname}'")
        try:
            is_visible = self.wait_for_element(user_profile_locator, timeout=3).is_displayed()
            self.logger.info(f"Профиль пользователя '{firstname}' найден на странице: {is_visible}")
            return is_visible
        except Exception:
            self.logger.warning(f"Профиль пользователя '{firstname}' НЕ появился за заданное время")
            return False
