from mongoengine import connect
from sendbox.main.resources import HomeResource
from sendbox.users.resources import CRUDUser, CourierUser, AdminUser, LoginUser
from sendbox.quotes.resources import CRUDQuote, GetQuote
from sendbox.middleware.auth import AuthMiddleware
import falcon
connect('sendbox', host="mongodb://localhost/sendbox", port=27017)


app = falcon.API(middleware=AuthMiddleware())

app.add_route('/',HomeResource())
app.add_route('/home', HomeResource())
app.add_route('/users',CRUDUser())
app.add_route('/user/{user_id}',CRUDUser())
app.add_route('/login',LoginUser())
app.add_route('/user/courier/{user_id}', CourierUser())
app.add_route('/user/admin/{user_id}', AdminUser())
app.add_route('/quotes',CRUDQuote())
app.add_route('/quote/{quote_id}',CRUDQuote())
app.add_route('/quote',GetQuote())
