from flask import render_template, redirect, session, flash
from models import db, User
from forms import UserForm

def create_user():
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
            import pdb
            pdb.set_trace()
            return render_template('register.html', form=form)

def user_login():
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