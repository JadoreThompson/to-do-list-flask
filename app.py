from flask import Flask
from views import views
import uvicorn

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"
app.register_blueprint(views)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
