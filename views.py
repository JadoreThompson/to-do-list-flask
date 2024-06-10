from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from api import User, LoginUser
import requests

views = Blueprint('views', __name__)
base_url = "http://localhost:8080/"


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password']
        )

        # Call the register function from api.py
        endpoint = "register"
        url = base_url + endpoint
        response = requests.post(url, json=new_user.dict())
        print(response.json())

        return redirect(url_for('views.login'))

    return render_template('register.html')

@views.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = LoginUser(
            email=request.form['email'],
            password=request.form['password']
        )

        # Call the login function from api.py
        endpoint = "login"
        url = base_url + endpoint
        response = requests.post(url, json=user)
        print(response.json())

        return redirect(url_for('views.dashboard'))

    return render_template('login.html')

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@views.route('/tasks/create')
def create_task():
    return render_template('create_task.html')

@views.route('/tasks/update/<int:task_id>')
def update_task(task_id):
    return render_template('update_task.html')