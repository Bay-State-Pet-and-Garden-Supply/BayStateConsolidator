import pytest
from baystate_consolidator.core.normalization import to_title_case_preserve_brand, normalize_units


def test_title_case():
    assert to_title_case_preserve_brand("DOG FOOD") == "Dog Food"
    assert to_title_case_preserve_brand("ACANA Dog Food") == "ACANA Dog Food"


def test_normalize_units():
    assert normalize_units("10 lbs") == "10 lb"
    assert normalize_units("5 oz.") == "5 oz"
    assert normalize_units("10lbs") == "10 lb"
