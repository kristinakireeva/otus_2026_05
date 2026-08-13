import pytest
import allure
from pages import MainPage, CatalogPage, ProductPage, RegisterPage, AdminLoginPage


@pytest.mark.order(1)
@allure.title("Проверка наличия элементов на главной странице")
def test_01_main_page_elements(browser, base_url):
    main_page = MainPage(browser, base_url)
    main_page.open()
    assert main_page.wait_for_element(main_page.LOGO), "Логотип не отображается"
    assert main_page.wait_for_element(main_page.SEARCH_INPUT), "Строка поиска не найдена"
    assert main_page.wait_for_element(main_page.CART_BUTTON), "Кнопка корзины не найдена"
    assert main_page.wait_for_element(main_page.SLIDER), "Слайдер не отображается"
    assert main_page.wait_for_element(main_page.CONTACT_LINK), "Ссылка контактов не найдена"


@pytest.mark.order(2)
@allure.title("Проверка наличия элементов на странице каталог")
def test_02_catalog_page_elements(browser, base_url):
    catalog_page = CatalogPage(browser, base_url)
    catalog_page.open()
    assert catalog_page.wait_for_element(catalog_page.FILTER_BLOCK), "Блок фильтров не отображается"
    assert catalog_page.wait_for_element(catalog_page.PRODUCTS_GRID), "Сетка товаров не отображается"
    assert catalog_page.wait_for_element(catalog_page.BREADCRUMBS), "Строка навигации не найдена"
    assert catalog_page.wait_for_element(catalog_page.SORT_DROPDOWN), "Выпадающий список сортировки не найден"
    assert catalog_page.wait_for_element(catalog_page.CATEGORY_TITLE), "Заголовок категории не найден"


@pytest.mark.order(3)
@allure.title("Проверка наличия элементов на карточке товара")
def test_03_product_page_elements(browser, base_url):
    product_page = ProductPage(browser, base_url)
    product_page.open()
    assert product_page.wait_for_element(product_page.PRODUCT_COVER), "Главное изображение товара не отображается"
    assert product_page.wait_for_element(product_page.PRODUCT_NAME), "Название товара не найдено"
    assert product_page.wait_for_element(product_page.ADD_TO_CART_BTN), "Кнопка добавления в корзину не найдена"
    assert product_page.wait_for_element(product_page.PRODUCT_PRICE), "Цена товара не найдена"
    assert product_page.wait_for_element(product_page.QUANTITY_INPUT), "Поле выбора количества не найдено"


@pytest.mark.order(4)
@allure.title("Проверка наличия элементов на странице входа в админку")
def test_04_admin_login_elements(browser, base_url):
    admin_login_page = AdminLoginPage(browser, base_url)
    admin_login_page.open()
    assert admin_login_page.wait_for_element(admin_login_page.LOGIN_BOX), "Форма авторизации не отображается"


@pytest.mark.order(5)
@allure.title("Проверка наличия элементов на странице регистрации пользователя")
def test_05_registration_page_elements(browser, base_url):
    """Тест проверяет наличие ключевых элементов на странице регистрации (Замечание 3)"""
    register_page = RegisterPage(browser, base_url)

    with allure.step("Открываем страницу регистрации"):
        register_page.open()

    with allure.step("Проверка элементов формы регистрации"):
        assert register_page.wait_for_element(register_page.FIRSTNAME_INPUT), "Поле ввода имени не найдено"
        assert register_page.wait_for_element(register_page.LASTNAME_INPUT), "Поле ввода фамилии не найдено"
        assert register_page.wait_for_element(register_page.EMAIL_INPUT), "Поле ввода Email не найдено"
        assert register_page.wait_for_element(register_page.PASSWORD_INPUT), "Поле ввода пароля не найдено"
        assert register_page.wait_for_element(register_page.SAVE_BUTTON), "Кнопка сохранения не найдена"