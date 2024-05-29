from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Task

views = Blueprint('views', __name__)

@views.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@views.route('/create-task', methods=['POST', 'GET'])
def create_task():
    if request.method == "POST":
        def get_form_data():
            title = request.form.get('name')
            description = request.form.get('description')
            completed = bool(request.form.get('completed'))
            task = Task(title=title, description=description, done=completed)
            return task

        task = get_form_data()
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('create-task.html')

@views.route('/delete-task/<int:id>')
def delete_task(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/update-task/<int:id>', methods=['POST', 'GET'])
def update_task(id):
    task = Task.query.filter_by(id=id).first()

    if request.method == "POST":
        task.title = request.form.get('name')
        task.description = request.form.get('description')
        task.done = bool(request.form.get('completed'))


        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('update-task.html', task=task)
