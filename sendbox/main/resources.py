import falcon
import json

class HomeResource(object):
    def on_get(self, req, resp):
        resp.body = json.dumps({'status':True, 'message': "Welcome to the sendbox API"})
        resp.status = falcon.HTTP_200