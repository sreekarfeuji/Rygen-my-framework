import re
from playwright.sync_api import Page, expect
class BasePage:
    def __init__(self, page: Page):
        self.page = page
    def click(self, locator):
        locator.scroll_into_view_if_needed()
        locator.click()
    def fill(self, locator, value):
        locator.scroll_into_view_if_needed()
        if not locator.is_disabled():
            locator.fill(str(value))
    def select_dropdown(self, locator, value):
        locator.scroll_into_view_if_needed()
        if not locator.is_disabled():
            locator.click()
            self.page.get_by_text(str(value), exact=False).click()
    def wait(self, ms):
        self.page.wait_for_timeout(ms)
    def assert_visible(self, locator, message="Element not visible"):
        expect(locator).to_be_visible(timeout=10000)
    def assert_hidden(self, locator):
        expect(locator).to_be_hidden(timeout=10000)
    def assert_value(self, locator, expected_value):
        expect(locator).to_have_value(str(expected_value), timeout=10000)
    def assert_class_contains(self, locator, class_fragment):
        expect(locator).to_have_class(re.compile(class_fragment), timeout=10000)
    def assert_text_contains(self, locator, text_fragment):
        expect(locator).to_contain_text(re.compile(text_fragment, re.IGNORECASE), timeout=10000)

    def assert_url_contains(self, partial_url):
        expect(self.page).to_have_url(re.compile(f".*{re.escape(partial_url)}.*"), timeout=15000)

    def assert_text_visible(self, text):
        expect(self.page.get_by_text(text, exact=False)).to_be_visible(timeout=10000)
    def assert_title(self, title):
        expect(self.page).to_have_title(title, timeout=10000)