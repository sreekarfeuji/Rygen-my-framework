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

            for field, value in fields.items():

                if not value:
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
                    f"//div[@id='{section}']//label[text()='{label}']/..//*[self::span or self::input]"
                )
                tag_name = locator.evaluate("(el) => el.tagName")
                print(tag_name)
                if tag_name == "INPUT":
                    locator.fill(str(value))
                else:
                    locator.click()
                    self.page.wait_for_timeout(10000)
                    self.page.get_by_text(str(value), exact=True).last.click()
                self.page.keyboard.press("Escape")
                print(f"COMPLETED: {label}")