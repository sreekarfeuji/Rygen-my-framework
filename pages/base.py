from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def fill(self, locator, value):
        locator.scroll_into_view_if_needed()
        if not locator.is_disabled():
            locator.fill(str(value))

    def click(self, locator):
        locator.scroll_into_view_if_needed()
        locator.click()

    def select_dropdown(self, locator, value):
        locator.scroll_into_view_if_needed()
        if not locator.is_disabled():
            locator.click()
            self.page.get_by_text(str(value), exact=False).click()

    def scroll_and_click(self, locator):
        locator.scroll_into_view_if_needed()
        locator.click()

    def is_disabled(self, locator):
        return locator.is_disabled()

    def wait(self, ms):
        self.page.wait_for_timeout(ms)

    def assert_visible(self, locator, message="Element not visible"):
        expect(locator).to_be_visible(timeout=10000)

    def assert_url_contains(self, partial_url):
        expect(self.page).to_have_url(f".*{partial_url}.*", timeout=15000)

    def assert_text_visible(self, text):
        expect(self.page.get_by_text(text, exact=False)).to_be_visible(timeout=10000)
