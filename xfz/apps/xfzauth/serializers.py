from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'telephone', 'uuid', 'is_superuser', 'is_active', 'is_staff']
