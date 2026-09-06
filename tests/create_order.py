import json

from playwright.sync_api import Page

from pages.order import Order
from pages.login import LoginPage
from pages.login_2 import LoginPage2


def test2(page: Page):

    k = LoginPage(page)
    m = LoginPage2(page)

    k.navigate("3PLAdminUser")

    m.enter_password("3plAdmin@2026")
    m.click_sign_in()

    z = Order(page)

    z.select_domain_modal("JCB")
    z.cancel_click()
    z.click_order()
    z.cancel_click()
    z.click_order()  

    with open("test-data/create_order.json", "r") as file:
        test_data = json.load(file)

    for test_name, data in test_data.items():

        for section, section_data in data.items():

            if section in ["basic-information", "basic_information"]:
                z.basic_information(**section_data)
            else:
                z.common_component(
                    test_name,
                    section,
                    section_data
                )
    z.click_create_order()
    page.wait_for_timeout(1000000)