from mongoengine import Document, StringField, FloatField, BooleanField, ObjectIdField, DateTimeField
from sendbox.quotes.model import Quote
from sendbox.users.model import User
from datetime import datetime
import falcon
class Shipment(Document):
    origin       = StringField(required=True)
    destination  = StringField(required=True)
    weight       = FloatField(min_value=0.00, required=True)
    quote_id     = ObjectIdField(required=True)
    client_id    = ObjectIdField(required=True)
    is_accepted  = BooleanField(default=False)
    is_paid      = BooleanField(default=False)
    is_completed = BooleanField(default=False)
    total_price  = FloatField(default=0.00)
    payment_ref  = StringField(default=None)
    created_at   = DateTimeField(default=datetime.utcnow())

    def update_price(self):
        quote = Quote.objects.get(id=self.quote_id)
        self.total_price = quote['price_per_kg'] *self.weight
        self.save()

    def format(self):
        shipment = {}
        shipment['id']           = str(self.id)
        shipment['origin']       = self.origin
        shipment['destination']  = self.destination
        shipment['weight']       = self.weight
        shipment['quote']        = self.fetch_quote().format()
        shipment['client']       = self.fetch_user().format()
        shipment['is_accepted']  = self.is_accepted
        shipment['is_paid']      = self.is_paid
        shipment['is_completed'] = self.is_completed
        shipment['total_price']  = self.total_price
        shipment['payment_ref']  = self.payment_ref
        shipment['created_at']   = self.created_at.strftime("%c")
        return shipment
    
    def fetch_user(self):
        try:
            user = User.objects.get(id=self.client_id)
        except:
            return None
        return user
    def fetch_quote(self):
        try:
            quote = Quote.objects.get(id=self.quote_id)
        except:
            return None
        return quote

