from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Task

views = Blueprint('views', __name__)

@views.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)