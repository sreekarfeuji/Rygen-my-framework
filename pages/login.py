import re
import allure
from playwright.sync_api import expect
from pages.base import BasePage
from config import Base_Url


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.user_name = page.locator('input[placeholder="Enter your username or email address"]')
        self.password = page.locator('input[placeholder="Password"]')

    @allure.step("Navigate to app and enter username: {value}")
    def navigate(self, value):
        self.page.goto(Base_Url)
        self.fill(self.user_name, value)
        self.click(self.page.locator("#continue"))

    @allure.step("Enter password")
    def enter_password(self, password):
        self.fill(self.password, password)

    @allure.step("Click Sign In")
    def click_sign_in(self):
        self.click(self.page.get_by_role("button", name="Sign in"))

    @allure.step("Assert login successful")
    def is_visible(self):
        expect(self.page).to_have_url(re.compile(r"qa\.rygen\.com/corsair"), timeout=15000)

    @allure.step("Login as {username}")
    def login(self, username, password):
        self.navigate(username)
        self.enter_password(password)
        self.click_sign_in()
        self.is_visible()
