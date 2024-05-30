from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Task

views = Blueprint('views', __name__)


@views.route('/')
def home():
    tasks = Task.query.filter_by(done=0).all()
    print("Tasks", tasks)

    return render_template('home.html', tasks=tasks)


@views.route('/create-task', methods=['POST', 'GET'])
def create_task():
    if request.method == "POST":
        def get_form_data():
            title = request.form['name']
            description = request.form['description']
            completed = request.form['completed']

            print("Title", title)
            print("Description", description)
            print("Completed", completed)

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
    task = Task.query.get(id)
    if task:
        if request.method == "POST":
            title = request.form.get('name')
            description = request.form.get('description')
            done = bool(request.form.get('completed'))

            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if done is not None:
                task.done = done

            task.verified = True
            db.session.commit()

            return redirect(url_for('views.home'))
    else:
        return "Task not found!", 404

    return render_template('update-task.html', task=task)
