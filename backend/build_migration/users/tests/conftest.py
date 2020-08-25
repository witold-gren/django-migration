import pytest


@pytest.fixture
def user_password():
    return "7jefB#f@Cc7YJB]2v"


@pytest.fixture
def admin_register_user_data(user_password):
    return {
        "username": "test",
        "email": "test@test.com",
        "password1": user_password,
        "password2": user_password,
    }
