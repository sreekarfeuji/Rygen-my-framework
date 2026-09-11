import logging
import configparser
import json
from pathlib import Path
import pytest
from playwright.sync_api import Page

from pages.login import LoginPage
from utils.data_loader import DataLoader

logger = logging.getLogger(__name__)


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
