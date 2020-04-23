import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    # parser.addoption('--language', action='store', default=None,
    #                  help="Choose browser: chrome or firefox")


@pytest.fixture(scope="function")
def browser(request):
    """"path for debug"""
    path_driver_chrome = "C:\\Users\\eyagudin\\Desktop\\Autotests_tele2\\chromedriver.exe"
    path_driver_firefox = "C:\\Users\\eyagudin\\Desktop\\Autotests_tele2\\geckodriver.exe"
    browser_name = request.config.getoption("browser_name")
    browser = None
    # user_language = request.config.getoption("language")
    if browser_name == "chrome":
        options = Options()
        # options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Chrome(path_driver_chrome, options=options)
        browser.maximize_window()
        print("\nstart chrome browser for test..")
    elif browser_name == "firefox":
        options = Options()
        # options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Firefox(path_driver_firefox, options=options)
        print("\nstart firefox browser for test..")
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()

