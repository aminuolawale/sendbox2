from mongoengine import connect
from sendbox.main.resources import HomeResource
from sendbox.users.resources import CRUDUser, MakeAdmin, MakeCourier, LoginUser
from sendbox.quotes.resources import CRUDQuote, GetQuote
from sendbox.shipments.resources import CRUDShipment, PayForShipment, AcceptShipment, VerifyShipment, CompleteShipment
from sendbox.middleware.auth import AuthMiddleware
import falcon
connect('sendbox', host="mongodb://localhost/sendbox", port=27017)
print('connected to database successfully')

app = falcon.API(middleware=AuthMiddleware())

app.add_route('/',HomeResource())
app.add_route('/home', HomeResource())
app.add_route('/users',CRUDUser())
app.add_route('/user/{user_id}',CRUDUser())
app.add_route('/login',LoginUser())
app.add_route('/user/courier/{user_id}', MakeCourier())
app.add_route('/user/admin/{user_id}', MakeAdmin())
app.add_route('/quotes',CRUDQuote())
app.add_route('/quote/{quote_id}',CRUDQuote())
app.add_route('/quote',GetQuote())
app.add_route('/shipments', CRUDShipment())
app.add_route('/shipments/{shipment_id}', CRUDShipment())
app.add_route('/shipment/accept/{shipment_id}', AcceptShipment())
app.add_route('/shipment/pay/{shipment_id}', PayForShipment())
app.add_route('/shipment/verify/{shipment_id}',VerifyShipment())
app.add_route('/shipment/complete/{shipment_id}', CompleteShipment())
