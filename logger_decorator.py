import logging
from functools import wraps
import json

def print_classification(param, result):
    with open("log.txt", 'a') as file:
        tolog = {"parameter": f"{param}", "value": f"{result}"}
        json.dump(tolog, file)
        file.write('\n')

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Call the decorated function
        result = func(*args, **kwargs)
        
        # Log the result
        print_classification(args, result)

        return result
    
    return wrapper

def log_decorator_batch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Call the decorated function
        results = func(*args, **kwargs)
        
        # Log the result
        for (param, result) in zip(*args, results):
            print_classification(param, result)

        return results
    
    return wrapper