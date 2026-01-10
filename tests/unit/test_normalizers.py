import pytest
from baystate_consolidator.normalizers.price import normalize_price
from baystate_consolidator.normalizers.text import normalize_text, normalize_weight


class TestPriceNormalizer:
    def test_simple_price(self):
        assert normalize_price("$10.00") == 10.00
        assert normalize_price("10.50") == 10.50

    def test_currency_symbol(self):
        assert normalize_price("USD 10.99") == 10.99
        assert normalize_price("€5.00") == 5.00

    def test_floats(self):
        assert normalize_price(15.5) == 15.5
        assert normalize_price(10) == 10.0

    def test_invalid_input(self):
        assert normalize_price(None) is None
        assert normalize_price("Not a price") is None
        assert normalize_price("") is None


class TestTextNormalizer:
    def test_clean_text(self):
        assert normalize_text("  Hello World  ") == "hello world"
        assert normalize_text("TiTle Case") == "title case"
        assert normalize_text("Foo   Bar") == "foo bar"

    def test_empty(self):
        assert normalize_text(None) == ""
        assert normalize_text("") == ""


class TestWeightNormalizer:
    def test_lb_conversion(self):
        assert normalize_weight("10 lbs") == "10.0 lb"
        assert normalize_weight("5 POUNDS") == "5.0 lb"

    def test_oz_conversion(self):
        assert normalize_weight("16 oz") == "16.0 oz"
        assert normalize_weight("16 ounces") == "16.0 oz"

    def test_kg_to_lb(self):
        # 1 kg approx 2.2 lb
        result = normalize_weight("1 kg")
        assert result is not None
        assert "lb" in result

    def test_no_unit(self):
        assert normalize_weight("10") is None
        assert normalize_weight("heavy object") is None
