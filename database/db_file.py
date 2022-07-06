from create import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/market.db'

class Products(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    photo = db.Column(db.Text, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Products %r>' % self.prod_id

class Categories(db.Model):
    categor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Categories %r>' % self.categor_id



def add_product(product):
    name = product['name']
    price = product['price']
    description = product['description']
    photo = product['photo']
    category = product['category']
    productSQL = Products(name=name, price=price, description=description, photo=photo, category=category)
    db.session.add(productSQL)
    db.session.commit()


def add_category(name):
    productSQL = Categories(name=name)
    db.session.add(productSQL)
    db.session.commit()