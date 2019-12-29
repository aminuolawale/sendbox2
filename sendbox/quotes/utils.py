from .model import Quote
import falcon

def is_duplicate(quote_data, user):
    origin = quote_data['origin']
    destination = quote_data['destination']
    courier_id = user['id']
    try:
        existing_quote = Quote.objects.get(origin=origin, destination=destination,courier_id=courier_id)
        return True
    except:
        return False
    
def load_quote(quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
        return quote
    except:
        description ={
                'status': False,
                'message': 'Invalid quote_id'
            }
        raise falcon.HTTPNotFound(description=description)
