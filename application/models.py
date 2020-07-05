import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

#Each document (e.g a user, a course or an enrollment) lives inside a collection
#Each collection (e.g of users, of courses or of enrollments) lives inside a database

#The class User models a 'user'
class User(db.Document):
    user_id    = db.IntField( unique=True )
    first_name = db.StringField( max_length=50 )
    last_name  = db.StringField( max_length=50 )
    email      = db.StringField( max_length=50, unique=True)
    password   = db.StringField( )

    def hash_and_set_password(self, password):
        self.password = generate_password_hash(password)

    def compare_passwords(self, password):
        return check_password_hash(self.password, password)

#The class Patient models a patient
class Patient(db.Document):
    name             = db.StringField( max_length=25 )
    surname          = db.StringField( max_length=25 )
    phone_number     = db.StringField( max_length=10, unique=True )
    address          = db.StringField( )
    clinic           = db.StringField( max_length=50 )
    registrationDate = db.DateField( ) 
