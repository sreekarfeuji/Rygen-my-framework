import json
import random
import allure
from playwright.sync_api import Page
from pages.order import Order
from config import DOMAIN
def test2(logged_in: Page):
    order = Order(logged_in)
    order.select_domain_modal(DOMAIN)
    order.cancel_click()
    order.click_order()
    order.cancel_click()
    order.click_order()
    with open("test-data/create_order.json", "r") as file:
        test_data = json.load(file)
    suffix = random.randint(10000, 99999)
    for test_name, data in test_data.items():
        allure.dynamic.title(f"Order Test: {test_name}")
        for section, section_data in data.items():
            if "input" in section_data and "Location_Code" in section_data["input"]:
                section_data["input"]["Location_Code"] = f"{section_data['input']['Location_Code']}_{suffix}"
            if section in ["basic-information"]:
                order.basic_information(**section_data)
            else:
                order.common_component(test_name, section, section_data)
    order.click_create_order()
    logged_in.wait_for_timeout(10000)
