from django.urls import include, path
from rest_framework import routers

from .views import FilterAthletesClass, RunViewSetClass, get_intro

router = routers.DefaultRouter()
router.register(r'',RunViewSetClass)

urlpatterns = [    
    path('company_details/',get_intro),
    path('runs/',include(router.urls)),
    path('users/',FilterAthletesClass.as_view({'get':'list'})),
    # path('users/<type>/',FilterAthletesClass.as_view({'get':'list'})),
    
]