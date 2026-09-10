import configparser
import pytest
from playwright.sync_api import Page

from pages.login import LoginPage
from pages.data_loader import DataLoader

config = configparser.ConfigParser()
config.read("config.ini")

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


@pytest.fixture
def order_test_data():
    data = DataLoader.load_json("test-data/create_order.json")
    return next(iter(data.values()))