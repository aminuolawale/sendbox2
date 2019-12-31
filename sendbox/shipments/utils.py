from .model import Shipment
from sendbox.quotes.model import Quote
from sendbox.users.model import User
import falcon
from bson import ObjectId

def load_shipment(shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)
        return shipment
    except:
        description ={
                'status': False,
                'message': 'Invalid shipment_id'
            }
        raise falcon.HTTPNotFound(description=description)
def verify_courier(shipment, user_id):
    quote_id = shipment['quote_id']
    quote = Quote.objects.get(id=quote_id)
    courier_id = quote['courier_id']
    courier = User.objects.get(id=courier_id)
    user_id = ObjectId(user_id)
    if courier_id == user_id:
        return courier
    else:
        description ={
                'status': False,
                'message': 'You cannot access this resource'
            }
        raise falcon.HTTPForbidden(description=description)

def load_client(shipment, user_id):
    client_id = shipment['client_id']
    user_id = ObjectId(user_id)
    client = User.objects.get(id=client_id)
    if client_id == user_id:
        return client
    else:
        description ={
                'status': False,
                'message': 'You cannot access this resource'
            }
        raise falcon.HTTPForbidden(description=description)


