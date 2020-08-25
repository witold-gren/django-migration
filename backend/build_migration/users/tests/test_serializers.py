from build_migration.users.serializers import UserSerializer


class TestUserSerializers:
    def test_serialize_data(self, user_instance):
        assert UserSerializer(user_instance).data == {
            "username": user_instance.username,
            "first_name": user_instance.first_name,
            "last_name": user_instance.last_name,
            "email": user_instance.email,
        }

    def test_required_field_in_serializers(self):
        serializer = UserSerializer(data={})
        assert serializer.is_valid() is False
        assert set(serializer.errors) == {"username"}
