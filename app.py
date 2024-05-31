from flask import Flask
from views import views
from models import db

app = Flask(__name__)
app.register_blueprint(views)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()