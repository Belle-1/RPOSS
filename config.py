# config.py

"""
This file should contain one variable assignment per line. 
When the app is initialized, the variables in this file will
be used to configure Flask and its extensions are accessible 
via the "app.config" dictionary e.g."app.config['DEBUG']"

--

Those configuration variables can be used by flask, extensions or me.

# app.py or app/__init__.py
from flask import Flask
 
app = Flask(__name__)
app.config.from_object('config')

# so now i can access the configuration variables via app.config["VAR_NAME"]

--

BCRYPT_LOG_ROUNDS | If you are using Flask-Bcrypt to hash your passwords, 
you'll need to specify the number of "rounds" that the algorithm executes
in hashing a password. The more rounds used to hash a password, the 
longer it'll take for an attacker to guess a password given a hash.
"""

DEBUG = False  # turns off debugging features in Flask

BCRYPT_LOG_ROUNDS = 12

SQLALCHEMY_TRACK_MODIFICATIONS = False
