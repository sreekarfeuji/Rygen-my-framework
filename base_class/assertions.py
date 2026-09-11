import math
import allure


class OrderAssertions:

    def __init__(self, order_page):
        self.order = order_page

    @staticmethod
    def _compute_line_item_totals(inp: dict) -> dict:
        length      = float(inp.get("Length",      0))
        width       = float(inp.get("Width",       0))
        height      = float(inp.get("Height",      0))
        weight      = float(inp.get("Weight",      0))
        linear_feet = float(inp.get("Linear_Feet", 0))
        handling    = int(float(inp.get("Handling", 0)))

        per_pallet_ft3 = (length * width * height) / 1728
        cubic_feet     = math.floor(per_pallet_ft3 * handling * 100) / 100

        return {
            "cubic_feet":   cubic_feet,
            "total_weight": weight,
            "linear_feet":  linear_feet,
            "handling":     handling,
        }

    @allure.step("Assert line item aggregate tiles match computed values")
    def assert_line_item_totals(self, section_data: dict):
        inp      = section_data.get("input", {})
        expected = self._compute_line_item_totals(inp)

        with allure.step(f"Total Weight tile = {expected['total_weight']} lbs"):
            self.order.assert_text_contains(
                self.order.tile_total_weight, str(int(expected["total_weight"]))
            )

        with allure.step(f"Linear Feet tile = {expected['linear_feet']} ft"):
            self.order.assert_text_contains(
                self.order.tile_linear_feet, str(expected["linear_feet"])
            )

        with allure.step(f"Cubic Feet tile = {expected['cubic_feet']} ft³"):
            self.order.assert_text_contains(
                self.order.tile_cubic_feet, str(expected["cubic_feet"])
            )

        with allure.step(f"Total Handling Units tile = {expected['handling']}"):
            self.order.assert_text_contains(
                self.order.tile_total_handling, str(expected["handling"])
            )
