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

    def __str__(self):        
        return self.athlete.username

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