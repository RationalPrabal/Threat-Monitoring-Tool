from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('auth/', include(('apps.accounts.urls', 'accounts'))),
    path('events/', include(('apps.events.urls', 'events'))),
    path('alerts/', include(('apps.alerts.urls', 'alerts'))),
    path('auditlogs/', include(('apps.auditlogs.urls', 'auditlogs'))),
    path('roles/', include(('apps.rolepermissions.urls', 'rolepermissions'))),
]
