from .model import Quote
from .utils import is_duplicate, load_quote, validate_input
from bson.objectid import ObjectId
import falcon
import json


class CRUDQuote(object):
    def on_get(self, req, resp, quote_id=None):
        if quote_id:
            quote = load_quote(quote_id)
            resp.body = json.dumps({'status':True,'message':'succes', 'data':quote})
            resp.status = falcon.HTTP_200
        quotes = [ quote.format() for quote in Quote.objects ]
        resp.body = json.dumps({'status':True,'message':'succes', 'data':quotes})
        resp.status = falcon.HTTP_200
    def on_post(self, req, resp):
        user = req.context['user']
        if not user['is_courier']:
            resp.body = json.dumps({'status':False,'message':'user must be courier to set quote'})
            resp.status = falcon.HTTP_401
            return
        quote_data = req.media
        validate_input(quote_data,user)
        if is_duplicate(quote_data, user):
            resp.body = json.dumps({'status':False,'message':'you have already set a quote on the given locations'})
            resp.status = falcon.HTTP_400
            return
        quote_data['courier_id'] = req.context['user']['id']
        quote = Quote.objects.create(**quote_data)
        quote.save()
        resp.body = json.dumps({'status':True,'message':'sucessfully created quote','data':quote.format()})
        resp.status = falcon.HTTP_201
    def on_put(self, req, resp, quote_id):
        quote = load_quote(quote_id)
        user = req.context['user']
        user_id = ObjectId(user['id'])
        if quote['courier_id'] != user_id:
            resp.body = json.dumps({'status':False,'message':'you cannot perform this action'})
            resp.status = falcon.HTTP_403
            return
        quote_data = req.media
        for key in quote_data:
            quote[key] = quote_data[key]
        quote.save()
        resp.body = json.dumps({'status':True,'message':'sucessfully created quote','data':quote.format()})
        resp.status = falcon.HTTP_200
    def on_delete(self,req, resp, quote_id):
        quote = load_quote(quote_id)
        user = req.context['user']
        user_id = ObjectId(user['id'])
        if quote['courier_id'] != user_id:
            resp.body = json.dumps({'status':False,'message':'you cannot perform this action'})
            resp.status = falcon.HTTP_403
            return
        quote.delete()
        resp.body = json.dumps({'status':True,'message':'sucessfully deleted quote'})
        resp.status = falcon.HTTP_200

class GetQuote(object):
    def on_get(self, req, resp):
        origin = req.media['origin']
        destination = req.media['destination']
        weight = req.media['weight']
        try:
            quotes = [{'quote':quote.format(),'total_price':quote['price_per_kg']*weight} for quote in Quote.objects.filter(origin=origin, destination=destination)]
        except:
            resp.body = json.dumps({'status':True,'message':'no quotes found for given origin and destination','data':[]})
            resp.status = falcon.HTTP_200
            return
        resp.body = json.dumps({'status':True,'message':'success','data':quotes})
        resp.status = falcon.HTTP_200
        





    