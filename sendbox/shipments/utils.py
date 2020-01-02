from .model import Shipment
from sendbox.quotes.model import Quote
from sendbox.users.model import User
from sendbox.quotes.utils import load_quote
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

def disallow_self_booking(shipment, user_id):
    quote_id = shipment['quote_id']
    quote = load_quote(quote_id)
    courier_id = quote['courier_id']
    user_id = ObjectId(user_id)
    if user_id == courier_id:
        description = {
            'status': False,
            'message':'User cannot book on own quote'
        }
        raise falcon.HTTPForbidden(description=description)
def payment_ready(shipment):
    if not shipment['is_accepted']: 
        description ={
            'status': False,
            'message':'Courier must accept booking before shipment is paid for'
        }
        raise falcon.HTTPForbidden(description=description)
    if shipment['payment_ref']:
        description ={
            'status': False,
            'message':'There is a pending payment on this shipment already. Please proceed to verify payment on this shipment'
        }
        raise falcon.HTTPForbidden(description=description)
def verification_ready(shipment):
    if not shipment['payment_ref']:
        description ={
            'status': False,
            'message':'There is no pending payment on this shipment. Please proceed to pay for this shipment'
        }
        raise falcon.HTTPForbidden(description=description)

def completion_ready(shipment):
    if not shipment['is_paid']:
        description = {
            'status': False,
            'message': 'Shipment must be paid for for this resource to be accessed'
        }
        raise falcon.HTTPForbidden(description=description)