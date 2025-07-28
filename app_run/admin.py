from django.contrib import admin

from .models import AthleteInfo, Run


class RunAdmin(admin.ModelAdmin):
    list_display = ['id','athlete_id',"status",'athlete__username','created_at','comment']
class AthleteInfoAdmin(admin.ModelAdmin):
    list_display = ['id','user_id',"goals",'weight']

admin.site.register(Run,RunAdmin)    
admin.site.register(AthleteInfo, AthleteInfoAdmin)    