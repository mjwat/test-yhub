from typing import Optional


def build_url(base_url: str, path: str) -> str:
    normalized_base_url = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{normalized_base_url}{normalized_path}"


def normalize_url_for_match(url: Optional[str]) -> str:
    if url is None:
        return ""
    return url.lower().rstrip("/")


def url_contains_expected(actual_url: str, expected_url_part: str) -> bool:
    normalized_actual = normalize_url_for_match(actual_url)
    normalized_expected = normalize_url_for_match(expected_url_part)
    return bool(normalized_expected) and normalized_expected in normalized_actual
