import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    """Страница управления товарами в панели администратора PrestaShop"""

    CATALOG_MENU_TAB = (By.XPATH, "//li[@id='subtab-AdminCatalog']/a")

    PRODUCTS_MENU_LINK = (By.XPATH, "//li[@id='subtab-AdminProducts']/a")

    NEW_PRODUCT_BTN = (By.ID, "page-header-desc-configuration-add")

    CONFIRM_ADD_BTN = (By.XPATH,
                       "//button[contains(text(), 'Добавить товар')] | //button[contains(text(), 'Next') or contains(text(), 'Add')]")

    PRODUCT_NAME_INPUT = (By.ID, "product_header_name_1")

    SAVE_PRODUCT_BTN = (By.ID, "product_footer_save")

    FIRST_PRODUCT_ACTIONS_BTN = (By.XPATH,
                                 "//tbody/tr//div[@class='btn-group-action']//a[@data-toggle='dropdown'] | //tbody/tr//a[contains(@class, 'dropdown-toggle')]")
    DELETE_PRODUCT_LINK = (By.XPATH,
                           "//tbody/tr//a[contains(@class, 'delete')] | //tbody/tr//a[contains(@data-url, 'delete')]")
    CONFIRM_DELETE_BTN = (By.XPATH, "//button[contains(@class, 'btn-confirm-submit') and contains(text(), 'Удалить')]")

    PRODUCT_CREATED_ALERT = (By.XPATH,
                             "//div[contains(@class, 'alert-success')]//p[contains(text(), 'Обновление завершено')]")
    PRODUCT_DELETED_ALERT = (By.XPATH,
                             "//div[contains(@class, 'alert-success')]//p[contains(text(), 'Удаление завершено')]")

    def open_via_menu(self):
        self.wait_for_clickable(self.CATALOG_MENU_TAB).click()
        time.sleep(1.5)

        self.wait_for_clickable(self.PRODUCTS_MENU_LINK).click()
        time.sleep(1.5)
        return self

    def click_new_product(self):
        self.wait_for_clickable(self.NEW_PRODUCT_BTN).click()
        time.sleep(2.0)

        try:
            modal_iframe = self.wait_for_element((By.TAG_NAME, "iframe"))
            self.driver.switch_to.frame(modal_iframe)
        except Exception:
            pass

        return self

    def click_confirm_add_product(self):
        confirm_btn = self.wait_for_clickable(self.CONFIRM_ADD_BTN)

        from selenium.webdriver.common.keys import Keys
        confirm_btn.send_keys(Keys.ENTER)
        time.sleep(4.0)

        self.driver.switch_to.default_content()
        return self

    def create_simple_product(self, name, price=0):
        name_field = self.wait_for_element(self.PRODUCT_NAME_INPUT)
        name_field.click()

        from selenium.webdriver.common.keys import Keys
        name_field.send_keys(Keys.CONTROL + "a")
        name_field.send_keys(Keys.BACKSPACE)
        name_field.send_keys(name)
        time.sleep(0.5)

        self.wait_for_clickable(self.SAVE_PRODUCT_BTN).click()
        time.sleep(2.5)
        return self

    def click_first_product_actions(self):
        self.wait_for_clickable(self.FIRST_PRODUCT_ACTIONS_BTN).click()
        time.sleep(0.5)
        return self

    def click_delete_product(self):
        self.wait_for_clickable(self.DELETE_PRODUCT_LINK).click()
        time.sleep(1.0)
        return self

    def confirm_product_deletion(self):
        self.wait_for_clickable(self.CONFIRM_DELETE_BTN).click()
        time.sleep(3.0)
        return self

    def is_creation_success_visible(self):
        return self.wait_for_element(self.PRODUCT_CREATED_ALERT).is_displayed()

    def is_deletion_success_visible(self):
        return self.wait_for_element(self.PRODUCT_DELETED_ALERT).is_displayed()

    def go_back_to_products_list(self):
        self.wait_for_clickable(self.PRODUCTS_MENU_LINK).click()
        time.sleep(2.0)
        return self

    def is_product_present_in_list(self, product_name):
        product_row_xpath = (By.XPATH,
                             f"//td[contains(text(), '{product_name}')] | //a[contains(text(), '{product_name}')]")
        try:
            return self.wait_for_element(product_row_xpath, timeout=10).is_displayed()
        except Exception:
            return False
