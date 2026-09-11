import logging
import allure
from playwright.sync_api import Page
from base_class.base_page import BasePage


logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#signInName")
        self.continue_btn = page.locator("#continue")
        self.password_input = page.locator("#password")
        self.signin_btn = page.locator("#next")
        self.dashboard_marker = page.get_by_text("Select a Domain")

    @allure.step("Login as {username}")
    def login(self, username, password):
        logger.info("Login started")
        self.fill(self.username_input, username)
        self.assert_value(self.username_input, username)  # verify before page transitions
        self.click(self.continue_btn)
        self.assert_visible(self.password_input)
        self.fill(self.password_input, password)
        self.click(self.signin_btn)
        self.assert_visible(
            self.dashboard_marker,
            "Login did not reach 'Select a Domain' within 30 seconds. "
            "Check whether the login redirect completed and the account session loaded.",
            timeout=30000,
        )
        logger.info("Login completed; domain selector visible")
