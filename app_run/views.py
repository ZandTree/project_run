from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import distance
from openpyxl import load_workbook
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.models import (AthleteInfo, Challenge, CollectibleItem, Position,
                            Run)

from .pagination import CustomPagination
from .serializers import (AthleteInfoSerializer, ChallengeSerializer,
                          CollectibleItemSerializer, PositionSerializer,
                          RunSerializer, UserItemSerializer, UserSerializer)
from .utils import (calc_total_distance, create_dict, get_total_distance,
                    get_total_time)


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
    queryset = User.objects.prefetch_related('items').filter(is_superuser=False).annotate(count=Count('runs'),filter=Q(runs__status="finished"))     
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
        
    def get_serializer_class(self, *args, **kwargs):
        """
        provide diff serializers for actions
        """
        if self.action == "list":
            return UserSerializer
        elif self.action == "retrieve":
            return UserItemSerializer
        return super().get_serializer_class()
    

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
        """
        1. assigns run status to "finished"
        2. each iteration 10 run's creates a new obj Challenge Model via division;
        3. if geo data present |=> calc distance (float) of a given Run obj
        """
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
                run_postions = run.positions.all()               
                run.distance = get_total_distance(run_postions) 
                run.run_time_seconds = get_total_time(run_postions)               
                run.save()
                data = {"status":run.status}
                total = calc_total_distance(run)
                if  total >= 50:                    
                    Challenge.objects.create(full_name="Пробеги 50 километров!",athlete=run.athlete)                     
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
        return qs 
    
    def perform_create(self, serializer):
        super().perform_create(serializer=serializer)        
        data = serializer.data
        run = get_object_or_404(Run,id=data["run"])  
        user = run.athlete          
        runner_coords = (data["latitude"],data["longitude"])        
        items = CollectibleItem.objects.all() 
        for item in items:
            item_coords = (item.latitude,item.longitude)            
            dist = distance(item_coords,runner_coords).meters            
            if dist <= 100:                  
                user.items.add(item) 
                print(user.items.all())            
           
     

class ShowCollectibleItemSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CollectibleItemSerializer       
    queryset = CollectibleItem.objects.all()    


@api_view(['POST'])
def create_items(request):
    """
    validating length of each row;
    creating dict data: zipping  model_fields(keys) and row (values)
    """    
    file_items = request.FILES.get("file")
    if file_items:
        wb = load_workbook(filename=file_items) 
        ctx = wb.active
        
        model_fields = ('name', 'uid', 'value', 'latitude', 'longitude', 'picture')             
        invalid_rows = []
        for row in ctx.iter_rows(min_row=2,values_only=True):
            if row[0]:
                data = create_dict(model_fields,row)                                                           
                row_ser = CollectibleItemSerializer(data=data)
                if row_ser.is_valid():
                    row_ser.save()                    
                else:                    
                    invalid_rows.append(list(row))
          
        if invalid_rows:
            return Response(data=invalid_rows)
        else:
            return Response(status=status.HTTP_201_CREATED)
        
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST) 



