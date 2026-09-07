import re
import allure
from playwright.sync_api import expect
from pages.base import BasePage
class Order(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.order = page.locator('//ul[@class="nav-list nav-list-nested"]//span[text()="Order"]')
        self.new_order = page.locator('//span[text()="New Order"]')
        self.cancel = page.locator('//button[@type="button"]/span[text()="Cancel"]').first
        self.domain_option = lambda value: page.locator(f"//div[contains(@class,'modal-content')]//span[text()='{value}']")
        self.radio_input = lambda section, label: page.locator(f"//div[@id='{section}']//label[text()='{label}']/..//input")
        self.section_field = lambda section, field_type, label: page.locator(f"//div[@id='{section}']//label[normalize-space()='{label}']/..//*[self::{field_type}]")
        self.direction = page.locator("#direction")
        self.billing_terms = page.locator("#billing-terms")
        self.remove_btn = page.locator("//button[contains(@class,'remove-button') and @aria-label='Remove'] | //button[@aria-label='Remove']//span[contains(@class,'pi-times')]/..")
        self.create_order_btn = page.locator("//button[contains(@aria-label,'Create Order') or .//span[contains(text(),'Create Order')]]")
        self.toast = page.locator(".p-toast-message, .p-message, [class*='toast'], [class*='success']")
    @allure.step("Click Order > New Order")
    def click_order(self):
        self.click(self.order)
        self.click(self.new_order)
        expect(self.page).to_have_url(re.compile(r"order/entry"), timeout=10000)
    def cancel_click(self):
        if self.cancel.count() > 0:
            self.click(self.cancel)
    @allure.step("Select domain: {value}")
    def select_domain_modal(self, value):
        self.scroll_and_click(self.domain_option(value))
    def handle_radio_buttons(self, section, radio_data):
        for field, value in radio_data.items():
            if str(value).lower() == "yes":
                label = field.replace("_", " ")
                self.radio_input(section, label).click(force=True)
    @allure.step("Fill section: {section}")
    def common_component(self, test_name, section, section_data):
        for field_type, fields in section_data.items():
            if field_type in ["radio-buttons", "radio_buttons"]:
                continue
            for field, value in fields.items():
                if field in ["radio-buttons"] and isinstance(value, dict):
                    self.handle_radio_buttons(section, value)
                    continue
                if isinstance(value, dict):
                    continue
                label = field.replace("_", " ")
                locator = self.section_field(section, field_type, label)
                with allure.step(f"Set '{label}' = '{value}'"):
                    if field_type == "input":
                        self.fill(locator, value)
                    elif field_type == "span":
                        self.select_dropdown(locator, value)

    @allure.step("Fill basic information")
    def basic_information(self,direction=None,billing_terms=None,requested_mode=None,internal_notes=None,):
        if direction:
            self.select_dropdown(self.direction, direction)

        if billing_terms:
            self.select_dropdown(self.billing_terms, billing_terms)

    @allure.step("Submit: Create Order")
    def click_create_order(self):
        if self.remove_btn.count() > 0:
            self.scroll_and_click(self.remove_btn)
            self.wait(500)

        self.scroll_and_click(self.create_order_btn)
