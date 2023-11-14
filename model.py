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
    
    # Define foreign keys for location_id and product_id
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    
    trade_year = db.Column(db.String(4))
    trade_quantity = db.Column(db.Integer)

    # Define relationships to Location and Products
    location = db.relationship('Location', backref='trade_data', foreign_keys=[location_id])
    product = db.relationship('Products', backref='trade_data', foreign_keys=[product_id])
   
class SalesStatistics(db.Model):
    __tablename__ = 'sales_statistics'
    stat_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    stat_year = db.Column(db.String(4))
    sales_volume = db.Column(db.Integer)

    product = db.relationship('Products', foreign_keys=[product_id])
    location = db.relationship('Location', foreign_keys=[location_id])



def update_sales_statistics():
    # Query TradeData
    trade_data = TradeData.query.all()

    # Process each trade entry
    for trade in trade_data:
        # Logic to aggregate or calculate statistics
        # Example: summing trade quantities for a product
        existing_stat = SalesStatistics.query.filter_by(
            product_id=trade.product_id, 
            location_id=trade.location_id,
            stat_year=trade.trade_year
        ).first()

        if existing_stat:
            # Update existing statistic
            existing_stat.sales_volume += trade.trade_quantity
        else:
            # Create a new statistic entry
            new_stat = SalesStatistics(
                product_id=trade.product_id,
                location_id=trade.location_id,
                stat_year=trade.trade_year,
                sales_volume=trade.trade_quantity
            )
            db.session.add(new_stat)
    
    # Commit changes to the database
    db.session.commit()
