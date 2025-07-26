from django.contrib.auth.models import User
from django.db import models

# class RunManager(models.Manager):
#     def filter_superusers(self):
#         return self.get_queryset().filter(athlete__user_is_superuser=False)
    
class Run(models.Model):
    class Status(models.TextChoices):
        INIT = "init", "Init"
        IN_PROGRES = "in_progress", "Started"
        FINISHED = "finished", "Finished"

    
    athlete = models.ForeignKey(User,on_delete=models.CASCADE,related_name="runs")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField() 
    status = models.CharField(choices=Status,default=Status.INIT)  

    def __str__(self):        
        return self.athlete.username
