from flask import redirect
from routes import route_auth
from routes import route_feedback
from routes import route_users

def all_routes(app):

    @app.route('/')
    def home_page():
      return redirect('/register')

    route_auth.auth_routes(app)
    route_users.user_routes(app)
    route_feedback.feedback_routes(app)