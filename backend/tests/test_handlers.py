"""
Test the global error handlers here. We change the templates for these for
non-DRF projects, and DRF project should probably set their own. These tests
also sanity-check whether the middleware stack and apps are configured correctly.
"""

from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.urls import path

import pytest

from config.urls import urlpatterns as existing_urlpatterns

pytestmark = pytest.mark.urls("tests.test_handlers")


def internal_error_view(request):
    return HttpResponseServerError()


def not_found_view(request):
    return HttpResponseNotFound()


def forbidden_view(request):
    return HttpResponseForbidden()


# We use a custom urlconf because we need to use custom views for these tests, and
# we also need to test the whole Django stack rather than the view in isolation
urlpatterns = existing_urlpatterns + [
    path("500_error", internal_error_view),
    path("404_error", not_found_view),
    path("403_error", forbidden_view),
]


@pytest.mark.django_db
def test_500_handler(client):
    response = client.get("/500_error")
    assert response.status_code == 500


@pytest.mark.django_db
def test_404_handler(client):
    response = client.get("/404_error")
    assert response.status_code == 404


@pytest.mark.django_db
def test_403_handler(client):
    response = client.get("/403_error")
    assert response.status_code == 403
