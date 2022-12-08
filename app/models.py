from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    name = db.Column(db.String(50))
    job = db.Column(db.Boolean())


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.String(500))
    image = db.Column(db.LargeBinary(length=5120))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    number = db.Column(db.Integer)
    money = db.Column(db.Float)
    destination = db.Column(db.String(50))


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    money = db.Column(db.Float)
    destination = db.Column(db.String(50))


class Collection(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
