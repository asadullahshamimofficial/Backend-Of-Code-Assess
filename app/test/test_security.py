from datetime import timedelta
from jose import jwt
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token

def test_access_token_type():

    token = create_access_token({
        "sub": "1"
    })

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[
            settings.JWT_ALGORITHM
        ]
    )

    assert payload["type"] == "access"


def test_refresh_token_type():

    token = create_refresh_token({
        "sub": "1"
    })

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[
            settings.JWT_ALGORITHM
        ]
    )

    assert payload["type"] == "refresh"