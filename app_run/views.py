from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.models import Run

from .serializers import RunSerializer


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
    