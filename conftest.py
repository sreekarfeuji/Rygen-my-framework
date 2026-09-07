import pytest
from playwright.sync_api import Page

from pages.login import LoginPage
from config import USERNAME, PASSWORD


@pytest.fixture
def logged_in(page: Page):
    login = LoginPage(page)
    login.login(USERNAME, PASSWORD)
    yield page
