from mongoengine import Document, StringField, FloatField, ObjectIdField
from ..users.model import User

class Quote(Document):
    origin = StringField(required=True)
    destination = StringField(required=True)
    price_per_kg = FloatField(required=True)
    courier_id = ObjectIdField(required=True)


    def format(self):
        quote = {}
        quote['id'] = str(self.id)
        quote['origin'] = self.origin
        quote['destination'] = self.destination
        quote['price_per_kg'] = self.price_per_kg
        quote['courier'] = User.objects.get(id=self.courier_id).format()
        return quote