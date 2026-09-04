import json

from playwright.sync_api import Page

from pages.order import Order
from pages.login import LoginPage
from pages.login_2 import LoginPage2


def test3(page: Page):

    k = LoginPage(page)
    m = LoginPage2(page)

    k.navigate("3PLAdminUser")

    m.enter_password("3plAdmin@2026")
    m.click_sign_in()

    z = Order(page)

    z.select_domain_modal("23")
    z.cancel_click()
    z.click_order()
    z.cancel_click()
    z.click_order()
    k = page.locator(
        "//div[@id='stop-1']//label[normalize-space()='Timezone']/..//*[self::span]"
    )