from playwright.sync_api import Page


def handle_radio_buttons(page: Page, section: str, radio_data: dict):
    """
    Dynamically handles radio buttons/toggles.
    If the value in test data is 'Yes', it locates the button and clicks it.
    """
    for field, value in radio_data.items():
        if str(value).lower() == "yes":
            label = field.replace("_", " ")
            print(f" [RADIO] Clicking '{label}' in section '{section}'")
            
            locator = page.locator(
                f"//div[@id='{section}']//label[text()='{label}']/..//input"
            )
            
            # Click the radio/toggle input
            locator.click(force=True)
