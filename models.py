from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(80))
    sku = db.Column(db.String(80), unique=True, nullable=False)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(300))
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
