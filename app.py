from flask import Flask, render_template, url_for, redirect, session, jsonify
import pymongo
from functools import wraps

app = Flask(__name__)
# A random key generated beforehand
app.secret_key = b'\x80Xt\xc1\x87\xa5\xf4\x04\x9c\xcdG\x1e\x02\rN\xde'

# Database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.db


# Decorator
def login_required(f):
    # Checks if the session contains the key 'logged_in' which is entered after logging in to the system
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return wrap


def admin_required(f):
    # Checks if user is logged in and has the access role 'admin'.
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['user']['access_role'] == 'admin':
            return f(*args, **kwargs)
        else:
            return jsonify(({"error": "admin permissions required"})), 400,

    return wrap


# Imports all the routes from the routes page
from user import routes


@app.route("/")
def Login():
    return render_template('login.html')


@app.route("/register/")
def register():
    return render_template('registration.html')


@app.route("/home/")
@login_required
def home_page():
    return render_template('home.html')



