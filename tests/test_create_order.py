from pages.order import Order
def test_create_order(logged_in, order_test_data, domain):
    order_page = Order(logged_in)
    order_page.select_domain_modal(domain)
    order_page.cancel_click()
    order_page.click_order()
    order_page.cancel_click()
    order_page.click_order()
    order_page.fill_order_form(order_test_data)
    order_page.click_create_order()