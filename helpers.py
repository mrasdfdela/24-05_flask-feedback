from flask import session

def confirm_user(username):
    s_username = session['username']
    return username == s_username