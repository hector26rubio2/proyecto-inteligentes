from flask import Flask
from flask_cors import CORS
from routes.my_routes import my_routes

app = Flask(__name__)

app.register_blueprint(my_routes)
cors = CORS(app)

if __name__ == '__main__':
    app.run(debug=False, port=9000)
