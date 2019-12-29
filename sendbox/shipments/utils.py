from .model import Shipment
from sendbox.quotes.model import Quote
from sendbox.users.model import User
import falcon

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
def load_courier(shipment):
    quote_id = shipment['quote_id']
    quote = Quote.objects.get(id=quote_id)
    courier_id = quote['courier_id']
    courier = User.objects.get(id=courier_id)
    current_user_id = req.context['user']['id']
    if courier_id == current_user_id:
        return courier
    else:
        description ={
                'status': False,
                'message': 'You cannot access this resource'
            }
        raise falcon.HTTPForbidden(description=description)
def load_client(shipment):
    client_id = shipment['client']['id']
    client = User.objects.get(id=client_id)
    return client

