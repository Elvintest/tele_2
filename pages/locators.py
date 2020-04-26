from selenium.webdriver.common.by import By


class MainPageLocators():
    button_news = (By.CSS_SELECTOR, "[href='/app/news']")
    mbkpi_desctop_content = (By.CLASS_NAME, "recharts-responsive-container")
    button_reports = (By.CSS_SELECTOR, "[href='/app/report']")
    no_data_message = (By.CLASS_NAME, "cap__text")
    button_tasks = (By.CSS_SELECTOR, "[href='/app/tasks']")
    button_mb_kpi = (By.CSS_SELECTOR, "[href='/app/retail-control']")
    button_administration = (By.CSS_SELECTOR,"[href='/app/admin']")

class MbkpiLocators():
    button_mb_kpi = (By.CSS_SELECTOR, "[href='/app/retail-control']")
    button_mb_kpi_download = (By.CSS_SELECTOR, "div.card__content > div > div > button:nth-child(2)")
    button_download_ready_report = (By.CSS_SELECTOR, "[title='Скачать отчет']")
    button_close_report = (By .CSS_SELECTOR, "[title='Удалить']")


class TaskLocators():
    button_tasks = (By.CSS_SELECTOR, "[href='/app/tasks']")
    single_task = (By.CLASS_NAME, "task")


class ReportLocators():
    button_download_report = (By.CLASS_NAME, "btn.button-icon.btn.report__download")
    button_download_ready_report = (By.CSS_SELECTOR, "[title='Скачать отчет']")
    button_close_report = (By.CSS_SELECTOR, "[title='Удалить']")

class CmsLocators():
    news_list = (By.CLASS_NAME, "news-list")
    button_add_new = (By.CSS_SELECTOR,".top-bar__children>button>span")