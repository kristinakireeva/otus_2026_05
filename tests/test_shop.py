import pytest
import allure
from pages import MainPage, CatalogPage, ProductPage


@pytest.mark.order(7)
@allure.title("Добавление товара в корзину с главной страницы")
def test_07_add_to_cart_random_product(browser, base_url):
    main_page = MainPage(browser, base_url)
    product_page = ProductPage(browser, base_url)
    main_page.open()
    main_page.click_random_product()
    product_page.click_add_to_cart()
    modal_title = product_page.get_cart_modal_title()
    assert "Товар добавлен в корзину" in modal_title.text, f"Ожидался текст подтверждения, но отображается: '{modal_title.text}'"


@pytest.mark.order(8)
@allure.title("Изменение валюты отображения цен на главной странице")
def test_08_currency_change_main_page(browser, base_url):
    main_page = MainPage(browser, base_url)
    main_page.open()
    main_page.change_currency_to_usd()
    new_prices = main_page.get_product_prices_text()

    assert new_prices, "Список цен на главной пуст!"
    # Строгая валидация знака валюты (Замечание 8)
    for price in new_prices:
        assert "$" in price, f"В цене '{price}' на главной отсутствует символ '$'!"


@pytest.mark.order(9)
@allure.title("Изменение валюты отображения цен на товары в каталоге")
def test_09_currency_change_catalog_page(browser, base_url):
    catalog_page = CatalogPage(browser, base_url)
    catalog_page.open()
    catalog_page.change_currency_to_usd()
    new_catalog_prices = catalog_page.get_catalog_product_prices_text()

    assert new_catalog_prices, "Список цен в каталоге пуст!"
    # Строгая валидация знака валюты (Замечание 8)
    for price in new_catalog_prices:
        assert "$" in price, f"В цене '{price}' в каталоге отсутствует символ '$'!"