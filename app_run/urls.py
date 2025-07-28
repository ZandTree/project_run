from django.urls import include, path
from rest_framework import routers

from .views import (CreateUpdatePersonalInfo, FilterAthletesClass, RunStart,
                    RunStop, RunViewSetClass, get_intro)

router = routers.DefaultRouter()
router.register(r'',RunViewSetClass)

urlpatterns = [    
    path('company_details/',get_intro),
    path('runs/<run_id>/start/',RunStart.as_view()),
    path('runs/<run_id>/stop/',RunStop.as_view()),
    path('runs/',include(router.urls)),
    path('users/',FilterAthletesClass.as_view({'get':'list'})),
    path('athlete_info/<user_id>/',CreateUpdatePersonalInfo.as_view())    
    
]