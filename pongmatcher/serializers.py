from rest_framework import serializers
from pongmatcher.models import MatchRequest, Participant

class MatchRequestSerializer(serializers.Serializer):
    id = serializers.CharField(source='uuid')
    player = serializers.CharField(source='player_uuid')
    match_id = serializers.CharField(required=False)

    def create(self, validated_data):
        return MatchRequest.objects.create(**validated_data)
