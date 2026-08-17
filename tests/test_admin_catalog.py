import pytest
import random
import allure
from pages import AdminLoginPage, AdminProductsPage


@pytest.mark.order(10)
@allure.title("Создание нового товара через администратора с проверкой в списке")
def test_10_add_new_product_by_admin(admin_session, base_url):
    # Использована фикстура admin_session для исключения дублирования (Замечание 7)
    admin_products_page = AdminProductsPage(admin_session, base_url)
    admin_products_page.open_via_menu()

    product_name = f"Test T-Shirt {random.randint(1000, 9999)}"
    admin_products_page.click_new_product()
    admin_products_page.click_confirm_add_product()
    admin_products_page.create_simple_product(product_name)

    assert admin_products_page.is_creation_success_visible(), "Уведомление об успехе не появилось"

    admin_products_page.go_back_to_products_list()
    assert admin_products_page.is_product_present_in_list(product_name), "Созданный товар не найден в списке"


@pytest.mark.order(11)
@allure.title("Удаление товара из списка в разделе администратора")
def test_11_delete_product_by_admin(admin_session, base_url):
    # Использована фикстура admin_session (Замечание 7)
    admin_products_page = AdminProductsPage(admin_session, base_url)
    admin_products_page.open_via_menu()

    admin_products_page.click_first_product_actions()
    admin_products_page.click_delete_product()
    admin_products_page.confirm_product_deletion()

    assert admin_products_page.is_deletion_success_visible(), "Уведомление об удалении не появилось"

