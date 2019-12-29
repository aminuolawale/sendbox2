from .model import Shipment
from .utils import load_shipment, load_client
import falcon
import json

class CRUDShipment(object):
    def on_post(self, req, resp):
        shipment_data = req.media
        shipment_data['client_id'] = req.context['user']['id']
        shipment = Shipment.objects.create(**shipment_data)
        shipment.save()
        resp.body = json.dumps({'status':True,'message':'shipment created successfully', 'data':shipment.format()}) 
        resp.status = falcon.HTTP_201
    def on_get(self, req, resp, shipment_id):
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
        courier = load_courier(shipment)
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
        client = load_client(shipment)
        








             