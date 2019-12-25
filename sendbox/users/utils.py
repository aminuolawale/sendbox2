from .model import User

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