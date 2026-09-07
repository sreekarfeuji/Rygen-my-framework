from playwright.sync_api import Page


def handle_radio_buttons(page: Page, section: str, radio_data: dict):
    for field, value in radio_data.items():
        if str(value).lower() == "yes":
            label = field.replace("_", " ")
            locator = page.locator(
                f"//div[@id='{section}']//label[text()='{label}']/..//input"
            )
            locator.click(force=True)
