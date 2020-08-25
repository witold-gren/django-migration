from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from build_migration.users import serializers, views


class TestUserViewSet:
    def test_serializer_list_of_users(self, admin_user, rf, user_factory):
        view = views.UserViewSet.as_view({"get": "list"})

        users = user_factory.build_batch(5)
        views.UserViewSet.queryset = users
        request = rf.get("/users/")
        force_authenticate(request, user=admin_user)
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == len(users)
        assert (
            response.data.get("results")
            == serializers.UserSerializer(users, many=True).data
        )

    @patch.object(views.UserViewSet, "get_object")
    def test_serializer_detail_of_users(self, mock_views, admin_user, rf):
        view = views.UserViewSet.as_view({"get": "retrieve"})

        mock_views.return_value = admin_user
        request = rf.get(f"/users/{admin_user.id}/")
        force_authenticate(request, user=admin_user)
        response = view(request, pk=1)

        assert mock_views.called
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializers.UserSerializer(admin_user).data
