from rest_framework import serializers
from django.contrib.auth.models import User

from mainApp.models import items


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = items
        fields = ['id', 'type', 'community', 'longitude', 'latitude']


class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=items.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'items']
