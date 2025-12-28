import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.events.models import SecurityEvent

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        if 'password' not in kwargs:
            kwargs['password'] = 'testpass123'
        if 'username' not in kwargs:
            kwargs['username'] = 'testuser'
        if 'email' not in kwargs:
            kwargs['email'] = 'test@example.com'
            
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def auto_login_user(db, create_user, api_client):
    def make_auto_login(user=None, **kwargs):
        if user is None:
            user = create_user(**kwargs)
        api_client.force_authenticate(user=user)
        return api_client, user
    return make_auto_login

@pytest.fixture
def admin_user(create_user):
    return create_user(username='admin', role='ADMIN', is_staff=True)

@pytest.fixture
def analyst_user(create_user):
    return create_user(username='analyst', role='ANALYST')
