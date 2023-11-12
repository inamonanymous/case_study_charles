from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(255))

class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_description = db.Column(db.String(255))
    product_unit = db.Column(db.String(255))

class TradeData(db.Model):
    __tablename__ = 'trade_data'
    trade_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    trade_year = db.Column(db.String(4))
    trade_quantity = db.Column(db.Integer)

class SalesStatistics(db.Model):
    __tablename__ = 'sales_statistics'
    stat_id = db.Column(db.Integer, primary_key=True)
    stat_year = db.Column(db.String(4))
    stat_series_name = db.Column(db.String(255))
    stat_value = db.Column(db.Integer)
