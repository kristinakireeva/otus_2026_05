import unittest
import pytest
from pages import MainPage, CatalogPage, ProductPage, AdminLoginPage, RegisterPage


class PrestaShopPresenceTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_class_fixtures(self, browser, base_url):
        self.driver = browser
        self.base_url = base_url

    @pytest.mark.order(1)
    def test_01_main_page_elements(self):
        """Тест проверяет наличие ключевых элементов на главной странице"""
        main_page = MainPage(self.driver, self.base_url)
        main_page.open()

        # Проверяем элементы напрямую через базовое ожидание, без вызова несуществующих методов
        self.assertTrue(main_page.wait_for_element(main_page.LOGO), "Логотип не отображается")
        self.assertTrue(main_page.wait_for_element(main_page.SEARCH_INPUT), "Строка поиска не найдена")
        self.assertTrue(main_page.wait_for_element(main_page.CART_BUTTON), "Кнопка корзины не найдена")
        self.assertTrue(main_page.wait_for_element(main_page.SLIDER), "Слайдер не отображается")
        self.assertTrue(main_page.wait_for_element(main_page.CONTACT_LINK), "Ссылка контактов не найдена")

    @pytest.mark.order(2)
    def test_02_catalog_page_elements(self):
        """Тест проверяет наличие ключевых элементов на странице каталога"""
        catalog_page = CatalogPage(self.driver, self.base_url)
        catalog_page.open()

        self.assertTrue(catalog_page.wait_for_element(catalog_page.FILTER_BLOCK), "Блок фильтров не отображается")
        self.assertTrue(catalog_page.wait_for_element(catalog_page.PRODUCTS_GRID), "Сетка товаров не отображается")
        self.assertTrue(catalog_page.wait_for_element(catalog_page.BREADCRUMBS), "Хлебные крошки не найдены")
        self.assertTrue(catalog_page.wait_for_element(catalog_page.SORT_DROPDOWN), "Дропдаун сортировки не найден")
        self.assertTrue(catalog_page.wait_for_element(catalog_page.CATEGORY_TITLE), "Заголовок категории не найден")

    @pytest.mark.order(3)
    def test_03_product_page_elements(self):
        """Тест проверяет наличие ключевых элементов на карточке товара"""
        product_page = ProductPage(self.driver, self.base_url)
        product_page.open()

        self.assertTrue(product_page.wait_for_element(product_page.PRODUCT_COVER),
                        "Главное изображение товара не отображается")
        self.assertTrue(product_page.wait_for_element(product_page.PRODUCT_NAME), "Название товара не найдено")
        self.assertTrue(product_page.wait_for_element(product_page.ADD_TO_CART_BTN),
                        "Кнопка добавления в корзину не найдена")
        self.assertTrue(product_page.wait_for_element(product_page.PRODUCT_PRICE), "Цена товара не найдена")
        self.assertTrue(product_page.wait_for_element(product_page.QUANTITY_INPUT), "Поле выбора количества не найдено")

    @pytest.mark.order(4)
    def test_04_admin_login_elements(self):
        """Тест проверяет наличие элементов на странице логина в админку"""
        admin_login_page = AdminLoginPage(self.driver, self.base_url)
        admin_login_page.open()

        self.assertTrue(admin_login_page.wait_for_element(admin_login_page.LOGIN_BOX),
                        "Форма авторизации не отображается")

    @pytest.mark.order(5)
    def test_05_registration_page_elements(self):
        """Тест проверяет наличие элементов на странице регистрации пользователя"""
        register_page = RegisterPage(self.driver, self.base_url)
        register_page.open()

        self.assertTrue(register_page.wait_for_element(register_page.GENDER_RADIO),
                        "Выбор пола (Radio button) не найден")
        self.assertTrue(register_page.wait_for_element(register_page.FIRSTNAME_INPUT), "Поле ввода имени не найдено")
        self.assertTrue(register_page.wait_for_element(register_page.LASTNAME_INPUT), "Поле ввода фамилии не найдено")
        self.assertTrue(register_page.wait_for_element(register_page.EMAIL_INPUT), "Поле ввода Email не найдено")
        self.assertTrue(register_page.wait_for_element(register_page.SAVE_BUTTON), "Кнопка сохранения не найдена")
