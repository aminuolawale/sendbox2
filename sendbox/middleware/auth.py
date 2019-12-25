import jwt
import falcon

class AuthMiddleware(object):
    
    def process_request(self, req, resp):
        exempts={
        '/users':['GET', 'POST'],
        '/login': ['POST'],
        '/quotes': ['GET']
        }
        if req.path in exempts and req.method in exempts[req.path]:
            return
        token = req.get_header('Authorization')
        if not token:
            description ={
                'status': False,
                'message': 'Token not provided.Please provide token under header "Authorization"'
            }
            raise falcon.HTTPUnauthorized(description=description)
        try:
            user = jwt.decode(token, 'secret')
        except:
            description ={
                'status': False,
                'message': 'Invalid token'
            }
            raise falcon.HTTPUnauthorized(description=description)
        req.context['user'] = user