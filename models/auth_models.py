from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LoginResponse:
    access_token: str
    token_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoginResponse":
        access_token = data.get("access_token")
        token_type = data.get("token_type")

        if not isinstance(access_token, str) or not access_token.strip():
            raise ValueError("Response field 'access_token' must be a non-empty string.")

        if token_type is not None and not isinstance(token_type, str):
            raise ValueError("Response field 'token_type' must be a string when provided.")

        return cls(access_token=access_token, token_type=token_type)
