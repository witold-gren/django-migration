"""
Tests for endpoints belonging to no particular app. These are mostly sanity
checks to ensure the configuration is correct.
"""

from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_health_check(client):
    view_name = "health_check:health_check_home"
    url = reverse(view_name)
    response = client.get(url)
    assert response.status_code == 200
