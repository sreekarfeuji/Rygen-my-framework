import allure
from playwright.sync_api import Page
from base_class.base_page import BasePage


class Order(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.order = page.locator('//ul[@class="nav-list nav-list-nested"]//span[text()="Order"]')
        self.new_order = page.locator('//span[text()="New Order"]')
        self.cancel = page.locator('//button[@type="button"]/span[text()="Cancel"]').first
        self.domain_option = lambda value: page.locator(f"//div[contains(@class,'modal-content')]//span[text()='{value}']")
        self.assigned_to = lambda value: page.locator(f"//button[contains(@class,'p-button')]//span[contains(@class,'p-button-label') and normalize-space()='Assigned to {value}']")
        self.radio_input = lambda section, label: page.locator(f"//div[@id='{section}']//label[normalize-space()='{label}']/..//input")
        self.section_field = lambda section, field_type, label: page.locator(f"//div[@id='{section}']//label[normalize-space()='{label}']/..//*[self::{field_type}]")
        self.direction = page.locator("#direction")
        self.billing_terms = page.locator("#billing-terms")
        self.requested_mode = page.locator("#requested-mode")
        self.internal_notes = page.locator("#internal-notes")
        self.remove_btn = page.locator(
            "//button[contains(@class,'remove-button') and @aria-label='Remove'] "
            "| //button[@aria-label='Remove']//span[contains(@class,'pi-times')]/.."
        ).first
        self.create_order_btn = page.locator("//button[contains(@aria-label,'Create Order') or .//span[contains(text(),'Create Order')]]")
        self.success_toast = page.locator(".p-toast-message-success")
        self.input_errors = page.locator(".input-error-msg:visible")
        self.submit_result = page.locator(".input-error-msg:visible, .p-toast-message-success:visible")
        self.tile_total_packaging = page.locator("//span[normalize-space()='Total Packaging Units']/preceding-sibling::span[1]")
        self.tile_total_handling = page.locator("//span[normalize-space()='Total Handling Units']/preceding-sibling::span[1]")
        self.tile_total_weight = page.locator("//span[normalize-space()='Total Weight']/preceding-sibling::span[1]")
        self.tile_linear_feet = page.locator("//span[normalize-space()='Linear Feet']/preceding-sibling::span[1]")
        self.tile_cubic_feet = page.locator("//span[normalize-space()='Cubic Feet']/preceding-sibling::span[1]")

    @allure.step("Click Order > New Order")
    def click_order(self, domain=None):
        self.click(self.order)
        self.click(self.new_order)
        self.assert_url_contains(r"order/entry")
        if domain:
            self.assert_visible(self.assigned_to(domain))

    def cancel_click(self):
        if self.cancel.count() > 0:
            self.click(self.cancel)

    @allure.step("Select domain: {value}")
    def select_domain_modal(self, value):
        self.click(self.domain_option(value))

    def handle_radio_buttons(self, section, radio_data):
        for field, value in radio_data.items():
            if str(value).lower() == "yes":
                label = field.replace("_", " ")
                self.radio_input(section, label).click(force=True)

    @allure.step("Fill section: {section}")
    def common_component(self, section, section_data):
        for field_type, fields in section_data.items():
            for field, value in fields.items():
                if field == "radio-buttons" and isinstance(value, dict):
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
    def basic_information(self, direction=None, billing_terms=None, requested_mode=None, internal_notes=None):
        if direction:
            self.select_dropdown(self.direction, direction)
        if billing_terms:
            self.select_dropdown(self.billing_terms, billing_terms)
        if requested_mode:
            self.select_dropdown(self.requested_mode, requested_mode)
        if internal_notes:
            self.fill(self.internal_notes, internal_notes)

    @allure.step("Fill order form using test data")
    def fill_order_form(self, data):
        for section, section_data in data.items():
            if section == "basic-information":
                self.basic_information(**section_data)
            else:
                self.common_component(section, section_data)


    @allure.step("Submit: Create Order")
    def click_create_order(self):
        if self.remove_btn.count() > 0:
            self.click(self.remove_btn)
            self.assert_hidden(self.remove_btn)  # wait for removal to complete
        self.click(self.create_order_btn)
        self.submit_result.first.wait_for(state="visible", timeout=10000)
