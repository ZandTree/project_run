from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Run


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run        
        fields = ["id","athlete","created_at","comment"]

class UserSerializer(serializers.ModelSerializer):    
    type = serializers.SerializerMethodField()
    class Meta:
        model = User          
        fields = ["id","type","username","date_joined","last_name","first_name"]

    def get_type(self,obj):
        type = None
        if obj.is_staff is True:             
            type = "coach"      
        elif obj.is_staff is False:            
            type = "athlete"
        return type
            
        
          