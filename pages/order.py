from playwright.sync_api import Page


class Order:

    def __init__(self, page: Page):

        self.page = page

        self.order = page.locator(
            '//ul[@class="nav-list nav-list-nested"]//span[text()="Order"]'
        )

        self.new_order = page.locator(
            '//a[@href="/corsair/order/entry"]/span[@class="p-button-icon p-button-icon-right pi pi-plus"]'
        )

        self.cancel = page.locator(
            '//button[@type="button"]/span[text()="Cancel"]'
        ).first

    def click_order(self):

        self.order.click()
        self.new_order.click()

    def cancel_click(self):

        if self.cancel.count() > 0:
            self.cancel.click()

    def select_domain_modal(self, value: str):

        self.domain = self.page.locator(
            f"//div[contains(@class,'modal-content')]//span[text()='{value}']"
        )

        self.domain.scroll_into_view_if_needed()
        self.domain.click()

    def common_component(self, test_name, section, section_data):

        for field_type, fields in section_data.items():

            # Skip top-level radio-buttons category if found
            if field_type in ["radio-buttons", "radio_buttons"]:
                print(f"[SKIP] '{field_type}' category found in JSON — skipping.")
                continue

            for field, value in fields.items():

                # Redirect radio-buttons key / dict to pages/test.py handler
                if field in ["radio-buttons", "radio_buttons"] and isinstance(value, dict):
                    from pages.test import handle_radio_buttons
                    handle_radio_buttons(self.page, section, value)
                    continue

                if isinstance(value, dict):
                    print(f"[SKIP] '{field}' found in JSON — skipping.")
                    continue


                label = field.replace("_", " ")

                print("\n----------------------------")
                print(f"Test Name : {test_name}")
                print(f"Section   : {section}")
                print(f"Type      : {field_type}")
                print(f"Field     : {label}")
                print(f"Value     : {value}")
                print("----------------------------")

                locator = self.page.locator(
                    f"//div[@id='{section}']//label[normalize-space()='{label}']/..//*[self::{field_type}]"
                )

                # Normal input
                if field_type == "input":
                    locator.scroll_into_view_if_needed()
                    if not locator.is_disabled():
                        locator.fill(str(value))
                    else:
                        print(f" [SKIP] '{label}' in '{section}' is disabled/read-only.")

                # Dropdown
                elif field_type == "span":
                    locator.scroll_into_view_if_needed()
                    if not locator.is_disabled():
                        locator.click()
                        self.page.get_by_text(str(value), exact=False).click()
                    else:
                        print(f" [SKIP] Span '{label}' in '{section}' is disabled/read-only.")


    def basic_information(
        self,
        direction: str = None,
        billing_terms: str = None,
        requested_mode: str = None,
        internal_notes: str = None,
    ):
        if direction:
            direction_locator = self.page.locator(
                "//span[@id='direction'] | //label[normalize-space()='Direction']/..//*[self::span]"
            ).first
            direction_locator.scroll_into_view_if_needed()
            direction_locator.click()
            self.page.get_by_text(direction, exact=False).click()

        if billing_terms:
            billing_locator = self.page.locator(
                "//span[@id='billing-terms'] | //span[@id='billing_terms'] | //label[normalize-space()='Billing Terms']/..//*[self::span]"
            ).first
            billing_locator.scroll_into_view_if_needed()
            billing_locator.click()
            self.page.get_by_text(billing_terms, exact=False).click()

        if requested_mode:
            mode_locator = self.page.locator(
                "//label[normalize-space()='Requested Mode']/..//*[self::span]"
            ).first
            mode_locator.scroll_into_view_if_needed()
            mode_locator.click()
            self.page.get_by_text(requested_mode, exact=False).click()

        if internal_notes:
            notes_locator = self.page.locator(
                "//label[normalize-space()='Internal Notes']/..//*[self::textarea or self::input]"
            ).first
            notes_locator.scroll_into_view_if_needed()
            notes_locator.fill(internal_notes)

    def click_create_order(self):
        # Click the remove (X) button on the reference number row if present
        remove_btn = self.page.locator(
            "//button[contains(@class,'remove-button') and @aria-label='Remove']"
            " | //button[@aria-label='Remove']//span[contains(@class,'pi-times')]/.."
        ).first
        if remove_btn.count() > 0:
            remove_btn.scroll_into_view_if_needed()
            remove_btn.click()
            self.page.wait_for_timeout(500)

        create_order_btn = self.page.locator(
            "//button[contains(@aria-label,'Create Order') or .//span[contains(text(),'Create Order')]]"
        ).first
        create_order_btn.scroll_into_view_if_needed()
        create_order_btn.click()