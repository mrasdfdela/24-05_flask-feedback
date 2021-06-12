from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import FeedbackForm, UserForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "letmehasfeedback"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

def confirm_user(username):
    s_username = session['username']
    return username == s_username

@app.route('/')
def home_page():
  return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    try: 
        if session['username']:
            s_username = session['username']
            return redirect(f'/users/{s_username}')
    except:
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

            session['username'] = new_user.username
            return redirect(f'/users/{new_user.username}')
        else:
            return render_template('/register.html', form=form)

# @app.route('/secret')
# def secret_site():
#     try:
#         if session['username']:
#             return render_template('/secret.html')
#     except:
#         return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
      if session['username']:
          s_username = session['username']
          return redirect(f'/users/{s_username}')
    except:
        form = UserForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            u = User.authenticate(username, password)

            if u:
                session['username'] = u.username
                return redirect('/secret')
            else:
                form.username.errors = ['Invalid username/password']
        else:
            return render_template('/login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>', methods=['GET'])
def user(username):
    if confirm_user(username):
        user = User.query.get_or_404(username)
        return render_template('/user.html', user=user)
    else:
        return redirect(f'/users/{username}')

@app.route('/users/<username>/delete', methods=['POST'])
def user_delete(username):
    if confirm_user(username):
        user = User.query.filter_by(username=username)
        feedback = Feedback.query.filter_by(username=username)
        feedback.delete()
        user.delete()
        db.session.commit()
        return redirect('/')
    else:
        return redirect(f'/users/{username}')

@app.route('/users/<username>/feedback/add', methods=['POST','GET'])      
def add_feedback(username):
    form = FeedbackForm()    
    if form.validate_on_submit() and confirm_user(username):
        title = form.title.data
        content = form.content.data        
        new_feedback = Feedback(title=title, content=content,username=username)

        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    elif confirm_user(username):
        return render_template('/feedback.html', username=username, form=form)
    else:
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit() and confirm_user(feedback.username):
        feedback.title = form.title.data
        feedback.content = form.content.data        
        db.session.commit()
    elif confirm_user(feedback.username):
        return render_template('/feedback_update.html', username=feedback.username, form=form)

    return redirect(f'/users/{feedback.username}')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback:
        Feedback.query.filter_by(id=feedback.id).delete()
        db.session.commit()
    return redirect(f'/users/{feedback.username}')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")