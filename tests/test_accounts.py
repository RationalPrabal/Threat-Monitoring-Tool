import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('api:accounts:register')
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'strongpassword123',
        'password_confirm': 'strongpassword123',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_user_login(api_client, create_user):
    user = create_user(username='login@example.com', email='login@example.com', password='password123')
    url = reverse('api:accounts:login')
    data = {
        'username': 'login@example.com', # Assuming login view accepts username/email
        'password': 'password123'
    }
    # Standard SimpleJWT TokenObtainPairView often expects 'username' key even if it holds email,
    # or you configured logic. The implementation prompt was: "email/username field". 
    # Default TokenObtainPairView uses 'username' and 'password'.
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

@pytest.mark.django_db
def test_current_user(auto_login_user):
    client, user = auto_login_user()
    url = reverse('api:accounts:current_user')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username
