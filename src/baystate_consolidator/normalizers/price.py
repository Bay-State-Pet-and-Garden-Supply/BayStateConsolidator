from typing import Optional, Union
from price_parser import Price


def normalize_price(raw: Union[str, float, int, None]) -> Optional[float]:
    """
    Extracts a float price from a string or number using price-parser.
    Returns None if no valid price is found.
    """
    if raw is None:
        return None

    if isinstance(raw, (float, int)):
        return float(raw)

    if not isinstance(raw, str) or not raw.strip():
        return None

    try:
        price = Price.fromstring(raw)
        if price.amount is not None:
            return float(price.amount)
    except Exception:
        return None

    return None
