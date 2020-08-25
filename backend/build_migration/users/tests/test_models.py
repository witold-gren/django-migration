class TestUser:
    def test_string_representation(self, user_instance):
        assert str(user_instance) == user_instance.username
