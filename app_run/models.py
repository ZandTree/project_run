from django.contrib.auth.models import User
from django.db import models

# class RunManager(models.Manager):
#     def filter_superusers(self):
#         return self.get_queryset().filter(athlete__user_is_superuser=False)
    
class Run(models.Model):
    athlete = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()   

    def __str__(self):        
        return self.athlete.username

