from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    class Status(models.TextChoices):
        INIT = "init", "Init"
        IN_PROGRES = "in_progress", "In progress"
        FINISHED = "finished", "Finished"
    
    athlete = models.ForeignKey(User,on_delete=models.CASCADE,related_name="runs")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField() 
    status = models.CharField(choices=Status,default=Status.INIT) 
    distance = models.FloatField(null=True,blank=True) 

    def __str__(self):        
        return str(self.id)

class AthleteInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    weight = models.IntegerField(blank=True,null=True)
    goals = models.TextField(blank=True,default="")
    
    def __str__(self):
        return f"user id = {self.user.id}"
    
class Challenge(models.Model):

    full_name = models.CharField(max_length=120)
    athlete = models.ForeignKey(User,on_delete=models.CASCADE,related_name="challenges")   

    def __str__(self):
        return f"{self.full_name} for user {self.athlete}" 
    
class Position(models.Model):

    run = models.ForeignKey(Run,on_delete=models.CASCADE,related_name="positions")
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.run} is parallel(w): {self.latitude} - medidian: {self.longitude}"
    
class CollectibleItem(models.Model):
    name = models.CharField(max_length=120)    
    uid = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.SmallIntegerField()

    def __str__(self):
        return self.name


