from django.db.models import Sum
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
        raise ValueError("Not enough data to calculate the distance") 
    
def calc_total_distance(obj):   
    total =Run.objects.filter(athlete=obj.athlete).aggregate(summ=Sum('distance'))
    return total["summ"]


def create_dict(tuple_keys,tuple_values)->dict:
    """ return dict with keys from iterables: tuple keys and tuple values """     
    return dict(zip(tuple_keys,tuple_values)) 
   
    

    


 