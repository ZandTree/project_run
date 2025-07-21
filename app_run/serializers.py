from rest_framework import serializers

from .models import Run


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run        
        fields = ["id","athlete","created_at","comment"]