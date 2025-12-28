from rest_framework import serializers
from .models import SecurityEvent
from apps.accounts.serializers import UserDetailSerializer

class EventListSerializer(serializers.ModelSerializer):
    created_by_user = UserDetailSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = SecurityEvent
        fields = (
            'id', 'source_name', 'event_type', 'severity', 
            'description', 'timestamp', 'is_acknowledged', 
            'created_by_user'
        )

class EventDetailSerializer(serializers.ModelSerializer):
    created_by_user = UserDetailSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = SecurityEvent
        fields = '__all__'

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = (
            'source_name', 'event_type', 'severity', 
            'description', 'source_ip', 'destination_ip', 
            'raw_data'
        )

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data) # Signal handles alert creation

class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = ('is_acknowledged',)
