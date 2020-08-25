import pytest

from build_migration.users.admin import UserCreationForm


class TestUserCreationForm:
    @pytest.mark.django_db
    def test_clean_success(self, admin_register_user_data):
        # instantiate the form with a new username
        form = UserCreationForm(admin_register_user_data)

        # run is_valid() to trigger the validation
        valid = form.is_valid()
        assert valid

        # run the actual clean methods
        assert form.clean_username() == admin_register_user_data["username"]

    @pytest.mark.django_db
    @pytest.mark.parametrize("duplicate_field", ["username"])
    def test_clean_duplicate_error(
        self, duplicate_field, admin_register_user_data, user_factory
    ):
        user = user_factory()

        # instantiate the form with the same duplicate field value as already existing user
        form = UserCreationForm(
            {
                **admin_register_user_data,
                duplicate_field: getattr(user, duplicate_field),
            }
        )

        # run is_valid() to trigger the validation, which is going to fail
        # because the field value is already taken
        valid = form.is_valid()
        assert not valid

        # the form.errors dict should contain a single error called same as duplicate field
        assert len(form.errors) == 1
        assert duplicate_field in form.errors
