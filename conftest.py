import pytest
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach
from utils.config import selenoid_url, selenoid_login, selenoid_pass


DEFAULT_BROWSER_VERSION = "100.0"


def pytest_addoption(parser):
    parser.addoption("--browser_version", default=DEFAULT_BROWSER_VERSION)


@pytest.fixture(scope="session")
def setup_browser(request):
    browser_version = request.config.getoption("--browser_version")
    browser_version = (
        browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    )
    browser.config.base_url = "https://demoqa.com/automation-practice-form"
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = "eager"
    browser.config.driver_options = driver_options  # чтоб тест выполнялся когда сайт продолжается грузиться , но html загрузился
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    # driver_options = webdriver.ChromeOptions()   #настройка чтоб не открывать браузер , надо для этого 8 , 10 строчку кода
    # driver_options.add_argument('--headless')

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {"enableVNC": True, "enableVideo": True},
    }

    options.capabilities.update(selenoid_capabilities)
    browser.config.driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options,
    )

    yield browser
    browser.quit()


@pytest.fixture(scope="function", autouse=True)
def teardown_browser():
    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)
