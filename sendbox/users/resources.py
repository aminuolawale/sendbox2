from .model import User
from .utils import unique_email, unique_username
import falcon
import json
import bcrypt, jwt

class CRUDUser(object):
    def on_get(self, req, resp, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except:
                resp.body = json.dumps({'status': False, 'message': 'invalid user_id'})
                resp.status = falcon.HTTP_404
                return
            resp.body = json.dumps({'status': True, 'message': 'success', 'data':user.format()})
            resp.status = falcon.HTTP_200
        else:
            users = [ user.format() for user in User.objects]
            resp.body = json.dumps({'status': True, 'message':'success', 'data': users})
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        user_data = req.media
        if not unique_username(user_data):
            resp.body = json.dumps({'satus':False,'message':'username unavailable. Please choose another'})
            resp.status = falcon.HTTP_400
            return
        if not unique_email(user_data):
            resp.body = json.dumps({'satus':False,'message':'email already registered. Please proceed to login or provide another email'})
            resp.status = falcon.HTTP_400
            return
        password = str.encode(user_data['password'])
        user_data['password'] = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8')
        user = User.objects.create(**user_data)
        user.save()
        resp.body = json.dumps({'status': True, 'message':'successfully added new user', 'data': user.format()})
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, user_id):
        user_data = req.media
        try:
            user = User.objects.get(id=user_id)
        except:
            resp.body = json.dumps({'status': False, 'message': 'invalid user_id'})
            resp.status = falcon.HTTP_404
            return
        for key in user_data:
            user[key] = user_data[key]
        user.save()
        resp.body = json.dumps({'status': True, 'message':'successfully updated user', 'data': user.format()})
        resp.status = falcon.HTTP_200
    
    def on_delete(self, req, resp, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            resp.body = json.dumps({'status': False, 'message': 'invalid user_id'})
            resp.status = falcon.HTTP_404
            return
        user.delete()
        resp.body = json.dumps({'status': True, 'message':'successfully deleted user'})
        resp.status = falcon.HTTP_200

class LoginUser():
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
        token  = jwt.encode(user.format(),'secret').decode('utf-8')
        resp.body = json.dumps({'status': True, 'message': 'user logged in succesfully', 'data':{'token':token}})
        resp.status = falcon.HTTP_200

class AdminUser(object):
    def on_put(self,req,resp, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            resp.body = json.dumps({'status': False, 'message': 'invalid user_id'})
            resp.status = falcon.HTTP_404
            return
        user['is_admin'] = True
        user.save()
        user = User.objects.get(id=user_id)
        resp.body = json.dumps({'status': True, 'message': 'user successfully made admin', 'data':user.format()})
        resp.status = falcon.HTTP_200

class CourierUser(object):
    def on_put(self,req,resp, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            resp.body = json.dumps({'status': False, 'message': 'invalid user_id'})
            resp.status = falcon.HTTP_404
            return
        user['is_courier'] = True
        user.save()
        user = User.objects.get(id=user_id)
        resp.body = json.dumps({'status': True, 'message': 'user successfully made courier', 'data':user.format()})
        resp.status = falcon.HTTP_200


        





