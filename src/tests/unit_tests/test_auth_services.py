import time
from calendar import timegm
from datetime import datetime, timedelta

import pytest
from jose import jwt

from core.config import app_settings
from services.auth import create_access_token


class TestAuthService:
    def test_create_access_token(self):
        login = "test_user"
        user_id = 123
        expires_delta = timedelta(minutes=20)

        token = create_access_token(login, user_id, expires_delta)

        assert isinstance(token, str)

        decoded_token = jwt.decode(token, app_settings.jwt_secret, algorithms=app_settings.algorithm)
        assert decoded_token['sub'] == login
        assert decoded_token['id'] == user_id

        expected_expires = timegm((datetime.utcnow() + expires_delta).utctimetuple())
        assert abs(decoded_token['exp'] - expected_expires) <= 1

    def test_token_expiration(self):
        login = "test_user"
        user_id = 123
        expires_delta = timedelta(seconds=0)
        token = create_access_token(login, user_id, expires_delta)

        time.sleep(2)
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, app_settings.jwt_secret, algorithms=[app_settings.algorithm])

    def test_invalid_expires_delta(self):
        login = "test_user"
        user_id = 123
        expires_delta = "invalid_delta"
        with pytest.raises(TypeError):
            create_access_token(login, user_id, expires_delta)