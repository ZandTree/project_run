from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    """
    distance: km
    """
    class Status(models.TextChoices):
        INIT = "init", "Init"
        IN_PROGRES = "in_progress", "In progress"
        FINISHED = "finished", "Finished"
    
    athlete = models.ForeignKey(User,on_delete=models.CASCADE,related_name="runs")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField() 
    status = models.CharField(choices=Status,default=Status.INIT) 
    distance = models.FloatField(null=True,blank=True) 
    run_time_seconds = models.IntegerField(null=True,blank=True)
    speed = models.FloatField(blank=True, default=0)

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
    """
    speed: m/sec; distance: km
    """
    run = models.ForeignKey(Run,on_delete=models.CASCADE,related_name="positions")
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_time = models.DateTimeField(null=True,blank=True)
    speed = models.FloatField(null=True,blank=True) 
    distance = models.FloatField(null=True,blank=True)


    def __str__(self):
        return f"{self.run} is parallel(w): {self.latitude} - medidian: {self.longitude}"
    
class CollectibleItem(models.Model):
    name = models.CharField(max_length=120)    
    uid = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.SmallIntegerField()
    users = models.ManyToManyField(User,related_name="items",blank=True,null=True)

    def __str__(self):
        return self.name



class Subscribe(models.Model):
    RATING = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
        (None, 'unknown')
    )
          
    coach = models.ForeignKey(User,related_name="coaches",on_delete=models.CASCADE)
    runner = models.ForeignKey(User,related_name="runners",on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING,default=None,blank=True,null=True)
    
    class Meta:
        unique_together = ('coach', 'runner')

    def __str__(self):
        return f"coach {self.coach}:ID {self.coach.id}, client: {self.runner},id:{self.runner.id}"

