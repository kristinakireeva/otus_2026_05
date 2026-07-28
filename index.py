from selenium import webdriver
import time


chrome = webdriver.Chrome('/opt/homebrew/bin/chromedriver')
chrome.get('http://localhost:8081/')
print(chrome.title)  # PrestaShop
time.sleep(5)

chrome.quit()