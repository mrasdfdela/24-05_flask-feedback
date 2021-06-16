from flask import render_template, redirect, session, flash
from models import db, User
from forms import UserForm
from controllers.auth import create_user, user_login

def auth_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        create_user()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        user_login()

    @app.route('/logout', methods=['GET'])
    def logout():
        session.pop('username')
        return redirect('/')