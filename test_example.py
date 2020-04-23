from .pages.main_page import MainPage
from .pages.new_page import NewPage
from .pages.locators import MainPageLocators,MbkpiLocators,TaskLocators, ReportLocators, CmsLocators
import time
from selenium.common.exceptions import NoSuchElementException
import os,os.path
import json
import requests
from datetime import datetime


# def test_all_content_well(browser):
#     link = "master.c1.dlr.tele2.at-consulting.ru:30467"
#     page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
#     page.open()  # открываем страницу
#     page.login()  # выполняем метод страницы - переходим на страницу логина
#     time.sleep(3)
def check_exists(browser, locator):  # функция для вывода ошибок
    try:
        browser.find_element(*locator)
    except NoSuchElementException:
        return False
    return True


def test_all_content_well(browser):
    link = "master.c1.dlr.tele2.at-consulting.ru:30467"
    page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.login()  # выполняем метод страницы - переходим на страницу логина
    # browser.execute_script("window.scrollBy(0, 100);")
    browser.implicitly_wait(20)
    # проверяем таблицу MB_KPI на главной
    assert check_exists(browser, MainPageLocators.mbkpi_desctop_content), '!MB_KPI on desktop doesnt exist!'
    browser.implicitly_wait(20)
    # page.open_news()
    browser.find_element(*MainPageLocators.button_news).click()  # открываем страницу новостей
    browser.implicitly_wait(20)
    # проверяем наличие списка новостей
    assert check_exists(browser, CmsLocators.news_list), '!news_list doesnt exist!'
    browser.implicitly_wait(10)
    # открываем страницу отчетов
    browser.find_element(*MainPageLocators.button_reports).click()
    # Проверяем наличие хотя бы одного отчета на странице
    browser.implicitly_wait(60)
    assert check_exists(browser,ReportLocators.button_download_report), '!NO any available report on the page!'
    # открываем страницу задач
    browser.find_element(*MainPageLocators.button_tasks).click()
    # Проверяем наличие хотя бы одной задачи в списке
    browser.implicitly_wait(10)
    assert check_exists(browser, TaskLocators.single_task), '!NO any available task!'

def test_mb_kpi_download(browser):

    link = "master.c1.dlr.tele2.at-consulting.ru:30467"
    page = NewPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.login()  # выполняем метод страницы - переходим на страницу логина
    browser.implicitly_wait(20)
    browser.find_element(*MainPageLocators.button_mb_kpi).click()
    browser.implicitly_wait(20)
    time.sleep(10)
    browser.find_element(*MbkpiLocators.button_mb_kpi_download).click()
    browser.implicitly_wait(200)
    assert browser.find_element(*MbkpiLocators.button_download_ready_report), 'LINK FOR DOWNLOADING WASNT CREATED'
    browser.find_element(*MbkpiLocators.button_download_ready_report).click()
    browser.find_element(*MbkpiLocators.button_close_report).click()
    time.sleep(20)
    home_directory = os.path.expanduser("~\\Downloads")
    files_arrow = os.listdir(home_directory)
    assert 'MB_KPI.xlsx' in files_arrow, '!NO downloaded file mb_kpi!'
    file = os.path.join(home_directory,'MB_KPI.xlsx')
    report_size = os.path.getsize(file)
    assert report_size > 0, '!MB_KPI file is empty!'
    if report_size > 0:
        os.remove(file)


def test_create_task():
    # Логинимся на портале через апи, получаем токен
    response = requests.post('http://master.c1.dlr.tele2.at-consulting.ru:30467/gw/public/auth/user/login',
                             json={"username": "test3@test.ru", "password": "test3"},
                             headers={"Content-Type": "application/json"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of login is {response.status_code}'
    login = response.json()
    token = login['data']['token']

    # Запрашиваем список задач с токеном, парсим, выводи number_tasks
    response = requests.post('http://master.c1.dlr.tele2.at-consulting.ru:30467/gw/secured/task/?size=1000&page=0',
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of request of number_tasks is {response.status_code}'

    number_tasks_before = int(response.json()['totalElements'])
    print(number_tasks_before)

    # Создаем задачу
    response = requests.put('http://master.c1.dlr.tele2.at-consulting.ru:30467/gw/secured/task/',
                            headers={"Authorization": f"Bearer {token}", "content-type": "application/json"},
                            json={"kindMnemonic": "ItSupport", "formData": {"mnemonic": "DEALER_IT_CONTACTS",
                                                                            "title": "Общие услуги - контакты ИТ дилера",
                                                                            "systemId": "E5A07302-3E0F-4DB0-93D1-D2A3DEC695C4",
                                                                            "systemName": "ИТ поддержка розничной сети",
                                                                            "automation": "Общие услуги",
                                                                            "sortOrder": 1100, "filesNeededCount": 0,
                                                                            "description": f"created by AUTOTEST {datetime.now()}",
                                                                            "refItSupportMnemonic": "DEALER_IT_CONTACTS",
                                                                            "posId": "97186",
                                                                            "fio": f"AUTOTEST {datetime.now()}",
                                                                            "mail": "autotest@test.ru",
                                                                            "phone": "79109755555"},
                                  "description": "autotesttest", "responsibleUser": None, "responsibleGroup": None,
                                  "attachmentUuidCollection": [], "startAfterCreation": True})
    assert response.status_code == 201 or response.status_code == 201, f'CREATING TASK IS FAILING, status code is {response.status_code}'
    print(response.json())
    print(response.status_code)
    time.sleep(20)
    # Повторно запрашиваем список задач с токеном, парсим, выводи number_tasks
    response = requests.post('http://master.c1.dlr.tele2.at-consulting.ru:30467/gw/secured/task/?size=1000&page=0',
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of request of number_tasks is {response.status_code}'

    number_tasks_after = int(response.json()['totalElements'])
    print(number_tasks_after)
    # Проверяем, что задач в базе на одну больше
    assert number_tasks_after == number_tasks_before + 1, 'TASK WASNT SAVED IN DATABASE'
