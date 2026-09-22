import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    """Страница управления товарами в панели администратора PrestaShop"""

    CATALOG_MENU_TAB = (By.XPATH, "//li[@id='subtab-AdminCatalog']/a")
    PRODUCTS_MENU_LINK = (By.XPATH, "//li[@id='subtab-AdminProducts']/a")
    NEW_PRODUCT_BTN = (By.ID, "page-header-desc-configuration-add")
    CONFIRM_ADD_BTN = (By.XPATH, "//button[contains(text(), 'Добавить товар')] | //button[contains(text(), 'Next') or contains(text(), 'Add')]")
    PRODUCT_NAME_INPUT = (By.ID, "product_header_name_1")
    SAVE_PRODUCT_BTN = (By.ID, "product_footer_save")
    FIRST_PRODUCT_ACTIONS_BTN = (By.XPATH, "//tbody/tr//div[@class='btn-group-action']//a[@data-toggle='dropdown'] | //tbody/tr//a[contains(@class, 'dropdown-toggle')]")
    DELETE_PRODUCT_LINK = (By.XPATH, "//tbody/tr//a[contains(@class, 'delete')] | //tbody/tr//a[contains(@data-url, 'delete')]")
    CONFIRM_DELETE_BTN = (By.XPATH, "//button[contains(@class, 'btn-confirm-submit') and contains(text(), 'Удалить')]")
    PRODUCT_CREATED_ALERT = (By.XPATH, "//div[contains(@class, 'alert-success')]//p[contains(text(), 'Обновление завершено')]")
    PRODUCT_DELETED_ALERT = (By.XPATH, "//div[contains(@class, 'alert-success')]//p[contains(text(), 'Удаление завершено')]")

    @allure.step("Переход в раздел 'Товары' через меню каталога")
    def open_via_menu(self):
        self.click_element(self.CATALOG_MENU_TAB)
        self.click_element(self.PRODUCTS_MENU_LINK)
        return self

    @allure.step("Нажатие кнопки создания нового товара")
    def click_new_product(self):
        self.click_element(self.NEW_PRODUCT_BTN)
        # Динамическое ожидание фрейма модального окна без фиксированных пауз (Замечание 5)
        try:
            self.logger.info("Ожидание появления iframe модального окна и переключение в него")
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
            )
            self.logger.info("Успешно переключились внутрь iframe")
        except Exception:
            self.logger.warning("Iframe не был обнаружен за 5 сек, продолжаем работу в основном контексте")
        return self

    @allure.step("Подтверждение добавления товара")
    def click_confirm_add_product(self):
        confirm_btn = self.wait_for_clickable(self.CONFIRM_ADD_BTN)
        self.logger.info("Нажатие клавиши enter для подтверждения добавления товара")
        confirm_btn.send_keys(Keys.ENTER)

        self.logger.info("Переключение контекста обратно на основную страницу")
        self.driver.switch_to.default_content()
        return self

    @allure.step("Создание и заполнение формы нового товара: {name}")
    def create_simple_product(self, name, price=0):
        self.enter_text(self.PRODUCT_NAME_INPUT, name)
        self.click_element(self.SAVE_PRODUCT_BTN)
        return self

    @allure.step("Выбор товара из списка и его удаление")
    def click_first_product_actions(self):
        self.click_element(self.FIRST_PRODUCT_ACTIONS_BTN)
        return self

    @allure.step("Нажатие кнопки удаления товара")
    def click_delete_product(self):
        self.click_element(self.DELETE_PRODUCT_LINK)
        return self

    @allure.step("Подтверждение удаления товара")
    def confirm_product_deletion(self):
        self.click_element(self.CONFIRM_DELETE_BTN)
        self.logger.info("Ожидание исчезновения кнопки подтверждения удаления")
        # Ожидаем завершения удаления по исчезновению кнопки подтверждения
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.CONFIRM_DELETE_BTN)
        )
        self.logger.info("Кнопка подтверждения исчезла")
        return self

    @allure.step("Проверка уведомления о создании товара")
    def is_creation_success_visible(self):
        is_visible = self.wait_for_element(self.PRODUCT_CREATED_ALERT).is_displayed()
        self.logger.info(f"Отображение уведомления успешного создания товара {is_visible}")
        return is_visible

    @allure.step("Проверка уведомления об удалении товара в каталоге")
    def is_deletion_success_visible(self):
        is_visible = self.wait_for_element(self.PRODUCT_DELETED_ALERT).is_displayed()
        self.logger.info(f"отображение уведомления успешного удаления товара {is_visible}")
        return is_visible

    @allure.step("Возврат к общему списку товаров")
    def go_back_to_products_list(self):
        self.click_element(self.PRODUCTS_MENU_LINK)
        return self

    @allure.step("Проверка наличия созданного товара '{product_name}' в каталоге")
    def is_product_present_in_list(self, product_name):
        product_row_xpath = (By.XPATH, f"//td[contains(text(), '{product_name}')] | //a[contains(text(), '{product_name}')]")
        self.logger.info(f"Поиск товара {product_name} в таблице каталога")
        try:
            is_present = self.wait_for_element(product_row_xpath, timeout=5).is_displayed()
            self.logger.info(f"Товар {product_name} найден в списке {is_present}")
            return is_present
        except Exception:
            self.logger.warning(f"Товар {product_name} не найден в списке за тайм-аут")
            return False
