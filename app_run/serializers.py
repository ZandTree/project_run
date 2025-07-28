from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AthleteInfo, Run


class UserSerializer(serializers.ModelSerializer):    
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()
    class Meta:
        model = User          
        fields = ["id","type","runs_finished","username","date_joined","last_name","first_name"]

    def get_type(self,obj)->str|None:
        type = None
        if obj.is_staff is True:             
            type = "coach"      
        elif obj.is_staff is False:            
            type = "athlete"
        return type
    def get_runs_finished(self,obj)->int:
        return obj.runs.filter(status='finished').count()
            
class AthleteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User          
        fields = ["id","username","last_name","first_name"]
    
            
class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteSerializer(source='athlete',read_only=True)    
    class Meta:
        model = Run        
        fields = ["id","athlete","created_at","comment","athlete_data","status"]

class AthleteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo        
        fields = ["id","weight","goals"]

    def validate_weight(self,value):        
        if 900 < value  or value < 0:  
            print("raising exception")      
            raise serializers.ValidationError(
                'This field can not be less than zero and more than 500 kg.')
        return value