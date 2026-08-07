import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Страница регистрации нового пользователя в магазине PrestaShop"""
    URL = "/registration"

    FIRSTNAME_INPUT = (By.NAME, "firstname")
    LASTNAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")

    GDPR_CHECKBOX = (By.XPATH, "//input[@name='psgdpr']")
    NEWSLETTER_CHECKBOX = (By.XPATH, "//input[@name='newsletter']")
    PRIVACY_CHECKBOX = (By.XPATH, "//input[@name='customer_privacy']")

    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'form-control-submit')]")

    def register_new_user(self, firstname, lastname, email, password):
        firstname_field = self.wait_for_element(self.FIRSTNAME_INPUT)
        firstname_field.click()
        from selenium.webdriver.common.keys import Keys
        firstname_field.send_keys(Keys.CONTROL + "a")
        firstname_field.send_keys(Keys.BACKSPACE)
        firstname_field.send_keys(firstname)

        lastname_field = self.wait_for_element(self.LASTNAME_INPUT)
        lastname_field.click()
        lastname_field.send_keys(Keys.CONTROL + "a")
        lastname_field.send_keys(Keys.BACKSPACE)
        lastname_field.send_keys(lastname)

        email_field = self.wait_for_element(self.EMAIL_INPUT)
        email_field.click()
        email_field.send_keys(Keys.CONTROL + "a")
        email_field.send_keys(Keys.BACKSPACE)
        email_field.send_keys(email)

        password_field = self.wait_for_element(self.PASSWORD_INPUT)
        password_field.click()
        password_field.send_keys(Keys.CONTROL + "a")
        password_field.send_keys(Keys.BACKSPACE)
        password_field.send_keys(password)

        self.wait_for_element(self.GDPR_CHECKBOX).send_keys(Keys.SPACE)
        time.sleep(0.2)

        self.wait_for_element(self.NEWSLETTER_CHECKBOX).send_keys(Keys.SPACE)
        time.sleep(0.2)

        self.wait_for_element(self.PRIVACY_CHECKBOX).send_keys(Keys.SPACE)
        time.sleep(0.2)

        self.wait_for_clickable(self.SAVE_BUTTON).click()

        time.sleep(2.5)
        return self