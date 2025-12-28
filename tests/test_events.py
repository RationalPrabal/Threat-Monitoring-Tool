import pytest
from django.urls import reverse
from rest_framework import status
from apps.events.models import SecurityEvent

@pytest.mark.django_db
def test_create_event(auto_login_user):
    client, user = auto_login_user()
    url = reverse('api:events:securityevent-list') # ViewSet default basename is model name lowercased?
    # Or explicitly I should check urls.py router registry.
    # In apps/events/urls.py: router.register(r'', EventViewSet)
    # If basename not specified, it derives from queryset model name? 
    # EventViewSet queryset = SecurityEvent.objects.all() -> 'securityevent'
    # So 'api:events:securityevent-list'.
    data = {
        'source_name': 'Firewall',
        'event_type': 'intrusion',
        'severity': 'HIGH',
        'description': 'Port scan detected',
        'source_ip': '192.168.1.100'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert SecurityEvent.objects.count() == 1
    assert SecurityEvent.objects.first().created_by == user

@pytest.mark.django_db
def test_list_events(auto_login_user):
    client, _ = auto_login_user()
    SecurityEvent.objects.create(
        source_name='Test', event_type='other', severity='LOW', description='Test'
    )
    url = reverse('api:events:securityevent-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1

@pytest.mark.django_db
def test_alert_auto_creation(auto_login_user):
    client, _ = auto_login_user()
    url = reverse('api:events:securityevent-list')
    data = {
        'source_name': 'IPS',
        'event_type': 'malware',
        'severity': 'CRITICAL',
        'description': 'Ransomware detected'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check alert was created
    from apps.alerts.models import Alert
    assert Alert.objects.count() == 1
    alert = Alert.objects.first()
    assert alert.severity == 'CRITICAL'
