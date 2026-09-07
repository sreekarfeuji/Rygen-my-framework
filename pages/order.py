import re
import allure
from playwright.sync_api import expect
from pages.base import BasePage


class Order(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.order = page.locator(
            '//ul[@class="nav-list nav-list-nested"]//span[text()="Order"]'
        )

        self.new_order = page.locator(
            '//a[@href="/corsair/order/entry"]/span[@class="p-button-icon p-button-icon-right pi pi-plus"]'
        )

        self.cancel = page.locator(
            '//button[@type="button"]/span[text()="Cancel"]'
        ).first

    @allure.step("Click Order > New Order")
    def click_order(self):
        self.order.click()
        self.new_order.click()
        expect(self.page).to_have_url(re.compile(r"order/entry"), timeout=10000)

    def cancel_click(self):
        if self.cancel.count() > 0:
            self.cancel.click()

    @allure.step("Select domain: {value}")
    def select_domain_modal(self, value):
        domain = self.page.locator(
            f"//div[contains(@class,'modal-content')]//span[text()='{value}']"
        )
        self.scroll_and_click(domain)

    @allure.step("Fill section: {section}")
    def common_component(self, test_name, section, section_data):
        for field_type, fields in section_data.items():

            if field_type in ["radio-buttons", "radio_buttons"]:
                continue

            for field, value in fields.items():

                if field in ["radio-buttons", "radio_buttons"] and isinstance(value, dict):
                    from pages.test import handle_radio_buttons
                    handle_radio_buttons(self.page, section, value)
                    continue

                if isinstance(value, dict):
                    continue

                label = field.replace("_", " ")

                locator = self.page.locator(
                    f"//div[@id='{section}']//label[normalize-space()='{label}']/..//*[self::{field_type}]"
                )

                with allure.step(f"Set '{label}' = '{value}'"):
                    if field_type == "input":
                        self.fill(locator, value)
                    elif field_type == "span":
                        self.select_dropdown(locator, value)

    @allure.step("Fill basic information")
    def basic_information(
        self,
        direction=None,
        billing_terms=None,
        requested_mode=None,
        internal_notes=None,
    ):
        if direction:
            locator = self.page.locator(
                "//span[@id='direction'] | //label[normalize-space()='Direction']/..//*[self::span]"
            ).first
            self.select_dropdown(locator, direction)

        if billing_terms:
            locator = self.page.locator(
                "//span[@id='billing-terms'] | //span[@id='billing_terms'] | //label[normalize-space()='Billing Terms']/..//*[self::span]"
            ).first
            self.select_dropdown(locator, billing_terms)

    @allure.step("Submit: Create Order")
    def click_create_order(self):
        remove_btn = self.page.locator(
            "//button[contains(@class,'remove-button') and @aria-label='Remove']"
            " | //button[@aria-label='Remove']//span[contains(@class,'pi-times')]/.."
        ).first
        if remove_btn.count() > 0:
            self.scroll_and_click(remove_btn)
            self.wait(500)

        create_order_btn = self.page.locator(
            "//button[contains(@aria-label,'Create Order') or .//span[contains(text(),'Create Order')]]"
        ).first
        self.scroll_and_click(create_order_btn)

        toast = self.page.locator(".p-toast-message, .p-message, [class*='toast'], [class*='success']").first
        expect(toast).to_be_visible(timeout=15000)