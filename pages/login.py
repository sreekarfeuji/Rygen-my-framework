from playwright.sync_api import Page, expect
from config import Base_Url 
class LoginPage:
    def __init__(self,page):
        self.page = page
        self.user_name = page.locator('input[placeholder="Enter your username or email address"]')
    def navigate(self,value):
        self.page.goto(Base_Url)
        self.user_name.fill(value)  
        self.page.locator("#continue").click()
    