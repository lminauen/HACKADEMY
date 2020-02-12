from django.contrib.auth.models import User
from rest_framework import serializers

from mainApp.models import items


class ItemsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = items
        fields = ['id', 'user', 'type', 'community', 'longitude', 'latitude']


class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=items.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'items']
