from rest_framework import serializers

from mainApp.models import items


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = items
        fields = ['id', 'type', 'community', 'longitude', 'latitude']
