from .model import User
import falcon

def unique_username(data):
    username = data['username']
    try:
        user = User.objects.get(username = username)
    except: 
        return True
    return True if not user else False
def unique_email(data):
    email = data['email']
    try:
        user = User.objects.get(email = email)
    except:
        return True
    return True if not user else False
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