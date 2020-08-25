from django.urls import resolve, reverse

import pytest

from build_migration.users.views import UserViewSet


class TestUserURLs:
    """Test URL patterns for users app."""

    @pytest.mark.parametrize("url,view_class", [("/users/", UserViewSet)])
    def test_users_views_resolve(self, url, view_class):
        assert resolve(url).func.cls == view_class

    @pytest.mark.parametrize(
        "url_name,url_kwargs,url",
        [
            ("users:user-list", {}, "/users/"),
            ("users:user-detail", {"pk": 1}, "/users/1/"),
        ],
    )
    def test_users_views_reverse(self, url_name, url_kwargs, url):
        assert reverse(url_name, kwargs=url_kwargs) == url
