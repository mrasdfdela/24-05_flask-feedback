from flask import render_template, redirect, flash
from models import db, Feedback
from forms import FeedbackForm
from helpers import confirm_user

def add_feedback_controller(username):
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
def update_feedback_controller(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit() and confirm_user(feedback.username):
        feedback.title = form.title.data
        feedback.content = form.content.data        
        db.session.commit()
    elif confirm_user(feedback.username):
        return render_template('/feedback_update.html', username=feedback.username, form=form)

    return redirect(f'/users/{feedback.username}')
def delete_feedback_controller(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback:
        Feedback.query.filter_by(id=feedback.id).delete()
        db.session.commit()
    return redirect(f'/users/{feedback.username}')