from playwright.sync_api import Page, expect
class LoginPage2:
    def __init__(self,page):
        self.page = page
        self.password = page.locator('input[placeholder="Password"]')
        self.submit = page.locator('')
    def enter_password(self,password):
        self.password.fill(password)
    def click_sign_in(self):
        self.page.get_by_role("button",name = "Sign in").click()
    def is_visible(self):
        expect(self.page).to_have_url("https://qa.rygen.com/corsair/")
        print("Login successful. Current URL:", self.page.url)
