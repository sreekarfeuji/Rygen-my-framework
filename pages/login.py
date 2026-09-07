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
    def login(self, username, password, max_retries=2):
        for attempt in range(1, max_retries + 1):
            try:
                self.navigate(username)
                self.enter_password(password)
                self.click_sign_in()
                self.is_visible()
                return
            except Exception as e:
                if attempt < max_retries:
                    print(f"[Attempt {attempt}/{max_retries}] Login failed. Retrying...")
                    self.page.reload()
                else:
                    try:
                        allure.attach(
                            self.page.screenshot(full_page=True),
                            name="login_failure_screenshot",
                            attachment_type=allure.attachment_type.PNG,
                        )
                    except Exception as screenshot_err:
                        print(f"Failed to capture login failure screenshot: {screenshot_err}")
                    raise e


