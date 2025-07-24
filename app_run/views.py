from app_run.models import Run
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .serializers import RunSerializer, UserSerializer


@api_view(['GET'])
def get_intro(request):    
    company_dict = {
        "company_name":settings.COMPANY_NAME,
        "slogan":settings.SLOGAN,
        "contacts":settings.CONTACTS
    }    
    return Response(company_dict)

class RunViewSetClass(viewsets.ModelViewSet):         
    queryset = Run.objects.select_related('athlete').all()    
    serializer_class = RunSerializer    

class FilterAthletesClass(viewsets.ReadOnlyModelViewSet):   
    serializer_class = UserSerializer     
    queryset = User.objects.filter(is_superuser=False)
    type = serializers.SerializerMethodField()  

    # "search" default; change to "q" via settings drf dict SEARCH_PARAM 
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']
    
    def get_queryset(self):   
        qs = self.queryset         
        type = self.request.query_params.get("type",None) 
        if type:
            if type == "coach":
                return qs.filter(is_staff=True)
            elif type == "athlete":
                return qs.filter(is_staff=False)  
        return qs      
        
