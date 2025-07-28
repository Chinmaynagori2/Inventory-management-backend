from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from models import db, User, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-key'

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()


def create_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def verify_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['username']
    except Exception:
        return None


def require_auth(f):
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization required'}), 401
        token = auth_header.split(' ')[1]
        user = verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    new_user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201  


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_token(user.username)
    return jsonify({'access_token': token}), 200


@app.route('/products', methods=['POST'])
@require_auth
def add_product(username):
    data = request.json
    product = Product(
        name=data['name'],
        type=data.get('type'),
        sku=data['sku'],
        image_url=data.get('image_url'),
        description=data.get('description'),
        quantity=data['quantity'],
        price=data['price']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'product_id': product.id}), 201


@app.route('/products/<int:pid>/quantity', methods=['PUT'])
@require_auth
def update_quantity(username, pid):
    data = request.json
    product = Product.query.get(pid)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product.quantity = data['quantity']
    db.session.commit()
    # response must include updated quantity field, so test script passes
    resp = {
        'product_id': product.id,
        'quantity': product.quantity
    }
    return jsonify(resp), 200


@app.route('/products', methods=['GET'])
@require_auth
def get_products(username):
    products = Product.query.all()
    all_products = [{
        'id': p.id,
        'name': p.name,
        'type': p.type,
        'sku': p.sku,
        'image_url': p.image_url,
        'description': p.description,
        'quantity': p.quantity,
        'price': p.price
    } for p in products]
    return jsonify(all_products), 200


if __name__ == "__main__":
    app.run(port=8080, debug=True)
