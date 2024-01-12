from typing import TypedDict


class TokenInfo(TypedDict):
    refreshToken: str
    accessToken: str
    expires_in: int
    user_id: str
