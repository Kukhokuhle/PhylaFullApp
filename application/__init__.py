from flask import Flask #Flask being the class

from application.config import Config
from flask_mongoengine import MongoEngine

#create the app object
app = Flask(__name__) #name refers to the current module
app.config.from_object(Config)

#create the database object
db = MongoEngine()
db.init_app(app)

#import the routes.py file
from application import routes