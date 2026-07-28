from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url="http://localhost:8081"):
        self.driver = driver
        self.base_url = base_url


    def wait_for_element(self, by, value, timeout=10):
        """Метод явного ожидания элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_clickable(self, by, value, timeout=15):
        """Новый метод: ожидание, пока элемент станет доступен для клика"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def wait_for_elements(self, by, value, timeout=10):
        """Метод явного ожидания списка элементов"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )


class MainPage(BasePage):
    """Страница 1: Главная"""
    URL = "/"

    LOGO = (By.XPATH, "//div[@id='_desktop_logo']")
    SEARCH_INPUT = (By.XPATH, "//input[@name='s']")
    CART_BUTTON = (By.XPATH, "//div[@id='_desktop_cart']")
    SLIDER = (By.XPATH, "//div[contains(@class, 'carousel')]")
    CONTACT_LINK = (By.XPATH, "//div[@id='contact-link']//a")
    RANDOM_PRODUCT_LINK = (By.XPATH,
                           "//div[@class='products']//article[contains(@class, 'product-miniature')]//a[@class='thumbnail product-thumbnail'] | //a[contains(@class, 'product-thumbnail')]")
    CURRENCY_DROP_DOWN = (By.XPATH, "//div[@id='_desktop_currency_selector']//button")
    ANY_CURRENCY_OPTION = (By.XPATH,
                           "//ul[contains(@class, 'dropdown-menu')]//a[contains(text(), 'USD') or contains(text(), '$')]")
    PRODUCT_PRICES = (By.XPATH, "//section[@class='featured-products clearfix']//span[@class='price']")


class CatalogPage(BasePage):
    """Страница 2: Каталог"""
    URL = "/3-clothes"

    BREADCRUMBS = (By.XPATH, "//nav[@class='breadcrumb']")
    PRODUCTS_GRID = (By.XPATH, "//*[@id='js-product-list']")
    SORT_DROPDOWN = (By.XPATH, "//div[contains(@class, 'products-sort-order')]")
    FILTER_BLOCK = (By.XPATH, "//div[@id='search_filters']")
    CATEGORY_TITLE = (By.XPATH, "//h1[contains(@class, 'h1')]")
    CURRENCY_DROP_DOWN = (By.XPATH, "//div[@id='_desktop_currency_selector']//button")
    ANY_CURRENCY_OPTION = (By.XPATH,
                           "//ul[contains(@class, 'dropdown-menu')]//a[contains(text(), 'USD') or contains(text(), '$')]")
    CATALOG_PRODUCT_PRICES = (By.XPATH, "//div[@id='js-product-list']//span[@class='price']")


class ProductPage(BasePage):
    """Страница 3: Карточка товара"""
    URL = "/men/1-1-hummingbird-printed-t-shirt.html"

    PRODUCT_NAME = (By.XPATH, "//h1[@itemprop='name'] | //h1")
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(@class, 'add-to-cart')]")
    PRODUCT_PRICE = (By.XPATH, "//*[@itemprop='price'] | //span[@class='current-price-value']")
    PRODUCT_COVER = (By.XPATH, "//div[contains(@class, 'images-container')]//img | //img[@class='js-qv-product-cover']")
    QUANTITY_INPUT = (By.XPATH, "//input[@id='quantity_wanted']")
    CART_MODAL_CHECK = (By.XPATH, "//h4[@id='myModalLabel']")


class AdminLoginPage(BasePage):
    """Страница 4: Логин в админку /administration"""
    URL = "/administration"

    LOGIN_BOX = (By.XPATH, "//*[@id='login-panel']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='passwd']")
    SUBMIT_BTN = (By.XPATH, "//button[@id='submit_login'] | //button[@name='submitLogin']")
    FORGOT_PASSWORD = (By.XPATH, "//a[contains(@class, 'forgot-password')]")
    ADMIN_PROFILE_IMG = (By.XPATH, "//i[text()='account_circle'] | //span[@class='employee_avatar_small']")
    LOGOUT_LINK = (By.XPATH, "//a[@id='header_logout']")


class RegisterPage(BasePage):
    """Страница 5: Регистрация пользователя"""
    URL = "/login?create_account=1"

    GENDER_RADIO = (By.NAME, "id_gender")
    FIRSTNAME_INPUT = (By.NAME, "firstname")
    LASTNAME_INPUT = (By.NAME, "lastname")
    EMAIL_INPUT = (By.NAME, "email")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'form-control-submit')]")
