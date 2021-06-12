from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "letmehasfeedback"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect('/secret')
    else:
        return render_template('/register.html', form=form)

@app.route('/secret')
def secret_site():
    return render_template('/secret.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.authenticate(username, password)

        if u:
            session['user_id'] = u.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password']
    else:
        return render_template('/login.html', form=form)