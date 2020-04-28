from .pages.main_page import MainPage
from .pages.new_page import NewPage
from .main_config import Main_config
from .pages.locators import MainPageLocators, MbkpiLocators, TaskLocators, ReportLocators, CmsLocators
import time
from selenium.common.exceptions import NoSuchElementException
import os, os.path
import json
import requests
from datetime import datetime


# def test_all_content_well(browser):
#     link = "master.c1.dlr.tele2.at-consulting.ru:30467"
#     page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
#     page.open()  # открываем страницу
#     page.login()  # выполняем метод страницы - переходим на страницу логина
#     time.sleep(3)
def check_exists(browser, locator):  # функция для вывода ошибок в UI
    try:
        browser.find_element(*locator)
    except NoSuchElementException:
        return False
    return True


def test_all_content_well(browser):
    link = f"{Main_config.url}:{Main_config.port}"
    page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.login()  # выполняем метод страницы - переходим на страницу логина
    # browser.execute_script("window.scrollBy(0, 100);")
    browser.implicitly_wait(20)
    # проверяем таблицу MB_KPI на главной
    assert check_exists(browser, MainPageLocators.mbkpi_desctop_content), '!MB_KPI on desktop doesnt exist!'
    browser.implicitly_wait(20)
    browser.find_element(*MainPageLocators.button_news).click()  # открываем страницу новостей
    browser.implicitly_wait(20)
    # проверяем наличие списка новостей
    assert check_exists(browser, CmsLocators.news_list), '!news_list doesnt exist!'
    browser.implicitly_wait(10)
    # открываем страницу отчетов
    browser.find_element(*MainPageLocators.button_reports).click()
    # Проверяем наличие хотя бы одного отчета на странице
    browser.implicitly_wait(60)
    assert check_exists(browser, ReportLocators.button_download_report), '!NO any available report on the page!'
    # открываем страницу задач
    browser.find_element(*MainPageLocators.button_tasks).click()
    # Проверяем наличие хотя бы одной задачи в списке
    browser.implicitly_wait(10)
    assert check_exists(browser, TaskLocators.single_task), '!NO any available task!'


def test_mb_kpi_download(browser):
    link = f"{Main_config.url}:{Main_config.port}"
    page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.login()  # выполняем метод страницы - логинимся под дилерской учеткой
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
    file = os.path.join(home_directory, 'MB_KPI.xlsx')
    report_size = os.path.getsize(file)
    assert report_size > 0, '!MB_KPI file is empty!'
    if report_size > 0:
        os.remove(file)


def test_create_task():
    user_name = Main_config.user_name
    password = Main_config.user_password
    # Логинимся на портале через апи, получаем токен
    api_login = f'http://{Main_config.url}:{Main_config.port}/gw/public/auth/user/login'
    response = requests.post(api_login,
                             json={"username": user_name, "password": password},
                             headers={"Content-Type": "application/json"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of login is {response.status_code}'
    login = response.json()
    token = login['data']['token']

    # Запрашиваем список задач с токеном, парсим, выводи number_tasks
    api_list_tasks = f'http://{Main_config.url}:{Main_config.port}/gw/secured/task/?size=1000&page=0'
    response = requests.post(api_list_tasks,
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of request of number_tasks is {response.status_code}'

    number_tasks_before = int(response.json()['totalElements'])
    print(number_tasks_before)

    # Создаем задачу
    api_create_task = f'http://{Main_config.url}:{Main_config.port}/gw/secured/task/'
    response = requests.put(api_create_task,
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
    time.sleep(20)
    # Повторно запрашиваем список задач с токеном, парсим, выводи number_tasks
    response = requests.post(api_list_tasks,
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of request of number_tasks is {response.status_code}'

    number_tasks_after = int(response.json()['totalElements'])
    print(number_tasks_after)
    # Проверяем, что задач в базе на одну больше
    assert number_tasks_after == number_tasks_before + 1, 'TASK WASNT SAVED IN DATABASE'


def test_check_admin_roots(browser):
    # Проверяем через api видимость админки для цф
    admin_user_name = Main_config.admin_user_name
    admin_user_password = Main_config.admin_user_password
    api_login = f'http://{Main_config.url}:{Main_config.port}/gw/public/auth/user/login'
    response = requests.post(api_login,
                             json={"username": admin_user_name, "password": admin_user_password},
                             headers={"Content-Type": "application/json"})
    assert response.status_code == 200 or response.status_code == 201, f'Status code of login is {response.status_code}'
    login = response.json()
    token = login['data']['token']
    api_check_all_unclosed = f'http://{Main_config.url}:{Main_config.port}/gw/secured/task/allUnclosed/visibility'
    response = requests.get(api_check_all_unclosed,
                            headers={"Authorization": f"Bearer {token}"})
    visibility_cf = response.json()['visibility']
    print(visibility_cf)
    assert visibility_cf, f"visibility CF is {visibility_cf}, admin roots are not available " \
                          f"for {admin_user_name}, {admin_user_password}"

    # Проверяем метод для неадминских учеток
    logpass_list = {'test1@test.ru': 'test1',
                    'test2@test.ru': 'test2',
                    'test3@test.ru': 'test3',
                    'test4@test.ru': 'test4',
                    'test5@test.ru': 'test5',
                    'test6@test.ru': 'test6'
                    }

    for k, v in logpass_list.items():
        response = requests.post(api_login,
                                 json={"username": k, "password": v},
                                 headers={"Content-Type": "application/json"})
        login = response.json()
        token = login['data']['token']
        response = requests.get(api_check_all_unclosed,
                                headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200 or response.status_code == 201, f'Status code of login is {response.status_code}'
        visibility_dealer_user = response.json()['visibility']
        print(k, v, visibility_dealer_user)
        assert visibility_dealer_user == False, f" for {k},{v} admin roots are available"
    # Проверяем с фронта наличие раздела "Администрирование" у цф
    link = f"{Main_config.url}:{Main_config.port}"
    page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.login_cf()  # выполняем метод страницы - логинимся под ЦФ
    browser.implicitly_wait(30)
    assert browser.find_element(*MainPageLocators.button_administration), \
        f'! NO ADMINISTRATION on the front for {admin_user_name} , {admin_user_password}!'


def test_access_creating_article(browser):
    # Проверяем с фронта наличие раздела "Добавить новость" у цф
    link = f"{Main_config.url}:{Main_config.port}"
    page = MainPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.login_cf()  # выполняем метод страницы - логинимся под ЦФ
    browser.implicitly_wait(20)
    browser.find_element(*MainPageLocators.button_news).click()  # открываем страницу новостей
    browser.implicitly_wait(20)
    # Проверяем наличие кнопки добавления новости
    assert check_exists(browser, CmsLocators.button_add_new), "!ADDING NEWS IS NOT AVAILABLE," \
                                                              " button_add_new is not founded"
    # Проверяем, что селектор добавления новости в момент проведения теста стабилен
    assert browser.find_element(*CmsLocators.button_add_new).text == "Добавить новость", \
        "Selector button_add_new is changed now, check the page of news or ask frontend developer "
