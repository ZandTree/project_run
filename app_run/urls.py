from django.urls import include, path
from rest_framework import routers

from .views import RunViewSetClass, get_intro

router = routers.DefaultRouter()
router.register(r'',RunViewSetClass)

urlpatterns = [    
    path('/company_details/',get_intro),
    path('/runs/',include(router.urls)),
    
]