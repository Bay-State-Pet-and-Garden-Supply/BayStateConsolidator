import re
from typing import Optional
from quantulum3 import parser


def normalize_text(text: Optional[str]) -> str:
    """
    Standardizes text to lowercase, single spaces.
    """
    if not text:
        return ""

    # Lowercase and strip
    text = text.lower().strip()
    # Replace multiple spaces with single space
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_weight(text: Optional[str]) -> Optional[str]:
    """
    Extracts weight and normalizes to canonical units (lb, oz).
    Returns formatted string "X lb" or "Y oz" or None.
    """
    if not text:
        return None

    try:
        quants = parser.parse(text)
        for quant in quants:
            unit_name = quant.unit.name.lower()
            if "pound" in unit_name or "lb" in unit_name:
                return f"{quant.value} lb"
            elif "ounce" in unit_name or "oz" in unit_name:
                return f"{quant.value} oz"
            elif "kilogram" in unit_name:
                # Convert kg to lb
                lbs = quant.value * 2.20462
                return f"{lbs:.2f} lb"
            elif "gram" in unit_name:
                # Convert g to oz
                oz = quant.value * 0.035274
                return f"{oz:.2f} oz"
    except Exception:
        return None

    return None
