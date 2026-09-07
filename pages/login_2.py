import re
import allure
from playwright.sync_api import expect
from pages.base import BasePage


class LoginPage2(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.password = page.locator('input[placeholder="Password"]')

    @allure.step("Enter password")
    def enter_password(self, password):
        self.password.fill(password)

    @allure.step("Click Sign In")
    def click_sign_in(self):
        self.page.get_by_role("button", name="Sign in").click()

    @allure.step("Assert login successful")
    def is_visible(self):
        expect(self.page).to_have_url(re.compile(r"qa\.rygen\.com/corsair"), timeout=15000)
