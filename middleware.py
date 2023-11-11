from functools import wraps

def jwt_based_authentication(func):
    @wraps
    def wrapper(*args, **kwargs):
        return func()
    return wrapper