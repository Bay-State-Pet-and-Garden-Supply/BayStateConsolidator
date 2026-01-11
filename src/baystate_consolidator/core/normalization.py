import re
from typing import Dict, Any, List, Optional
from baystate_consolidator.models.golden_record import GoldenRecord, FieldMetadata


def to_title_case_preserve_brand(text: str) -> str:
    words = text.split(" ")
    result = []
    for word in words:
        if not word:
            result.append(word)
            continue
        alpha = re.sub(r"[^a-zA-Z]", "", word)
        is_all_caps = len(alpha) > 1 and alpha == alpha.upper()
        if is_all_caps:
            result.append(word)
        else:
            result.append(word.capitalize())
    return " ".join(result)


def normalize_units(text: str) -> str:
    replacements = [
        (r"\b(lbs?\.?)\b", "lb", re.IGNORECASE),
        (r"\b(pounds?)\b", "lb", re.IGNORECASE),
        (r"\b(ounces?|oz\.?)\b", "oz", re.IGNORECASE),
        (r"\b(count|ct\.?)\b", "ct", re.IGNORECASE),
        (r"\b(feet|ft\.?)\b", "ft", re.IGNORECASE),
        (r"\b(inches?|in\.?)\b", "in", re.IGNORECASE),
        (r'"', " in "),
        (r"\b(liters?|l\.?)\b", "L", re.IGNORECASE),
    ]
    output = text
    for pattern, repl, flags in replacements:
        output = re.sub(pattern, repl, output, flags=flags)
    return output


def normalize_dimensions(text: str) -> str:
    # Normalize dimensions only when X is between numbers
    output = re.sub(r"(?<=\d)\s*[xX]\s*(?=\d)", " X ", text)
    # Normalize multiple spaces
    output = re.sub(r"\s{2,}", " ", output)
    return output


def ensure_inches_spacing(text: str) -> str:
    return re.sub(r"(\d+)\s*in\s*X\s*(\d+)\s*in", r"\1 X \2 in", text, flags=re.IGNORECASE)


def normalize_decimals(text: str) -> str:
    def replacer(match):
        num_str = match.group(1)
        try:
            num = float(num_str)
            fixed = f"{num:.2f}"
            trimmed = re.sub(r"\.0+$", "", fixed)
            trimmed = re.sub(r"\.([0-9]*[1-9])0+$", r".\1", trimmed)
            return trimmed
        except ValueError:
            return num_str

    return re.sub(r"(\d+\.\d+|\d+)(?=\s?(lb|oz|ct|in|ft|L)\b)", replacer, text, flags=re.IGNORECASE)


def strip_trailing_unit_periods(text: str) -> str:
    return re.sub(r"\b(lb|oz|ct|in|ft|L)\.", r"\1", text, flags=re.IGNORECASE)


def normalize_unit_casing(text: str) -> str:
    replacements = [
        (r"\b(LB)\b", "lb"),
        (r"\b(OZ)\b", "oz"),
        (r"\b(CT)\b", "ct"),
        (r"\b(FT)\b", "ft"),
        (r"\b(IN)\b", "in"),
        (r"\b(l)\b", "L"),
        (r"\b(Lb)\b", "lb"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    return text


def normalize_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([X&])", r" \1", text)
    text = re.sub(r"([X&])\s+", r"\1 ", text)
    return text.strip()


def normalize_consolidation_result(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = data.copy()

    if isinstance(normalized.get("name"), str):
        name = normalized["name"]
        name = normalize_dimensions(name)
        name = normalize_units(name)
        name = normalize_decimals(name)
        name = strip_trailing_unit_periods(name)
        name = normalize_unit_casing(name)
        name = ensure_inches_spacing(name)
        name = normalize_spacing(name)
        name = to_title_case_preserve_brand(name)
        # Re-assert canonical units after title case
        name = normalize_unit_casing(normalize_units(name))
        name = strip_trailing_unit_periods(name)
        name = ensure_inches_spacing(name)
        name = normalize_spacing(name)
        normalized["name"] = name

    if isinstance(normalized.get("weight"), str):
        try:
            weight_num = float(normalized["weight"])
            normalized["weight"] = str(
                weight_num
            )  # Trim trailing zeros handled by float->str usually enough
            if normalized["weight"].endswith(".0"):
                normalized["weight"] = normalized["weight"][:-2]
        except ValueError:
            pass

    return normalized


class SurvivorshipEngine:
    def apply(
        self, records: List[Dict[str, Any]], excel_price: Optional[float] = None
    ) -> GoldenRecord:
        # Simplistic merge preferring last record
        merged = {}
        for record in records:
            merged.update(record)

        if excel_price is not None:
            merged["price"] = excel_price

        # Ensure required fields are present or handle gracefully
        # This is a stub for the full logic
        if "sku" not in merged:
            merged["sku"] = "UNKNOWN"
        if "name" not in merged:
            merged["name"] = "Unknown Product"
        if "price" not in merged:
            merged["price"] = 0.0

        return GoldenRecord(**merged)
