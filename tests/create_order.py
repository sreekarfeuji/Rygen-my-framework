import json

import allure
from playwright.sync_api import Page

from pages.order import Order
from pages.login import LoginPage
from pages.login_2 import LoginPage2
from config import USERNAME, PASSWORD, DOMAIN


def test2(page: Page):

    k = LoginPage(page)
    m = LoginPage2(page)

    k.navigate(USERNAME)
    m.enter_password(PASSWORD)
    m.click_sign_in()
    m.is_visible()

    z = Order(page)

    z.select_domain_modal(DOMAIN)
    z.cancel_click()
    z.click_order()
    z.cancel_click()
    z.click_order()

    with open("test-data/create_order.json", "r") as file:
        test_data = json.load(file)
    import random
    suffix = random.randint(10000, 99999)
    for test_name, data in test_data.items():
        allure.dynamic.title(f"Order Test: {test_name}")
        for section, section_data in data.items():
            if "input" in section_data and "Location_Code" in section_data["input"]:
                section_data["input"]["Location_Code"] = f"{section_data['input']['Location_Code']}_{suffix}"
            if section in ["basic-information", "basic_information"]:
                z.basic_information(**section_data)
            else:
                z.common_component(test_name, section, section_data)
    z.click_create_order()
    page.wait_for_timeout(100000000)