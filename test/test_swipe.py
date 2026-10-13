import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# 1. Настройка параметров подключения к вашему эмулятору
options = AppiumOptions()
options.set_capability('platformName', 'Android')
options.set_capability('automationName', 'UiAutomator2')
options.set_capability('deviceName', 'Medium Phone API 37.0')

# Принудительно направляем Appium в Android Studio, обходя баги LDPlayer
options.set_capability('androidHome', 'C:\\Users\\Admin\\AppData\\Local\\Android\\Sdk')

# Строгие параметры обхода проверки цифровых подписей на Windows
options.set_capability('allowTestPackages', True)
options.set_capability('noSign', True)

# Запускаем системный лаунчер (главный экран Android)
options.set_capability('appPackage', 'com.google.android.apps.nexuslauncher')
options.set_capability('appActivity', '.NexusLauncherActivity')
options.set_capability('noReset', True)

# Подключение к вашему запущенному Appium Server
driver = webdriver.Remote('http://127.0.0.1:4723', options=options)


def swipe_gesture(driver, start_y_pct, end_y_pct):
    """Универсальная и надежная функция для свайпа по вертикали"""
    size = driver.get_window_size()
    width = size['width']
    height = size['height']

    start_x = int(width / 2)
    start_y = int(height * start_y_pct)
    end_x = int(width / 2)
    end_y = int(height * end_y_pct)

    # Используем проверенный нативный метод Appium для свайпа
    driver.swipe(start_x, start_y, end_x, end_y, duration=800)
    time.sleep(1.5)  # Ожидание завершения анимации прокрутки


try:
    print("[LOG] Главный экран открыт. Свайпаем ВВЕРХ, чтобы открыть меню всех приложений...")
    # Свайп снизу вверх: от 80% высоты экрана до 20%
    swipe_gesture(driver, start_y_pct=0.8, end_y_pct=0.2)

    calendar_element = None
    max_swipes = 10
    swipe_count = 0
    target_text = "Calendar"  # Поиск по английскому названию

    print(f"[LOG] Меню открыто. Начинаем поиск приложения '{target_text}'...")

    while swipe_count < max_swipes:
        try:
            # Ищем элемент по его тексту "Calendar"
            calendar_element = driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{target_text}")'
            )

            if calendar_element.is_displayed():
                print(f"[LOG] Ура! Приложение '{target_text}' найдено после {swipe_count} свайпов.")
                calendar_element.click()
                print("[LOG] Клик по календарю выполнен успешно!")
                break

        except NoSuchElementException:
            # Если не нашли на текущем экране меню — листаем дальше ВНИЗ (палец тянем вверх)
            print(f"[LOG] '{target_text}' не виден. Выполняем свайп вниз №{swipe_count + 1}...")
            swipe_gesture(driver, start_y_pct=0.7, end_y_pct=0.3)
            swipe_count += 1

    if swipe_count >= max_swipes and not calendar_element:
        raise NoSuchElementException(
            f"Ошибка: Приложение '{target_text}' не найдено в меню после {max_swipes} свайпов."
        )

except Exception as e:
    print(f"[CRITICAL ERROR] Тест упал с ошибкой: {e}")
    raise e

finally:
    print("[LOG] Закрываем сессию драйвера.")
    driver.quit()
