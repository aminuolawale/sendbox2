from .model import Quote

def is_duplicate(quote_data, user):
    origin = quote_data['origin']
    destination = quote_data['destination']
    courier_id = user['id']
    try:
        existing_quote = Quote.objects.get(origin=origin, destination=destination,courier_id=courier_id)
        return True
    except:
        return False