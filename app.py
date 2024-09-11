from flask import Flask
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from models import User, db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

db.init_app(app)

from services.user_service import UserService
user_service = UserService({'User': User})

from gateway import Gateway
gateway = Gateway({
    'user_service': user_service,
})
gateway.set_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
