import pytest
from django.urls import reverse
from rest_framework import status
from apps.events.models import SecurityEvent
from apps.alerts.models import Alert

@pytest.fixture
def create_alert(db):
    event = SecurityEvent.objects.create(
        source_name='Test', event_type='other', severity='HIGH', description='Test'
    )
    # Signal creates alert automatically
    return Alert.objects.first()

@pytest.mark.django_db
def test_create_alert_via_signal(db):
    SecurityEvent.objects.create(
        source_name='Test', event_type='other', severity='HIGH', description='Test'
    )
    assert Alert.objects.count() == 1

@pytest.mark.django_db
def test_acknowledge_alert(auto_login_user, create_alert):
    client, user = auto_login_user()
    alert = create_alert
    url = reverse('api:alerts:alert-acknowledge', args=[alert.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    
    alert.refresh_from_db()
    assert alert.status == Alert.Status.ACKNOWLEDGED
    assert alert.acknowledged_by == user

@pytest.mark.django_db
def test_resolve_alert_requires_notes(auto_login_user, create_alert):
    client, user = auto_login_user()
    alert = create_alert
    url = reverse('api:alerts:alert-resolve', args=[alert.id])
    # Missing notes
    response = client.post(url, {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # With notes
    response = client.post(url, {'notes': 'Fixed'})
    assert response.status_code == status.HTTP_200_OK
    
    alert.refresh_from_db()
    assert alert.status == Alert.Status.RESOLVED
    assert alert.resolution_notes == 'Fixed'
