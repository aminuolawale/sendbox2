from .model import User
from .utils import validate_input, load_user
import falcon
import json
import bcrypt, jwt
import datetime


class CRUDUser(object):
    def on_get(self, req, resp, user_id=None):
        if user_id:
            user = load_user(user_id)
            resp.body = json.dumps({'status': True, 'message': 'success', 'data':user.format()})
            resp.status = falcon.HTTP_200
        else:
            users = [ user.format() for user in User.objects]
            resp.body = json.dumps({'status': True, 'message':'success', 'data': users})
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        user_data = req.media
        validate_input(user_data)
        password = str.encode(user_data['password'])
        user_data['password'] = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8')
        user = User.objects.create(**user_data)
        user.save()
        resp.body = json.dumps({'status': True, 'message':'successfully added new user', 'data': user.format()})
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, user_id):
        user_data = req.media
        user = load_user(user_id)
        for key in user_data:
            user[key] = user_data[key]
        user.save()
        resp.body = json.dumps({'status': True, 'message':'successfully updated user', 'data': user.format()})
        resp.status = falcon.HTTP_200
    
    def on_delete(self, req, resp, user_id):
        user = load_user(user_id)
        user.delete()
        resp.body = json.dumps({'status': True, 'message':'successfully deleted user'})
        resp.status = falcon.HTTP_200

class LoginUser(object):
    def on_post(self, req, resp):
        login = req.media
        username = login['username'] if 'username' in login else None
        email = login['email'] if 'email' in login else None
        password = login['password'] if 'password' in login else None
        if not username and not email:
            resp.body = json.dumps({'status': False, 'message': 'Incomplete login. Must contain username or email and password'})
            resp.status = falcon.HTTP_400
            return
        try:
            user = User.objects.get(username=username) if username else User.objects.get(email=email)
        except:
            resp.body = json.dumps({'status': False, 'message': 'invalid username/email'})
            resp.status = falcon.HTTP_404
            return
        password = str.encode(password)
        hashed_password = str.encode(user['password'])
        if not bcrypt.checkpw(password,hashed_password):
            resp.body = json.dumps({'status': False, 'message': 'invalid username/email or password'})
            resp.status = falcon.HTTP_404
            return
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        users_t = user.format()
        users_t['exp'] = expiration_time
        token  = jwt.encode(users_t,'secret').decode('utf-8')
        resp.body = json.dumps({'status': True, 'message': 'user logged in succesfully', 'data':{'token':token}})
        resp.status = falcon.HTTP_200

class MakeAdmin(object):
    def on_put(self,req,resp, user_id):
        user = load_user(user_id)
        user['is_admin'] = True
        user.save()
        resp.body = json.dumps({'status': True, 'message': 'user successfully made admin', 'data':user.format()})
        resp.status = falcon.HTTP_200

class MakeCourier(object):
    def on_put(self,req,resp, user_id):
        user = load_user(user_id)
        user['is_courier'] = True
        user.save()
        resp.body = json.dumps({'status': True, 'message': 'user successfully made courier', 'data':user.format()})
        resp.status = falcon.HTTP_200


        





