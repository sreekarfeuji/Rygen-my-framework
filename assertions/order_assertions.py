import math
import re
from decimal import Decimal, ROUND_HALF_UP
import allure
from playwright.sync_api import expect


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

    @staticmethod
    def _total_pattern(expected, unit="", allow_whole_number=False):
        number = Decimal(str(expected))
        values = [number]
        if allow_whole_number:
            values.append(number.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

        patterns = []
        for value in values:
            text = format(value, "f")
            if "." in text:
                text = text.rstrip("0").rstrip(".")
            integer, dot, fraction = text.partition(".")
            grouped = format(int(integer), ",")
            integer_pattern = rf"(?:{re.escape(integer)}|{re.escape(grouped)})"
            decimal_pattern = rf"\.{fraction}0*" if dot else r"(?:\.0+)?"
            patterns.append(integer_pattern + decimal_pattern)

        return re.compile(rf"^\s*(?:{'|'.join(patterns)})\s*{re.escape(unit)}\s*$")

    @allure.step("Assert line item aggregate tiles match computed values")
    def assert_line_item_totals(self, section_data: dict):
        expected = self._compute_line_item_totals(section_data.get("input", {}))
        tiles = (
            ("Total Weight", self.order.tile_total_weight, "total_weight", "lbs"),
            ("Linear Feet", self.order.tile_linear_feet, "linear_feet", "ft"),
            ("Cubic Feet", self.order.tile_cubic_feet, "cubic_feet", "ft\u00b3"),
            ("Total Handling Units", self.order.tile_total_handling, "handling", ""),
        )
        for name, locator, key, unit in tiles:
            with allure.step(f"{name} tile = {expected[key]} {unit}"):
                pattern = self._total_pattern(
                    expected[key], unit, allow_whole_number=key == "cubic_feet"
                )
                expect(locator).to_have_text(pattern, timeout=10000)

    @allure.step("Assert order submission has no field errors")
    def assert_order_created(self):
        messages = []
        for error in self.order.input_errors.all():
            message = error.inner_text().strip()
            label = error.locator("xpath=ancestor::*[.//label][1]").locator("label").first
            field = label.inner_text().strip() if label.count() else ""
            messages.append(f"{field}: {message}" if field else message or "Unlabeled field error")

        if messages:
            details = "Mandatory fields missing or invalid:\n" + "\n".join(messages)
            print(details)
            raise AssertionError(details)

        self.order.assert_visible(self.order.success_toast)
        self.order.assert_text_contains(self.order.success_toast, "success")
