from flask import render_template, redirect, flash
from models import db, Feedback
from forms import FeedbackForm
from helpers import confirm_user
from controllers.feedback import add_feedback_controller, update_feedback_controller, delete_feedback_controller

def feedback_routes(app):

    @app.route('/users/<username>/feedback/add', methods=['POST','GET'])      
    def add_feedback(username):
        add_feedback_controller(username)

    @app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
    def update_feedback(feedback_id):
        update_feedback_controller(feedback_id)

    @app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
    def delete_feedback(feedback_id):
        delete_feedback_controller(feedback_id)