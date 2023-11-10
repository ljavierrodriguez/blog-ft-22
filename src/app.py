import os
import datetime
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User, Article, Profile
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASEURI')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app) # vinculamos nuestro archivo models con nuestra app
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)

# Definir rutas de nuestra api (endpoints)

@app.route('/')
def main():
    
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    
    return jsonify(users), 200

@app.route('/articles')
def get_articles():
    
    articles = Article.query.all()
    articles = list(map(lambda article: article.serialize(), articles))
    
    return jsonify(articles), 200

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username:
        return jsonify({ "msg": "username is required!"}), 400
    
    if not password:
        return jsonify({ "msg": "passeword is required!"}), 400
    
    userFound = User.query.filter_by(username=username).first()
    
    if not userFound:
        return jsonify({ "msg": "Bad credentials!"}), 401
    
    if not check_password_hash(userFound.password, password):
        return jsonify({ "msg": "Bad credentials!"}), 401
    
    expires = datetime.timedelta(days=3)
    access_token = create_access_token(identity=userFound.id, expires_delta=expires)
    
    data = {
        "success": "Login successfully!",
        "access_token": access_token,
        "type": "Bearer",
        "user": userFound.serialize()
    }
    
    return jsonify(data), 200

@app.route('/api/register', methods=['POST'])
def register():
    
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username:
        return jsonify({ "msg": "username is required!"}), 400
    
    if not password:
        return jsonify({ "msg": "passeword is required!"}), 400
    
    userFound = User.query.filter_by(username=username).first()
    
    if userFound:
        return jsonify({ "msg": "username already exists!"}), 400
    
    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.active = True
    
    profile = Profile()
    user.profile = profile
    
    user.save() 
    
    if not user:
        return jsonify({ "msg": "Error, Please try again"}), 400
    
    expires = datetime.timedelta(days=3)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    
    data = {
        "success": "Register successfully!",
        "access_token": access_token,
        "type": "Bearer",
        "user": user.serialize()
    }
    
    return jsonify(data), 200
    
    
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    profile = Profile.query.filter_by(users_id=id).first()
    
    data = {
        "success": "Profile Loaded",
        "profile": profile.serialize()
    }
    
    return jsonify(data), 200

# inicializador de nuestra api
if __name__ == '__main__':
    app.run()