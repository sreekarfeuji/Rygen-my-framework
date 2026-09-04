from playwright.sync_api import Page
from pages.login import LoginPage
from pages.login_2 import LoginPage2
def test1(page:Page):
    k = LoginPage(page)
    m = LoginPage2(page)
    k.navigate()
    k.fill("3PLAdminUser")
    k.continue_click()
    m.enter_password("3plAdmin@2026")
    m.click_sign_in()
    m.is_visible()
    