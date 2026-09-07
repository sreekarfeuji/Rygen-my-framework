import allure
from pages.base import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.user_name = page.locator('input[placeholder="Enter your username or email address"]')

    @allure.step("Navigate to app and enter username: {value}")
    def navigate(self, value):
        from config import Base_Url
        self.page.goto(Base_Url)
        self.user_name.fill(value)
        self.page.locator("#continue").click()