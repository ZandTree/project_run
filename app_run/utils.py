def check_float_digits(value:float)->bool:
    """
    check if float digits not more than 4
    3.0023  True 
    3.12345 False
    """
    return len(str(value).split(".")[1]) <=4