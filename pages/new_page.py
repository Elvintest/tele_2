from .main_page import MainPage
from .locators import MainPageLocators

class NewPage(MainPage):
    def open_news(self):
        self.browser.find_element(*MainPageLocators.button_news).click()
