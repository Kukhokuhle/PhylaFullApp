from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User

#create LoginForm and RegistrationForm classes
class LoginForm(FlaskForm):
    email       = StringField( "Email", validators=[ DataRequired(), Email() ] )
    password    = PasswordField( "Password", validators=[ DataRequired(), Length(min=6, max=15) ] )
    remember_me = BooleanField( "Remember me" )
    submit      = SubmitField( "Login" )

class RegistrationForm(FlaskForm):
    first_name          = StringField( "First Name", validators=[ DataRequired(), Length(min=2, max=55)    ] )
    last_name           = StringField( "Last Name", validators=[ DataRequired(), Length(min=2, max=55)     ] )
    email               = StringField( "Email", validators=[ DataRequired() ] )
    password            = PasswordField( "Password", validators=[ DataRequired(), Length(min=6, max=15)      ] )
    confirming_password = PasswordField( "Confirm Password", validators=[ DataRequired(), Length(min=6, max=15), EqualTo('password')   ] )
    register            = SubmitField( "Register Now" )

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please enter another one.")

class AddingPatientForm(FlaskForm):
    name                = StringField( "Name", validators=[ DataRequired(), Length(min=2, max=55)    ] )
    surname             = StringField( "Surname", validators=[ DataRequired(), Length(min=2, max=55)     ] )
    phone_number        = StringField( "Phone Number", validators=[ DataRequired(), Length(min=10, max=10) ] )
    email               = StringField( "Email" )
    address             = StringField( "Address", validators=[ DataRequired() ] )
    clinic              = StringField( "Clinic", validators=[ DataRequired() ] )
    registrationDate    = DateField( "Registration Date", format='%d/%m/%Y', validators=[ DataRequired() ] )
    registerPatient     = SubmitField( "Register Patient" )

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please enter another one.")
    
    # def validate_phone_number(self, phone_number):
    #     user = User.objects(phone_number=phone_number.data).first()
    #     if user:
    #         raise ValidationError("Phone Number is already in use. Please enter another one.")
    
    


