from .model import Shipment
from .utils import load_shipment, load_client, verify_courier
import falcon
import json
import requests

class CRUDShipment(object):
    def on_post(self, req, resp):
        shipment_data = req.media
        shipment_data['client_id'] = req.context['user']['id']
        shipment = Shipment.objects.create(**shipment_data)
        shipment.update_price()
        shipment.save()
        resp.body = json.dumps({'status':True,'message':'shipment created successfully', 'data':shipment.format()}) 
        resp.status = falcon.HTTP_201
    def on_get(self, req, resp, shipment_id=None):
        if shipment_id: 
            shipment = load_shipment(shipment_id)
            resp.body = json.dumps({'status':True, 'message':'success','data':shipment.format()})
            resp.status = falcon.HTTP_200
            return
        shipments = [ shipment.format() for shipment in Shipment.objects ]
        resp.body = json.dumps({'status':True, 'message':'success','data':shipments})
        resp.status = falcon.HTTP_200        
    def on_put(self, req, resp, shipment_id):
        shipment = load_shipment(shipment_id)
        shipment_data = req.media
        for key in shipment_data:
            shipment[key] = shipment_data[key]
        shipment.save()
        resp.body = json.dumps({'status':True, 'message':'successfully updated shipment','data':shipment})
        resp.status = falcon.HTTP_200   
    def on_delete(self, req, resp, shipment_id):
        shipment = load_shipment(shipment_id)
        shipment.delete()
        resp.body = json.dumps({'status':True, 'message':'successfully deleted shipment'})
        resp.status = falcon.HTTP_200 
        
class AcceptShipment(object):
    def on_put(self, req, resp, shipment_id):
        shipment = load_shipment(shipment_id)
        user_id = req.context['user']['id']
        verify_courier(shipment, user_id)
        shipment['is_accepted'] = True
        shipment.save()
        resp.body = json.dumps({'status':True, 'message':'successfully accepted shipment'})
        resp.status = falcon.HTTP_200 

class PayForShipment(object):
    def on_put(self, req, resp, shipment_id):
        shipment = load_shipment(shipment_id)
        if not shipment['is_accepted']:
            resp.body = json.dumps({'status':False, 'message':'Courier must accept booking before shipment is paid'})
            resp.status = falcon.HTTP_400
            return
        user_id = req.context['user']['id']
        client = load_client(shipment,user_id)
        amount = shipment['total_price']
        email = client['email']
        payment_details = {'amount':amount, 'email':email}
        API_KEY = 'Bearer sk_test_4929b051d09cf8291b9820f445198737f44503bd'
        url = 'https://api.paystack.co/transaction/initialize'
        response = requests.post(url,json=payment_details,headers={'Authorization':API_KEY,'Content-Type':'application/json'})
        data = response.json()['data']
        authorization_url = data['authorization_url']
        access_code = data['access_code']
        reference = data['reference']
        payment_prompt = {'authorization_url':authorization_url,'access_code':access_code,'reference':reference}
        resp.body = json.dumps({'status':True,
                    'message':'payment initialized. client should follow authorization url to complete payment',
                    'data':payment_prompt})
        resp.status = falcon.HTTP_200

class VerifyShipment(object):
    def on_put(self, req, resp, shipment_id):
        shipment = load_shipment(shipment_id)
        user_id = req.context['user']['id']
        client = load_client(shipment, user_id)
        url = 'https://api.paystack.co/transaction/verify/{}'.format(shipment['payment_ref'])
        API_KEY = 'Bearer sk_test_4929b051d09cf8291b9820f445198737f44503bd'
        response = requests.get(url,headers={'Authorization':API_KEY})
        print(response.json())
        data = response.json()['data']
        status = data['status']
        if not status:
            resp.body = json.dumps({'status':False, 'message':'payment unsuccessful'})
            resp.status = falcon.HTTP_500
            return
        shipment['is_paid'] = True
        shipment.save()
        resp.body = json.dumps({'status':True, 'message':'payment successful'})
        resp.status = falcon.HTTP_200
        
 








             