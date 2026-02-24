def build_url(base_url: str, path: str) -> str:
    normalized_base_url = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{normalized_base_url}{normalized_path}"
