from django.contrib import admin

from .models import Run


class RunAdmin(admin.ModelAdmin):
    list_display = ['id','athlete_id','athlete__username','created_at','comment']

admin.site.register(Run,RunAdmin)    