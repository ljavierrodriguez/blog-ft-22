import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User, Article

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASEURI')

db.init_app(app) # vinculamos nuestro archivo models con nuestra app
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
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

# inicializador de nuestra api
if __name__ == '__main__':
    app.run()