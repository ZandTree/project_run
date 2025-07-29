from django.contrib import admin

from .models import AthleteInfo, Challenge, Run


class RunAdmin(admin.ModelAdmin):
    list_display = ['id','athlete_id',"status",'athlete__username','created_at','comment',"user_type"]
    list_select_related = ("athlete",)
    list_filter = ["status"]

    def user_type(self, obj):
        """display sport type"""
        return obj.athlete.is_staff

class AthleteInfoAdmin(admin.ModelAdmin):
    list_display = ['id','user_id',"goals",'weight']

class ChellangeAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','athlete']    
    
admin.site.register(Run,RunAdmin)    
admin.site.register(Challenge,ChellangeAdmin)
admin.site.register(AthleteInfo, AthleteInfoAdmin)    