from mongoengine import Document, StringField, FloatField, BooleanField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
    username   = StringField(min_length=3, required=True, unique=True)
    fullname   = StringField(required=True)
    email      = EmailField(required=True)
    password   = StringField(min_length=8, required=True)
    is_admin   = BooleanField(default=False)
    is_courier = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow())

    def format(self):
        user = {}
        user['id']         = str(self.id)
        user['username']   = self.username
        user['fullname']   = self.fullname
        user['email']      = self.email
        user['password']   = self.password
        user['is_admin']   = self.is_admin
        user['is_courier'] = self.is_courier
        user['created_at'] = self.created_at.strftime("%c")
        return user
    def reload(self):
        self = User.objects.get(id=self.id)

