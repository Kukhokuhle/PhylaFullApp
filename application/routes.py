#import the app object from __init__.py file
from application import app, db
from flask import render_template, request, Response, json, redirect, flash
from application.models import User, Patient
from application.forms import LoginForm, RegistrationForm, AddingPatientForm

# @app.route("/sort_patients", methods=['GET', 'POST'])
# def sort_patients():

@app.route("/search_patient", methods=['GET', 'POST'])
def search_patient():
    logged_in     = True
    patientName   = request.args.get('patientName')
    patientsFound = Patient.objects(name=patientName).all() #get list of patients with given name

    if patientsFound:
        atLeastOnePatientFound = True
        numberOfPatientsFound  = patientsFound.count() #get number of patients found
        flash(f"{numberOfPatientsFound} patient(s) found.", "success")
    else:
        atLeastOnePatientFound = False
        flash("Patient could not be found.", "warning")
        return redirect("/patients")

    return render_template("patients.html", patients=True,
    numberOfPatientsFound=numberOfPatientsFound, patientsFound=patientsFound,
    atLeastOnePatientFound=atLeastOnePatientFound)

@app.route("/", methods=['GET', 'POST'] ) #route to run app
@app.route("/index", methods=['GET', 'POST'] )
@app.route("/login", methods=['GET', 'POST'] )  #index is the login page
def index():             #index is the login page
    logged_in = False
    form      = LoginForm()  #form is an instance of the LoginForm class
    title     = "Login"

    if form.validate_on_submit():
        #get the email and password from the FORM
        email          =    form.email.data
        password       =    form.password.data

        #check if email and password from the FORM exist in the DATABASE
        #get the 1st user in the db with email matching the email entered in FORM
        userInDatabase = User.objects(email=email).first() 
        
        if userInDatabase:
            #the email entered in FORM does exist in DATABASE
            #now check if the corresponding passwords match
            if userInDatabase.compare_passwords(password):
                #passwords match
                flash(f"You are successfully logged in { userInDatabase.first_name }!", "success")

                return redirect("/home") #take legitimate user to the home page

            else:
                flash("Incorrect email or password", "danger")    

        else:
            flash("Incorrect email or password", "danger")

    return render_template("index.html", title=title, form=form, index=True, logged_in=logged_in)

@app.route("/patients", methods=['GET', 'POST'])
def patients():
     #default is sorting by name in ascending order
    patientsInDatabase = Patient.objects.all().order_by("name")

    #sort the patients by? (name or registration date)
    sort_by = request.args.get('sort_by')
    order   = request.args.get('order')

    if ((sort_by=="name") and (order=="ascending")):
        patientsInDatabase = Patient.objects.all().order_by("name") #all patients ordered by name or registration date

    elif ((sort_by=="name") and (order=="descending")):
        patientsInDatabase = Patient.objects.all().order_by("-name")

    elif ((sort_by=="registrationDate") and (order=="ascending")):
        patientsInDatabase = Patient.objects.all().order_by("registrationDate")

    elif ((sort_by=="registrationDate") and (order=="descending")):
        patientsInDatabase = Patient.objects.all().order_by("-registrationDate")


    logged_in = True
    title     = "Patients"
    return render_template("patients.html", patientData=patientsInDatabase, title=title, patients=True, logged_in=logged_in)

@app.route("/register", methods=['GET', 'POST'])
def register():
    logged_in = False
    form      = RegistrationForm()  #form is an instance of the RegistrationForm class
    title     = "Register"

    if form.validate_on_submit():
        
        #get the ID for this new user who is registering
        lastUserId = User.objects.count() #get number of users already in database
        newUserId = lastUserId + 1

        #get the new user's credentials
        newUserFirst_name = form.first_name.data
        newUserLast_name  = form.last_name.data
        newUserEmail      = form.email.data
        newUserPassword   = form.password.data

        #create a new user object and save it to the database
        newUser   = User(user_id = newUserId, first_name = newUserFirst_name, 
                         last_name = newUserLast_name, email = newUserEmail)

        #hash password and assign it to the new user object
        newUser.hash_and_set_password( newUserPassword )

        #save the new user object to the database
        newUser.save()

        flash(f"{newUserFirst_name}, you are successfully registered! You can now login." , "success")

        return redirect("/index")
        
    return render_template("register.html", title=title, form=form, register=True, logged_in=logged_in)

@app.route("/home")   #This is the route to the Home page
def home():  

    logged_in = True  #in the Home Page, you are logged in (logged_in=True)
    title     = "Make The Promise, We'll Deliver"

    return render_template("home.html", title=title, home=True, logged_in=logged_in)

@app.route("/add_patient", methods=['GET', 'POST'])
def add_patient():
    logged_in=True  #you are logged in (logged_in=True)
    title = "Add Patient"

    form = AddingPatientForm()

    if form.validate_on_submit():
        #get the new patient's credentials
        newPatientName             = form.name.data
        newPatientSurname          = form.surname.data
        NewPatientPhoneNumber      = form.phone_number.data
        NewPatientAddress          = form.address.data
        NewPatientClinic           = form.clinic.data
        NewPatientRegistrationDate = form.registrationDate.data
        newPatientEmail            = form.email.data   #WILL USE LATER
        
        #create a new patient object and save it to the database
        newPatient = Patient(name = newPatientName, surname = newPatientSurname, 
        phone_number = NewPatientPhoneNumber, address = NewPatientAddress,
        clinic = NewPatientClinic, registrationDate = NewPatientRegistrationDate)

        #save the new patient object to the database
        newPatient.save()

        flash(f"{newPatientName} has been successfully registered." , "success")

        return redirect("/patients")

    return render_template("add_patient.html", form=form, add_patient=True, title=title, logged_in=logged_in)

@app.route("/orders", methods=['GET', 'POST'])
def orders():
    logged_in = True
    title     = "Orders"
    return render_template("orders.html", title=title, orders=True, logged_in=logged_in)

    

