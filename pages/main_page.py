from selenium.webdriver.common.by import By

from .base_page import BasePage


class MainPage(BasePage):
    def login(self):
        self.browser.find_element(By.ID, "mail").send_keys('test2@test.ru')
        self.browser.find_element(By.ID, "password").send_keys('test2')
        self.browser.find_element(By.CLASS_NAME, "ant-btn.ant-btn-primary").click()

