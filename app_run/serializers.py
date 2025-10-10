from django.contrib.auth.models import User
from django.db.models import Avg, Max, OuterRef, Prefetch, Subquery, Sum
from rest_framework import serializers

from .models import (AthleteInfo, Challenge, CollectibleItem, Position, Run,
                     Subscribe)
from .utils import check_float_digits


class UserSerializer(serializers.ModelSerializer):    
    type = serializers.SerializerMethodField()
    runs_finished = serializers.IntegerField(source="count",read_only=True)    
    rating = serializers.FloatField(read_only=True)    
    class Meta:
        model = User       
        fields = ["id","type","runs_finished","username","date_joined","last_name","first_name","rating"]

    def get_type(self,obj)->str|None:
        type = None
        if obj.is_staff is True:             
            type = "coach"      
        elif obj.is_staff is False:            
            type = "athlete"
        return type
        
           
class AthleteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User          
        fields = ["id","username","last_name","first_name"] 

class ShortAthleteSerializer(AthleteSerializer):    
    full_name = serializers.SerializerMethodField(read_only=True)       
    class Meta(UserSerializer.Meta):
        model = User          
        fields = ["id","username","full_name"] 

    def get_full_name(self,obj):        
        return f"{obj.first_name} {obj.last_name}"          
      

class SubscribeSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Subscribe
        fields = ["id","coach","runner"]
        

    def validate_coach(self,coach):        
        if not coach.is_staff:
            raise serializers.ValidationError("user should be a coach")
        return coach
    
    def validate_runner(self, runner):        
        if runner.is_staff:
            raise serializers.ValidationError("runner can not be a coach")
        return runner
    def validate(self,attrs):
        coach = attrs.get("coach")
        runner = attrs.get("runner")
        if Subscribe.objects.filter(coach_id = coach.id,runner_id = runner.id).exists():
            raise serializers.ValidationError("this pair is already exists")
        return attrs

class SubscribeSerExtended(serializers.ModelSerializer): 
    # in case you need extended info about the user
    coach = UserSerializer(read_only=True)  
    runner = UserSerializer(read_only=True)  
    class Meta:
        model = Subscribe
        fields = ["id","coach","runner"]

    # TODO: if needed add validation       


class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteSerializer(source='athlete',read_only=True)    
    class Meta:
        model = Run        
        fields = ["id","athlete","created_at","comment","athlete_data","status","distance","run_time_seconds","speed"]

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
        fields = ["full_name","athlete"]



class ChallengeSummarySerializer(serializers.Serializer): 

    def to_representation(self, instance):   
                       
        repr =  super().to_representation(instance)                
        repr["name_to_display"] = instance.full_name
        repr["athletes"] = []      
             
        users = User.objects.filter(is_staff=False).prefetch_related(
        Prefetch("challenges", queryset=Challenge.objects.select_related("athlete").only("full_name","athlete_id").distinct(),to_attr="related_challenges")
        ).only("first_name","last_name","username")       
                                
        for user in users:
            for challange in user.related_challenges:                
                if instance.full_name == challange.full_name:            
                    ser = ShortAthleteSerializer(user)                        
                    repr["athletes"].append(ser.data)
                    break                                    
        
        return repr   
    
class PositionSerializer(serializers.ModelSerializer):  
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f") 
    distance = serializers.FloatField(default=0)    
    speed = serializers.FloatField(default=0)    
    class Meta:
        model = Position         
        fields = ["id","run","latitude","longitude","date_time","distance","speed"]

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
            # print("longitude val invalid")
            raise serializers.ValidationError('This field should be a float in range [-90.0,90.0]')             
        return value
       
    def validate_longitude(self,value)->float:
        """
        float longitude val [-180.0,180] 
        """
        if value >= 180.0 or value <= -180.0:
            # print("longitude val invalid")
            raise serializers.ValidationError('This field should be a float in range [-180.0,180.0]')              
        return value 
         
    def validate_value(self,value)->int:
        """
        value of the item should be an int
        """        
        if not int(value):            
            raise serializers.ValidationError('Value should be an integer')              
        return value    



class UserCoachSerializer(UserSerializer):
    """
    for coaches: substitute parent serializer with add info:
    list m2m: collected items and subscribed athletes
    """  
    items =CollectibleItemSerializer(many=True, read_only=True)          
    athletes = serializers.SerializerMethodField(read_only=True)       
    class Meta(UserSerializer.Meta):
        model = User          
        fields = UserSerializer.Meta.fields + ["items","athletes"]

    def get_athletes(self,obj)->list|None:
        """
        return filtered runner_id's
        """        
        return obj.runners.values_list("runner_id",flat=True) 

class UserAthleteSerializer(UserSerializer):
    """
    for athletes: substitute parent serializer with add info:
    list m2m: collected items and subscribed athletes  
    """
    items =CollectibleItemSerializer(many=True, read_only=True)
    coach = serializers.SerializerMethodField(read_only=True)       
         
    class Meta(UserSerializer.Meta):
        model = User          
        fields = UserSerializer.Meta.fields + ["items","coach"]

    def get_coach(self,obj)->User|None:       
        coach = obj.coaches.values_list("coach_id",flat=True).last()         
        return coach    

class CoachAnaliticSerializer(serializers.Serializer):  
    

    def to_representation(self, instance):
        """
        instance of coach
        """       
        repr = super().to_representation(instance) 
           
        coach_athletes = (Subscribe.objects.select_related("coach","runner").filter(coach=instance).
        values_list("runner_id",flat=True))
       
        runs = (Run.objects.filter(athlete_id__in=coach_athletes).values("athlete_id").annotate(max_single_dist=Max("distance"),avg_speed=Avg("speed"),summ_dist=Sum("distance")))
         

        if coach_athletes and runs:
            longest_user = runs.order_by("max_single_dist").last()        
            user_total = runs.order_by("summ_dist").last()
            user_speed = runs.order_by("avg_speed").last()            
            repr["longest_run_user"] = longest_user["athlete_id"]
            repr["longest_run_value"] = round(longest_user["max_single_dist"],2)  
            repr["total_run_user"] = user_total["athlete_id"]
            repr["total_run_value"] = round(user_total["summ_dist"],2)  
            repr["speed_avg_user"] = user_speed["athlete_id"]
            repr["speed_avg_value"] = user_speed["avg_speed"]
        elif coach_athletes:            
            single_athlete = User.objects.get(id=coach_athletes[0])
            repr["longest_run_user"] = single_athlete.id
            repr["longest_run_value"] = 0  
            repr["total_run_user"] = single_athlete.id
            repr["total_run_value"] = 0  
            repr["speed_avg_user"] = single_athlete.id
            repr["speed_avg_value"] = 0

        
        
        return repr  
        

        
         
    