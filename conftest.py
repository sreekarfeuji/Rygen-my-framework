import logging
import configparser
import json
from pathlib import Path
import allure
import pytest
from playwright.sync_api import Page

from pages.login import LoginPage
from utils.data_loader import DataLoader

logger = logging.getLogger(__name__)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    try:
        if page.is_closed():
            return
        screenshot = page.screenshot(full_page=True, timeout=10000)
        allure.attach(
            screenshot,
            name=f"Failure screenshot - {item.name} - {report.when}",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        logger.exception("Could not attach failure screenshot for %s", item.nodeid)


PROJECT_ROOT = Path(__file__).resolve().parent
config = configparser.ConfigParser()
with (PROJECT_ROOT / "config.ini").open(encoding="utf-8") as file:
    config.read_file(file)

USERNAME = config["DEFAULT"]["USERNAME"]
PASSWORD = config["DEFAULT"]["PASSWORD"]
DOMAIN = config["DEFAULT"]["DOMAIN"]
BASE_URL = config["DEFAULT"]["Base_Url"]

@pytest.fixture
def logged_in(page: Page):
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.login(USERNAME, PASSWORD)
    yield page
@pytest.fixture
def domain():
    return DOMAIN
ORDER_DATA_PATH = PROJECT_ROOT / "test-data" / "create_order.json"
ORDER_SCENARIOS = tuple(json.loads(ORDER_DATA_PATH.read_text(encoding="utf-8")))
@pytest.fixture(params=ORDER_SCENARIOS, ids=ORDER_SCENARIOS)
def order_test_data(request):
    logger.info("Loading scenario: %s", request.param)
    data = DataLoader.load_json(ORDER_DATA_PATH)
    return data[request.param]
