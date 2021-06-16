from flask import render_template, redirect, flash
from models import db, User, Feedback
from helpers import confirm_user

def user_routes(app):

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