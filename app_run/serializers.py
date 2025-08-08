from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AthleteInfo, Challenge, CollectibleItem, Position, Run
from .utils import check_float_digits


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
        fields = ["id","athlete","created_at","comment","athlete_data","status","distance"]



class AthleteInfoSerializer(serializers.ModelSerializer):    
    
    user_id = serializers.IntegerField(source='user.id',read_only=True)
    
    class Meta:
        model = AthleteInfo        
        fields = ["user_id","weight","goals"]

    def validate_weight(self,value): 
        if not isinstance(value,int):
             raise serializers.ValidationError(
                'This field should be an integer')

        if 900 <= value  or value <= 0:                   
            raise serializers.ValidationError(
                'This value can not be less than zero and more than 900 kg.')
        return value
    
class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge 
        fields = "__all__"

class PositionSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Position         
        fields = ["id","run","latitude","longitude"]

    def validate_latitude(self,value)->float:
        """
        float latitude val [-90.0, 90.0] and max 4 digits after "."
        """
        if value >= 90.0 or value <= -90.0:
            raise serializers.ValidationError('This field should be a float in range [-90.0,90.0]')
        if not check_float_digits(value):        
            raise serializers.ValidationError(
                'Too many digits in float part')        
        return value
       
    def validate_longitude(self,value)->float:
        """
        float longitude val [-180.0,180] and max 4 digits after "."
        """
        if value >= 180.0 or value <= -180.0:
            raise serializers.ValidationError('This field should be a float in range [-180.0,180.0]')
        if not check_float_digits(value):        
            raise serializers.ValidationError(
                'Too many digits in float part')        
        return value  
       
    def validate_run(self,value)->float:
        """
        run (via FK) should be in status "in_progress"
        """        
        if value.status != "in_progress":            
            raise serializers.ValidationError(
                'run should be in progress status')
        return value     
    
    
    

class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ["id","name","uid","latitude", "longitude","picture","value"]

    def validate_latitude(self,value)->float:
        """
        float latitude val [-90.0, 90.0] 
        """
        if value >= 90.0 or value <= -90.0:
            print("longitude val invalid")
            raise serializers.ValidationError('This field should be a float in range [-90.0,90.0]')             
        return value
       
    def validate_longitude(self,value)->float:
        """
        float longitude val [-180.0,180] 
        """
        if value >= 180.0 or value <= -180.0:
            print("longitude val invalid")
            raise serializers.ValidationError('This field should be a float in range [-180.0,180.0]')              
        return value 
         
    def validate_value(self,value)->int:
        """
        value of the item should be an int
        """        
        if not int(value):            
            raise serializers.ValidationError('Value should be an integer')              
        return value    
      
class UserItemSerializer(UserSerializer):        
    class Meta(UserSerializer.Meta):
        model = User          
        fields = UserSerializer.Meta.fields + ["items"]

     