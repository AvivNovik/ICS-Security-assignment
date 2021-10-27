from flask import Flask, Blueprint
from user.models import User
from Tutorial import app


# routes that will be imported by the backend main page

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route("/user/signout")
def signout():
    return User().signout()


@app.route("/user/login", methods=['POST'])
def login():
    return User().login()


@app.route("/user/create_directory", methods=['GET'])
def create_directory():
    return User().create_directory()


@app.route("/user/delete_user", methods=['POST'])
def delete_user():
    return User().delete_user()
