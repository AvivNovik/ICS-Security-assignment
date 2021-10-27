from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from Tutorial import db, login_required, admin_required
import uuid
import os


class User:

    def start_session(self, user):
        # Delete the password so it wont be seen on the client side
        del user['password']

        # Relating the user to the session
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "access_role": request.form.get("access_role")
        }

        # encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing username
        if db.users.find_one({"username": user["username"]}):
            return jsonify({"error": "Username already exists"}), 400
        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify(({"error": "Signup failed"})), 400

    def signout(self):
        session.clear()
        return redirect("/")

    def login(self):
        # Check for existing username
        user = db.users.find_one({"username": request.form.get('username')})

        # Verify the password
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        else:
            return jsonify(({"error": "Username or password are incorrect"})), 400

    @admin_required
    def create_directory(self):
        # Creates a directory names 'ICS Security' on C:/ if the request's source has admin permissions.
        directory = "ICS Security"
        parent_dir = "C:/"
        path = os.path.join(parent_dir, directory)
        try:
            os.mkdir(path)
            return jsonify({"status": "success"}), 200
        except OSError as error:
            return jsonify(({"error": error.__str__()})), 400

    @login_required
    def delete_user(self):
        # Delete the user that the request's source is logged on to.
        user = session['user']
        if db.users.delete_one({"username": user['username']}):
            return jsonify({"status": "success"}), 200
        else:
            return jsonify(({"error": "deletion was failed"})), 400

    @login_required
    def edit_user(self):
        # reads from the html page the desired credentials
        # and change the request's source user's credentials in the database accordingly.
        user = session['user']
        new_username = request.form.get("new_username")
        new_password = request.form.get("new_password")
        new_access_role = request.form.get("new_access_role")

        if db.users.find_one_and_update({"username": user['username']},
                                        {"username": new_username, "password": new_password, "access_role": new_access_role}):
            return jsonify({"status": "success"}), 200
        else:
            return jsonify(({"error": "Could not change the credentials successfully"})), 400





