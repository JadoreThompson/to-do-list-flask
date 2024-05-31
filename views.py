from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Task, db
from datetime import datetime
import mail
import asyncio


views = Blueprint('views', __name__)


async def send_email_to_user(current_date):
    due_tasks = Task.query.filter_by(due_date=current_date).all()
    for task in due_tasks:
        mail.send_email(task.name, task.email)

    await asyncio.sleep(1)


current_date = datetime.now().date()
send_email_to_user(current_date)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password = generate_password_hash(password)


        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('views.login'))

    return render_template('register.html')

# @views.route('/login', method=['GET', 'POST'])
# def login():
#     if request.method == "POST":
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)
#
#         user_account = User.query.filter_by(email=email).first()
#
#         if user_account:
#             if check_password_hash(hashed_password, password):
#                 session['user_id'] = user_account.id
#                 return redirect(url_for('dashboard'))
#
#     return render_template('login.html')

@views.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user_account = User.query.filter_by(email=email).first()
        if user_account:
            if check_password_hash(user_account.password, password):
                session['user_id'] = user_account.id
                return redirect(url_for('views.dashboard',user_id=user_account.id))
            else:
                flash('Incorrect password')

    return render_template('login.html')

@views.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    session['user_id'] = user_id

    all_tasks = Task.query.filter_by(user_id=session['user_id']).all()
    user = User.query.get(user_id)

    return render_template('dashboard.html', all_tasks=all_tasks,user=user)

@views.route('/create-task/<int:user_id>', methods=['POST'])
def create_task(user_id):

    title = request.form['title']
    desc = request.form['desc']
    dueDate = request.form['due_date']

    new_task = Task(user_id=user_id, title=title, desc=desc, dueDate=dueDate)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('views.dashboard'))

@views.route('/update-task/<int:user_id>/<int:task_id>', methods=['POST'])
def update_task(task_id):

        task = Task.query.filter_by(id=task_id).first()

        if not task:
            flash('Task does not exist', category='error')

        if request.method == 'POST':
            task.title = request.form['title']
            task.desc = request.form['desc']
            task.dueDate = request.form['due_date']

            db.session.commit()

            return redirect(url_for('views.dashboard'))

        return render_template('update_task.html', task=task)

@views.route('/delete-task/<int:user_id>/<int:task_id>', methods=['POST'])
def delete_task(user_id, task_id):
    task = Task.query.filter_by(user_id=user_id, id=task_id).first()

    if not task:
        flash('Task does not exist', category='error')

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('views.dashboard'))
