from .model import Shipment
import falcon
import json

class CRUDShipment(object):
    def on_post(self, req, resp):
        shipment_data = req.media
        shipment_data['client_id'] = req.context['user']['id']
        shipment = Shipment.objects.create(**shipment_data)
        shipment.save()
        resp.body = json.dumps({'status':True,'message':'shipment created successfully', 'data':shipment.format()}) 
        resp.status = 