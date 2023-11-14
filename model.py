import logging
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    login_type = db.Column(db.Integer, comment="4096 = admin | 128 = guest")
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))

    location = db.relationship('Location', backref='users', foreign_keys=[location_id])

    @classmethod
    def sign_up(cls, username, password, firstname, surname, email, phone, location_id):
        if (len(username) > 8 and len(password) > 8):
            check_user = cls.query.filter_by(username=username).first()
            if check_user:
                return None
            user_entry = User(
                username=username.strip(),
                password=password.strip(),
                firstname=firstname.strip(),
                surname=surname.strip(),
                email=email.strip(),
                phone=phone.strip(),
                location_id=int(location_id)
            )
            
            db.session.add(user_entry)
            db.session.commit()
            return user_entry
            

    @classmethod 
    def log_in(cls, username, password):
        try:
            current_user = cls.query.filter_by(username=username).first()
            print(current_user.username)
            print(current_user.password)
            print(password)
            return str(password)==str(current_user.password)
        except:
            return False
            

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
    # Reset sales statistics before recalculating
    SalesStatistics.query.delete()

    # Query TradeData
    trade_data = TradeData.query.all()

    # Process each trade entry
    for trade in trade_data:
        try:
            # Check if the corresponding Products and Location entries exist
            product = Products.query.get(trade.product_id)
            location = Location.query.get(trade.location_id)

            if not product or not location:
                # Handle cases where Products or Location entry is not found
                continue

            # Check if the trade entry has already been processed
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
        except Exception as e:
            logging.error(f"Error processing trade entry: {trade.trade_id}. Error: {str(e)}")
    
    # Commit changes to the database
    db.session.commit()
