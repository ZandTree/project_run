from django.contrib import admin

from .models import AthleteInfo, Challenge, CollectibleItem, Position, Run


class RunAdmin(admin.ModelAdmin):
    list_display = ['id','athlete_id',"status",'athlete__username','created_at','comment',"distance","run_time_seconds"]
    list_select_related = ("athlete",)
    list_filter = ["status"]

    def user_type(self, obj):
        """display sport type"""
        return obj.athlete.is_staff

class AthleteInfoAdmin(admin.ModelAdmin):
    list_display = ['id','user_id',"goals",'weight']

class ChellangeAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','athlete'] 

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id','latitude','longitude','run',"date_time"]    
class CollectibleItemAdmin(admin.ModelAdmin):
    list_display = ['id','name','latitude','longitude','picture'] 

admin.site.register(Run,RunAdmin)    
admin.site.register(Challenge,ChellangeAdmin)
admin.site.register(AthleteInfo, AthleteInfoAdmin)    
admin.site.register(Position, PositionAdmin)    
admin.site.register(CollectibleItem,CollectibleItemAdmin)    