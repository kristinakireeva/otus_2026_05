import allure
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Карточка товара"""
    URL = "/men/1-1-hummingbird-printed-t-shirt.html"

    PRODUCT_NAME = (By.XPATH, "//h1[@itemprop='name'] | //h1")
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(@class, 'add-to-cart')]")
    PRODUCT_PRICE = (By.XPATH, "//*[@itemprop='price'] | //span[@class='current-price-value']")
    PRODUCT_COVER = (By.XPATH, "//div[contains(@class, 'images-container')]//img | //img[@class='js-qv-product-cover']")
    QUANTITY_INPUT = (By.XPATH, "//input[@id='quantity_wanted']")
    CART_MODAL_CHECK = (By.XPATH, "//h4[@id='myModalLabel']")

    @allure.step("Добавление товара в корзину")
    def click_add_to_cart(self):
        self.logger.info("Нажатие кнопки 'Добавить в корзину'")
        self.click_element(self.ADD_TO_CART_BTN)

    @allure.step("Получение текста из модального окна подтверждения")
    def get_cart_modal_title(self):
        return self.get_element_text(self.CART_MODAL_CHECK)
