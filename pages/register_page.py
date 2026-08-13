import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Страница регистрации нового пользователя в магазине PrestaShop"""
    URL = "/registration"

    # Поля ввода текста
    FIRSTNAME_INPUT = (By.NAME, "firstname")
    LASTNAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")  # Фокус на этом поле (Замечание 3)

    # Обязательные чекбоксы соглашений
    GDPR_CHECKBOX = (By.XPATH, "//input[@name='psgdpr']")
    NEWSLETTER_CHECKBOX = (By.XPATH, "//input[@name='newsletter']")
    PRIVACY_CHECKBOX = (By.XPATH, "//input[@name='customer_privacy']")

    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'form-control-submit')]")

    @allure.step("Создание и заполнение формы нового пользователя")
    def register_new_user(self, firstname, lastname, email, password):
        # Используем универсальные методы ввода из BasePage (Замечание 6)
        self.enter_text(self.FIRSTNAME_INPUT, firstname)
        self.enter_text(self.LASTNAME_INPUT, lastname)
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)  # Корректно заполняем пароль

        # Взаимодействие с чекбоксами через SPACE без time.sleep (Замечание 5)
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
        return self.wait_for_element(user_profile_locator).is_displayed()
