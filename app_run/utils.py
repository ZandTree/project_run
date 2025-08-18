from django.db.models import Max, Min, Sum
from geopy.distance import distance

from app_run.models import Run


def check_float_digits(value:float)->bool:
    """
    check if float digits not more than 4
    3.0023  True 
    3.12345 False
    """
    return len(str(value).split(".")[1]) <=4

def calc_distance(lst)->float:  
    """
    iterate through list of tuples with coordinates and calculate sum 
    of distance points  using 3d party geopy function
    """   
    total_distance = 0    
    for idx in range(len(lst)-1):
        point_1 = lst[idx]
        point_2 = lst[idx+1]        
        dist_between_points = distance(point_1,point_2).km
        total_distance += dist_between_points
    return total_distance    

def get_total_distance(qs)->float:
    """
    create list of tuples (lat,long) based on attr's of postion objects;
    qs should contain at least two elements for calculation
    """  
    if qs.count() >=2:   
        points_lst = []    
        [points_lst.append((pos.latitude,pos.longitude),) for pos in qs]    
        total = calc_distance(points_lst)        
        return round(total,4)
    else:
        return 0
        # raise ValueError("Not enough data to calculate the distance") 
    
def get_total_time(qs)->int:
    """
    calc time start and finish
    qs should contain at least two elements for calculation
    """  
    if qs.count() >=2:
        start_time = qs.aggregate(start = Min('date_time'))          
        finish_time = qs.aggregate(finish = Max('date_time'))         
        delta = finish_time["finish"] - start_time["start"]         
        _timestamp = delta.total_seconds()         
        return  _timestamp
         
    else:
        # raise ValueError("Not enough data to calculate the distance") 
        return 0
    
def calc_total_distance(obj):   
    total =Run.objects.filter(athlete=obj.athlete).aggregate(summ=Sum('distance'))
    return total["summ"]


def create_dict(tuple_keys,tuple_values)->dict:
    """ return dict with keys from iterables: tuple keys and tuple values """     
    return dict(zip(tuple_keys,tuple_values)) 
   
    

def parse_positions(qs,start=1):
    """
    return 
    - distance in km?;
    - speed    in m/sec;
    """
    distance_to_current = 0 
    qs_length = qs.count()
    if qs_length >= 2:
        for idx in range(qs_length - 1):
            prev_pos = qs[idx]
            next_pos = qs[idx+1]  
            prev_coords = (prev_pos.latitude,prev_pos.longitude)
            next_coords = (next_pos.latitude,next_pos.longitude)       
            dist_between_points = distance(prev_coords,next_coords).m
            _time = (next_pos.date_time - prev_pos.date_time)            
            time_in_seconds = _time.total_seconds()           
            speed = round(dist_between_points/time_in_seconds,2)
            # print("speed in m/sec ", round(speed,2))
            distance_to_current += dist_between_points
            next_pos.speed = speed
            next_pos.distance = round(distance_to_current/1000,2)
            next_pos.save()
    else:
            prev_pos.speed = 0
            prev_pos.distance = 0
            prev_pos.save()        

