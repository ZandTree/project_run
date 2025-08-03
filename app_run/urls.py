from django.urls import include, path
from rest_framework import routers

from .views import (CreateUpdatePersonalInfo, FilterAthletesClass,
                    PositionViewSet, RunStart, RunStop, RunViewSetClass,
                    ShowCollectibleItemSet, get_intro, showChallenges)

router = routers.DefaultRouter()
router.register(r'users',FilterAthletesClass,basename='users')
router.register(r'runs',RunViewSetClass,basename='runs')
router.register(r'positions',PositionViewSet,basename='positions')
router.register(r'collectible_item',ShowCollectibleItemSet,basename='items')

urlpatterns = [    
    path('company_details/',get_intro),
    path('runs/<run_id>/start/',RunStart.as_view()),
    path('runs/<run_id>/stop/',RunStop.as_view()),    
    path('athlete_info/<user_id>/',CreateUpdatePersonalInfo.as_view()),    
    path('challenges/',showChallenges),    
    path('',include(router.urls),name="collectible_item"),    
    path('',include(router.urls),name="runs"),
    path('',include(router.urls),name='users'),    
    path('',include(router.urls),name='positions')       
    
]