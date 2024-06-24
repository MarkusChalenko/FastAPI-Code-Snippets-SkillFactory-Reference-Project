from unittest.mock import AsyncMock, Mock
from contextlib import nullcontext as does_not_raise
import pytest
from fastapi import HTTPException
from starlette import status

from schemas.user import UserUpdate
from services.user import get_user_by_id, create_new_user, update_user, delete_user
from unittest.mock import patch


class TestUserService:
    @pytest.mark.parametrize(
        "test_user_id, expectation",
        [
            (1, does_not_raise()),
            ("1", pytest.raises(AssertionError))
        ]
    )
    async def test_get_user_by_id(self, user_test_data, test_user_id, expectation):
        with expectation:
            fake_db = AsyncMock()
            mock_execute_result = Mock()
            mock_execute_result.scalar.return_value = user_test_data
            fake_db.execute.return_value = mock_execute_result

            user = await get_user_by_id(fake_db, test_user_id)
            assert user.id == test_user_id

    async def test_create_new_user(self, user_test_data, user_create_test_data):
        fake_db = AsyncMock()

        mock_execute_result = Mock()
        mock_execute_result.scalar.return_value = user_test_data
        fake_db.execute.return_value = mock_execute_result

        created_user = await create_new_user(fake_db, user_create_test_data)
        assert created_user.login == user_create_test_data.login
        assert created_user.email == user_create_test_data.email

    async def test_update_existing_user(self, user_updated_test_data):
        fake_db_update = AsyncMock()
        mock_rowcount_result = Mock()

        mock_rowcount_result.rowcount.return_value = 1
        fake_db_update.execute.return_value = mock_rowcount_result

        get_user_by_id_mock = AsyncMock(return_value=user_updated_test_data)

        with patch("services.user.get_user_by_id", get_user_by_id_mock):
            updated_user = await update_user(fake_db_update, 1, UserUpdate(email="new_email@example.com"))

        assert updated_user.email == user_updated_test_data.email

    async def test_update_nonexistent_user(self, user_updated_test_data):
        fake_db_update = AsyncMock()
        mock_rowcount_result = Mock()

        mock_rowcount_result.rowcount.return_value = 0
        fake_db_update.execute.return_value = mock_rowcount_result

        with pytest.raises(HTTPException) as exc_info:
            await update_user(fake_db_update, 2, UserUpdate(email="new_email@example.com"))

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User with id 2 not found"
        fake_db_update.commit.assert_not_called()

    async def test_delete_existing_user(self):
        fake_db = AsyncMock()
        mock_rowcount_result = Mock()
        mock_rowcount_result.rowcount.return_value = 0
        fake_db.execute.return_value = mock_rowcount_result

        await delete_user(fake_db, 1)
        fake_db.commit.assert_called_once()

    async def test_delete_nonexistent_user(self):
        fake_db = AsyncMock()
        fake_db.execute.return_value.rowcount = 0

        with pytest.raises(HTTPException) as exc_info:
            await delete_user(fake_db, 999)
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User with id 999 not found"

        fake_db.commit.assert_not_called()
