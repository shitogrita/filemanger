import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls.base import reverse
from rest_framework.test import APIClient

from core.models import StoredFile

@pytest.mark.django_db
def test_file_upload_authenticated(authenticated_client):
    file = SimpleUploadedFile("test.txt", b"file content")
    response = authenticated_client.post('/upload/', {'file': file})
    assert response.status_code == 302
    assert StoredFile.objects.count() == 1

@pytest.mark.django_db
def test_file_upload_anonymous(client):
    file = SimpleUploadedFile("test.txt", b"file content")
    response = client.post('/upload/', {'file': file})
    assert response.status_code in [302, 403, 401]
    assert StoredFile.objects.count() == 0

@pytest.mark.django_db
def test_status_api_view(client):
    response = client.get('/status/')
    assert response.status_code == 200
    assert 'user_count' in response.content.decode() or 'Количество пользователей' in response.content.decode()

@pytest.mark.django_db
def test_api_file_list(authenticated_client):
    response = authenticated_client.get('/api/files/')
    assert response.status_code == 200
    assert isinstance(response.json(), list) or response['Content-Type'].startswith('application/json')

from unittest.mock import patch
from django.core import mail

@pytest.mark.django_db
@patch('django.core.mail.get_connection')
def test_email_service_status(mock_get_connection, client):
    mock_get_connection.return_value.open.return_value = None
    response = client.get('/status/')
    assert response.status_code == 200
    content = response.content.decode()
    assert 'OK' in content or 'email_service_status' in content


@pytest.mark.django_db
def test_ml_predict_endpoint_with_login():
    user = User.objects.create_user(username='walter', password='MargoHaha1')
    client = APIClient()
    login_successful = client.login(username='walter', password='MargoHaha1')
    assert login_successful

    url = reverse('ml_predict')
    data = {"input_data": {"text": "hello"}}

    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'