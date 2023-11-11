from dataclasses import dataclass

@dataclass(init=True)
class User(object):
    user_id: str
    first_name: str
    last_name: str
    
    