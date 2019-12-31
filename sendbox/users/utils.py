from .model import User
from verify_email import verify_email
import falcon
def valid_username(data):
    return True if len(username) >=3 else False
def unique_username(data):
    username = data['username']
    try:
        user = User.objects.get(username = username)
    except: 
        return True
    return True if not user else False
def valid_email(data):
    is_valid = verify_email(data['email'])
    return True if is_valid else False
    
def unique_email(data):
    email = data['email']
    try:
        user = User.objects.get(email = email)
    except:
        return True
    return True if not user else False
def valid_password(data):
    password = data['password']
    return True if len(password) >= 8 else False

def load_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except:
        description ={
                'status': False,
                'message': 'Invalid user_id'
            }
        raise falcon.HTTPNotFound(description=description)

def validate_input(data):
    if not valid_username(data):
        description={'status': False, 'message':'Invalid username. Username must be at least 3 characters long'}
        raise falcon.HTTPBadRequest(description=description)
    if not unique_username(data):
        description={'status': False, 'message':'Username unavaliable. Please choose another'}
        raise falcon.HTTPBadRequest(description=description)
    if not unique_email(data):
        description={'status': False, 'message':'email already registered. Please proceed to login or provide another email'}
        raise falcon.HTTPBadRequest(description=description)
    if not valid_password(data):
        description={'status': False, 'message':'invalid password. Password must be at least 8 characters long'}
        raise falcon.HTTPBadRequest(description=description)