from mongoengine import Document, StringField, FloatField, BooleanField, ObjectIdField
from sendbox.quotes.model import Quote
from sendbox.users.model import User
class Shipment(Document):
    origin       = StringField(required=True)
    destination  = StringField(required=True)
    weight       = FloatField(min_value=0.00, required=True)
    quote_id     = ObjectIdField(required=True)
    client_id    = ObjectIdField(required=True)
    is_accepted  = BooleanField(default=False)
    is_paid      = BooleanField(default=False)
    is_completed = BooleanField(default=False)
    total_price  = FloatField(default=self.fetch_quote()['price_per_kg']*weight)


    def format(self):
        shipment = {}
        shipment['origin']       = self.origin
        shipment['destination']  = self.destination
        shipment['weight']       = self.weight
        shipment['quote']        = self.fetch_quote()
        shipment['client']       = self.fetch_user()
        shipment['is_paid']      = self.is_paid
        shipment['is_accepted']  = self.is_accepted
        shipment['is_completed'] = self.is_completed
        shipment['total_price']  = self.total_price

    def fetch_user(self):
        try:
            user = User.objects.get(id=self.client_id)
        except:
            return None
        return User
    def fetch_quote(self):
        try:
            quote = Quote.objects.get(id=self.quote_id)
        except:
            return None
        return quote

