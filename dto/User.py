from dataclasses import dataclass
from datetime import datetime
@dataclass(init=True)
class User(object):
    user_id: str
    first_name: str
    last_name: str
    is_admin: bool
    password: str 
    email: str
    created_at: datetime