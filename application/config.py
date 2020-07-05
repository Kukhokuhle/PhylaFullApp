import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_string"

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }
    #we have a database called UTA_Enrollment in the MongoDB Compass
    #now, we have created an associated database object called db
    