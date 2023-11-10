from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

followers_table = db.Table(
    "followers", 
    db.Column("follower_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),   
    db.Column("followed_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)   
)

categories_articles = db.Table(
    "categories_articles",
    db.Column("articles_id", db.Integer, db.ForeignKey('articles.id'), nullable=False, primary_key=True),   
    db.Column("categories_id", db.Integer, db.ForeignKey('categories.id'), nullable=False, primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    lastlogin = db.Column(db.DateTime())
    profile = db.relationship("Profile", backref="user", uselist=False) # [<Profile 1>] => <Profile 1>
    articles = db.relationship("Article", backref="user")
    comments = db.relationship("Comment", backref="user")
    repplies = db.relationship("Reply", backref="user")
    
    # Esta relationship se crea asi cuando la tabla pivote o intermedia es una tabla dentro de models y no un modelo
    followers = db.relationship(
        "User", 
        secondary=followers_table, 
        primaryjoin=(followers_table.c.follower_id == id), 
        secondaryjoin=(followers_table.c.followed_id == id),  
        backref=db.backref("followeds", lazy="dynamic")
    )
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "active": self.active,
            "lastlogin": self.lastlogin,
            "followers": list(map(lambda follower: follower.username, self.followeds)),
            "followeds": list(map(lambda follower: follower.username, self.followers))
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default="")
    lastname = db.Column(db.String(120), default="")
    biography = db.Column(db.String(120), default="")
    github = db.Column(db.String(120), default="")
    facebook = db.Column(db.String(120), default="")
    twitter = db.Column(db.String(120), default="")
    instagram = db.Column(db.String(120), default="")
    avatar = db.Column(db.String(150), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    articles = db.relationship("Article", secondary=categories_articles)
    
    
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True) # Hola Mundo
    slug = db.Column(db.String(255), nullable=False, unique=True) # hola-mundo
    resume = db.Column(db.Text(), default="")
    content = db.Column(db.Text(), nullable=False)
    published = db.Column(db.Boolean(), default=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship("Comment", backref="article")
    medias = db.relationship("Media", backref="article")
    categories = db.relationship("Category", secondary=categories_articles)
    
    def serialize(self): 
        return {
            "id": self.id,
            "title": self.title,
            "categories": list(map(lambda category: category.name, self.categories)),
            "comments": len(self.comments)
        }
    
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())
    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    repplies = db.relationship("Reply", backref="comments")
    
    
class Reply(db.Model):
    __tablename__ = 'repplies'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())
    comments_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    
class Media(db.Model):
    __tablename__ = 'medias'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)


