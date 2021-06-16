from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import FeedbackForm, UserForm
from routes.main import all_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "letmehasfeedback"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
all_routes(app)
toolbar = DebugToolbarExtension(app)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")