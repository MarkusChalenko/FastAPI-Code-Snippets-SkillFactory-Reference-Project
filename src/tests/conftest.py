# import datetime
#
# import pytest
#
# from models import User
# from schemas.user import UserCreate
#
#
# @pytest.fixture
# def user_test_data():
#     test_user = User(id=1,
#                      login="User",
#                      email="test@gmail.com",
#                      hashed_password="rr23cr2",
#                      registered_at=datetime.datetime.utcnow())
#     return test_user
#
#
# @pytest.fixture
# def user_create_test_data():
#     test_create_user = UserCreate(login="User",
#                                   email="test@gmail.com",
#                                   password="test1234!",
#                                   registered_at=datetime.datetime.utcnow())
#     return test_create_user
#
#
# @pytest.fixture
# def user_updated_test_data():
#     test_create_user = UserCreate(login="User",
#                                   email="new_email@example.com",
#                                   password="test1234!",
#                                   registered_at=datetime.datetime.utcnow())
#     return test_create_user
