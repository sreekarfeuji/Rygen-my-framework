from pages.order import Order
from assertions.order_assertions import OrderAssertions

def test_create_order(logged_in, order_test_data, domain):
    order_page   = Order(logged_in)
    order_assert = OrderAssertions(order_page)

    order_page.select_domain_modal(domain)
    order_page.cancel_click()
    order_page.click_order()
    order_page.cancel_click()
    order_page.click_order(domain)
    order_page.fill_order_form(order_test_data)

    for section, section_data in order_test_data.items():
        if section.startswith("line-item"):
            order_assert.assert_line_item_totals(section_data)

    order_page.click_create_order()
    order_assert.assert_order_created()
