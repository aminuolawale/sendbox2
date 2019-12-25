from mongoengine import Document, StringField, FloatField, BooleanField, EmailField

class User(Document):
    username = StringField(min_length=3, required=True, unique=True)
    fullname = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(min_length=8, required=True)
    is_admin = BooleanField(default=False)
    is_courier = BooleanField(default=False)

    def format(self):
        user = {}
        user['id'] = str(self.id)
        user['username'] = self.username
        user['fullname'] = self.fullname
        user['email'] = self.email
        user['password'] = self.password
        user['is_admin'] = self.is_admin
        user['is_courier'] = self.is_courier
        return user

