from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Tasks
from datetime import datetime
import mail


views = Blueprint('views',  __name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/register', method=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']

        password = request.form['password']
        password = generate_password_hash(password)

        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@views.route('/login', method=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']

        password = request.form['password']
        hashed_password = generate_password_hash(password)

        user_account = Users.query.filter_by(email=email).first()

        if user_account:
            if check_password_hash(hashed_password, password):
                session['user_id'] = user_account.id
                return redirect(url_for('dashboard'))

    return render_template('login.html')

@views.route('/dashboard/<int:user_id>', method=['GET', 'POST'])
def dashboard(user_id):
    tasks = Tasks.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', tasks=tasks)



@views.route('/create-task/<int:user_id>', method=['POST'])
def create_task(user_id):

    title = request.form['title']
    desc = request.form['desc']
    dueDate = request.form['dueDate']

    new_task = Tasks(user_id=user_id, title=title, desc=desc, dueDate=dueDate)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('dashboard'))

@views.route('/update-task/<int:task_id>', method=['POST'])
def update_task(task_id):

        task = Tasks.query.filter_by(id=task_id).first()

        if not task:
            flash('Task does not exist', category='error')

        task.title = request.form['title']
        task.desc = request.form['desc']
        task.dueDate = request.form['dueDate']

        db.session.commit()

        return redirect(url_for('dashboard'))


@views.route('/delete-task/<int:task_id>', method=['POST'])
def delete_task(task_id):

    task = Tasks.query.filter_by(id=task_id).first()

    if not task:
        flash('Task does not exist', category='error')

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('dashboard'))


