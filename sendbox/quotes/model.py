from mongoengine import Document, StringField, FloatField, ObjectIdField, DateTimeField
from ..users.model import User
from datetime import datetime

class Quote(Document):
    origin       = StringField(required=True)
    destination  = StringField(required=True)
    price_per_kg = FloatField(required=True)
    courier_id   = ObjectIdField(required=True)
    created_at   = DateTimeField(default=datetime.utcnow())


    def format(self):
        quote = {}
        quote['id']           = str(self.id)
        quote['origin']       = self.origin
        quote['destination']  = self.destination
        quote['price_per_kg'] = self.price_per_kg
        quote['courier']      = User.objects.get(id=self.courier_id).format()
        quote['created_at']   = self.created_at.strftime("%c")
        return quote