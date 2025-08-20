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
   
            
def parse_positions(prev_position,next_position):
    """
    each new position object gets calculated attr's: distance (km) and speed (m/sec);
    first position gets values of zero;
    """     
    prev_coords = (prev_position.latitude,prev_position.longitude )
    next_coords = (next_position.latitude,next_position.longitude)
    dist_between_points = distance(next_coords,prev_coords).m   
    _time = next_position.date_time - prev_position.date_time 
    time_in_seconds = _time.total_seconds() 
    if time_in_seconds > 0:
            speed = round(dist_between_points/time_in_seconds,2) 
            raw_distance = prev_position.distance + dist_between_points/1000         
            _distance = round(raw_distance,2)            
            return (speed,_distance)
        
              
           
