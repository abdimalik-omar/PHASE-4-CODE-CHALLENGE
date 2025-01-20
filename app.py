from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import User, Product, db

app = Flask(__name__)

# Migration initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/users", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_username or check_email:
        return jsonify({"error": "Username or email already exists"}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": "User registered successfully"}), 201


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    result = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return jsonify(result), 200


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()

    return jsonify({"success": "User updated successfully"}), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "User deleted successfully"}), 200


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']

    new_product = Product(name=name, description=description, price=price)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"success": "Product added successfully"}), 201


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in products]
    return jsonify(result), 200


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get_or_404(product_id)

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)

    db.session.commit()
    return jsonify({"success": "Product updated successfully"}), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"success": "Product deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
