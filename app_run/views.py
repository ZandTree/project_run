from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.models import Run

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
    queryset = Run.objects.all()
    serializer_class = RunSerializer

class FilterAthletesClass(viewsets.ReadOnlyModelViewSet):   
    serializer_class = UserSerializer     
    queryset = User.objects.filter(is_superuser=False)
    
    def get_queryset(self):   
        qs = self.queryset         
        type = self.request.query_params.get("type",None) 
        if type:
            if type == "coach":
                return qs.filter(is_staff=True)
            elif type == "athelete":
                return qs.filter(is_staff=False)  
        return qs      
        
