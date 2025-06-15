# core/tests/conftest.py
import pytest
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def authenticated_client(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    client = Client()
    client.login(username='testuser', password='testpass')
    return client
