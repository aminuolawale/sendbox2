from .model import Quote
import falcon
import json

class CRUDQuote(object):
    def on_get(self, req, resp):
        quotes = [ quote.format() for quote in Quote.objects ]
        resp.body = json.dumps({'status':True,'message':'succes', 'data':quotes})
    def on_post(self, req, resp):
        user = req.context['user']
        if not user['is_courier']:
            resp.body = json.dumps({'status':False,'message':'user must be courier to set quote'})
            resp.status = falcon.HTTP_401
            return
        quote_data = req.media
        if is_duplicate(quote_data, user):
            resp.body = json.dumps({'status':False,'message':'cannot set duplicate quotes'})
            resp.status = falcon.HTTP_400
            return
        quote_data['courier_id'] = req.context['user']['id']
        quote = Quote.objects.create(**quote_data)
        quote.save()
        resp.body = json.dumps({'status':True,'message':'sucessfully created quote','data':quote.format()})
        resp.status = falcon.HTTP_201
    def on_put(self, req, resp, quote_id):
        try:
            quote = Quote.objects.get(id=quote_id)
        except:
            resp.body = json.dumps({'status':False,'message':'invalid quote_id'})
            resp.status = falcon.HTTP_400
        user = req.context['user']
        if quote['courier_id'] != user['id']:
            resp.body = json.dumps({'status':False,'message':'invalid quote_id'})
            resp.status = falcon.HTTP_403
        quote_data = req.media
        for key in quote_data:
            quote[key] = quote_data[key]
        quote.save()
        resp.body = json.dumps({'status':True,'message':'sucessfully created quote','data':quote.format()})
        resp.status = falcon.HTTP_200
    def on_delete(self,req, resp, quote_id):
        try:
            quote = Quote.objects.get(id=quote_id)
        except:
            resp.body = json.dumps({'status':False,'message':'invalid quote_id'})
            resp.status = falcon.HTTP_400
        user = req.context['user']
        quote_data = req.media
        for key in quote_data:
            quote[key] = quote_data[key]
        quote.save()
        resp.body = json.dumps({'status':True,'message':'sucessfully created quote','data':quote.format()})
        resp.status = falcon.HTTP_200





    