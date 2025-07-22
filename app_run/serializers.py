from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Run


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run        
        fields = ["id","athlete","created_at","comment"]

class UserSerializer(serializers.ModelSerializer):
    # type = serializers.ReadOnlyField()
    # # type = serializers.CharField(max_length=10)
    class Meta:
        model = User        
        fields = ["id","username","date_joined","last_name","first_name"]