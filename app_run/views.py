from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.models import AthleteInfo, Challenge, Position, Run

from .pagination import CustomPagination
from .serializers import (AthleteInfoSerializer, ChallengeSerializer,
                          PositionSerializer, RunSerializer, UserSerializer)


@api_view(['GET'])
def get_intro(request):    
    company_dict = {
        "company_name":settings.COMPANY_NAME,
        "slogan":settings.SLOGAN,
        "contacts":settings.CONTACTS
    }    
    return Response(company_dict)

class RunViewSetClass(viewsets.ModelViewSet):    
    """
    api/runs/...
    """     
    queryset = Run.objects.select_related('athlete').all()    
    serializer_class = RunSerializer 
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter]    
    ordering_fields = ['created_at',]
    filterset_fields = ['status','athlete']
       
class FilterAthletesClass(viewsets.ReadOnlyModelViewSet): 
    """
    all coaches and athletes (no su): order, filter, search, pagination
    /api/users/
    "search" default; change to "q" via settings in drf dict SEARCH_PARAM 
    """  
    serializer_class = UserSerializer        
    queryset = User.objects.filter(is_superuser=False)    
    type = serializers.SerializerMethodField()  

    
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['first_name', 'last_name','date_joined']
    pagination_class = CustomPagination

    
    def get_queryset(self):   
        qs = self.queryset                
        type = self.request.query_params.get("type",None) 
        if type:
            if type == "coach":
                return qs.filter(is_staff=True)
            elif type == "athlete":
                return qs.filter(is_staff=False)  
        return qs      

class RunStart(APIView):
    """
    initate start run
    """
    def post(self, request, run_id, format=None):               
        try:
            run = get_object_or_404(Run, id=run_id)  
            if run.status == "init":           
                run.status = "in_progress"
                run.save()
                data = {"status":run.status}
                return Response(data,status=status.HTTP_200_OK)  
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)         
        except Run.DoesNotExist:            
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class RunStop (APIView):
    """
    stopping runs/<run_id>/stop/
    """
    def post(self, request, run_id, format=None):
        try:            
            run = get_object_or_404(Run, id=run_id)
            if run.status == "in_progress":
                run.status = "finished"
                run.save()
                user = run.athlete                
                if user.runs.filter(status="finished").count()%10 == 0:
                    Challenge.objects.create(
                        athlete = run.athlete, full_name = "Сделай 10 Забегов!"
                    )                
                data = {"status":run.status}
                return Response(data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)        
        except Run.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CreateUpdatePersonalInfo(APIView):
    def get(self,request,user_id):        
        user = get_object_or_404(User,id=user_id)        
        obj,created = AthleteInfo.objects.get_or_create(
            user=user) 
        data = AthleteInfoSerializer(obj).data                       
        return Response(data,status=status.HTTP_200_OK)
    
    def put(self,request,user_id):           
        user = get_object_or_404(User,id=user_id)         
        if not user:            
            return Response(status=status.HTTP_404_NOT_FOUND)        
        object,created = AthleteInfo.objects.update_or_create(
                user=user
            )        
        ser = AthleteInfoSerializer(object,data=request.data)  
        if ser.is_valid(raise_exception=True):   
            ser.save()
            data = ser.data
            if created:
                return Response(data=data,status=status.HTTP_201_CREATED)   
            else:
                return Response(data=data,status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
         

@api_view(['GET'])
def showChallenges(request):
    athlete_id = request.query_params.get("athlete",None)      
    if athlete_id:
        athlete = get_object_or_404(User,id=athlete_id)
        lst = athlete.challenges.all()       
    else:
        lst = Challenge.objects.all()
    data = ChallengeSerializer(lst,many=True).data
    return Response(data=data,status=status.HTTP_200_OK)


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer        
    queryset = Position.objects.select_related("run").all()
    def get_queryset(self):   
        qs = self.queryset               
        run_id = self.request.query_params.get("run",None) 
        if run_id:            
            run_obj = get_object_or_404(Run,id=run_id)
            qs = run_obj.positions.all() 
            print(qs.count())     
        print(qs.count())           
        return qs    
            
    