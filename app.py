from flask import Flask, redirect, render_template, url_for, session, request, jsonify
from model import db, TradeData, Products, Location, SalesStatistics, update_sales_statistics, User
from sqlalchemy import func, distinct, or_
from sqlalchemy.orm import aliased
from collections import defaultdict
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/farmerdata_charles'
app.secret_key = 'mysecretkey'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/manage-trades/<int:id>', methods=['DELETE', 'GET'])
def manage_trades(id):
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    if not current_user.login_type == 4096 or current_user.login_type is None:
        return jsonify({"message": "Guest users not allowed"}), 401
    target_trade = TradeData.query.filter_by(trade_id=id).first()
    if not target_trade:
        return jsonify({"message": "No Record Found"}), 420
    db.session.delete(target_trade)
    db.session.commit()
    return jsonify({"message": "Trade Record Deleted"}), 201

@app.route('/manage-locations/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def manage_locations(id):
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    if not current_user.login_type == 4096 or current_user.login_type is None:
        return jsonify({"message": "Guest users not allowed"}), 401
    target_location = Location.query.filter_by(location_id=id).first()
    if target_location is None:
        return jsonify({"message": "no location found"}), 401
    if request.method=="PUT":
        data = request.get_json()
        target_location.location_name = data['location_name']
        db.session.commit()
        return jsonify({"message": "Product Updated"}), 201
    if request.method=="DELETE":
        target_users = User.query.filter_by(location_id=target_location.location_id).all()
        target_sales = SalesStatistics.query.filter_by(location_id=target_location.location_id).all()
        for i in target_users:
            i.location_id=None
        for i in target_sales:
            db.session.delete(i)
        db.session.commit()
        db.session.delete(target_location)
        db.session.commit()
        return jsonify({"message": "Location Deleted"}), 201
    if request.method=="GET":
        data = {
            'location_id': target_location.location_id,
            'location_name': target_location.location_name
        }
        return jsonify(data), 201
    return jsonify({"message": "bad request"}), 499

@app.route('/manage-products/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def manage_products(id):
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    if not current_user.login_type == 4096 or current_user.login_type is None:
        return jsonify({"message": "Guest users not allowed"}), 401
    target_product = Products.query.filter_by(product_id=id).first()
    if target_product is None:
        return jsonify({"message": "no product found"}), 401
    if request.method=="PUT":
        data = request.get_json()
        target_product.product_name = data['product_name']
        target_product.product_description = data['product_description']
        target_product.product_unit = data['product_unit']
        db.session.commit()
        return jsonify({"message": "Product Updated"}), 201
    if request.method=="DELETE":
        target_trades = TradeData.query.filter_by(product_id=target_product.product_id).all()
        target_sales = SalesStatistics.query.filter_by(product_id=target_product.product_id).all()
        for i in target_trades:
            db.session.delete(i)
        for i in target_sales:
            db.session.delete(i)
        db.session.commit()
        db.session.delete(target_product)
        db.session.commit()
        return jsonify({"message": "Product Deleted"}), 201
    if request.method=="GET":
        data = {
            'product_id': target_product.product_id,
            'product_name': target_product.product_name,
            'product_description': target_product.product_description,
            'product_unit': target_product.product_unit
        }
        return jsonify(data), 201
    return jsonify({"message": "bad request"}), 499

@app.route('/verify-user-data/<int:id>', methods=['PUT', 'GET'])
def verify_user_data(id):
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    if not current_user.login_type == 4096 or current_user.login_type is None:
        return jsonify({"message": "Guest users not allowed"}), 401
    target_user = User.query.filter_by(user_id=id).first()
    if not target_user or target_user.login_type==4096 or target_user.login_type==128:
        return jsonify({"message": "master user cannot be verified or no user found or user already verified"}), 417
    target_user.login_type=128
    db.session.commit()
    return jsonify({"message": "user verified"}), 201

@app.route('/delete-user-data/<int:id>', methods=['DELETE', 'GET'])
def delete_user_data(id):
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    if not current_user.login_type == 4096 or current_user.login_type is None:
        return jsonify({"message": "Guest users not allowed"}), 401
    target_user = User.query.filter_by(user_id=id).first()
    if not target_user or target_user.login_type==4096:
        return jsonify({"message": "master user cannot be deleted or no user found"}), 417
    db.session.delete(target_user)
    db.session.commit()
    return jsonify({"message": "user deleted"}), 201

@app.route('/get-users-data')
def get_users_data():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    if not current_user.login_type == 4096 or current_user.login_type is None:
        return jsonify({"message": "Guest users not allowed"}), 401
    query = User.query.with_entities(
        User.user_id,
        User.username,
        User.firstname,
        User.surname,
        User.email,
        User.phone,
        User.login_type,
        Location.location_name,
        ).join(Location, User.location_id==Location.location_id).all()
    data = [{
        'user_id': i.user_id,
        'username': i.username,
        'firstname': i.firstname,
        'surname': i.surname,
        'email': i.email,
        'phone': i.phone,
        'login_type': i.login_type,
        'location_id': i.location_name
    } for i in query]
    
    return jsonify(data), 201

@app.route('/get-product-location-trade')
def get_product_location_trade():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    products = Products.query.all()
    locations = Location.query.all()
    location_alias = aliased(Location)
    product_alias = aliased(Products)
    trades = db.session.query(
        TradeData.trade_id,
        TradeData.trade_year,
        TradeData.trade_quantity,
        location_alias.location_name.label('location_name'),
        product_alias.product_name.label('product_name')
    ).join(
        location_alias,
        TradeData.location_id == location_alias.location_id
    ).join(
        product_alias,
        TradeData.product_id == product_alias.product_id
    ).all()
    processed_products = [{
        "product_id": i.product_id,
        "product_name": i.product_name,
        "product_description": i.product_description,
        "product_unit": i.product_unit
    } for i in products]
    processed_locations = [{
        "location_id": i.location_id,
        "location_name": i.location_name
        }for i in locations]
    processed_trades = [{
    "trade_id": row.trade_id,
    "trade_year": row.trade_year,
    "trade_quantity": row.trade_quantity,
    "location_name": row.location_name,
    "product_name": row.product_name,
    } for row in trades]
    data = {
        'products': processed_products,
        'locations': processed_locations,
        'trades': processed_trades
    }
    return jsonify(data)


@app.route('/update-user-info/<int:id>', methods=['PUT', 'GET'])
def update_user_info(id):
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    if request.method=="PUT":
        data = request.get_json()
        target_user = User.query.filter_by(user_id=id).first()
        target_user.firstname = data['firstname'].strip()
        target_user.surname = data['surname'].strip()
        target_user.phone = data['phone'].strip()
        target_user.email = data['email'].strip()
        db.session.commit()
        return jsonify({"message": "update success"}), 201
    return jsonify({"message": "bad request"}), 405

@app.route('/add-product', methods=['POST', 'GET'])
def add_product():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    if request.method=="POST":
        data = request.get_json()
        product_entry = Products(
            product_name=data['product_name'],
            product_description=data['product_description'],
            product_unit=data['product_unit']
        )
        db.session.add(product_entry), 201
        db.session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "cant add product ? error"}), 401

@app.route('/add-location', methods=['POST', 'GET'])
def add_location():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    if request.method=="POST":
        data = request.get_json()
        location_entry = Location(location_name=data['location_name'])
        db.session.add(location_entry)
        db.session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "cant add location ? error"}), 401
    
@app.route('/add-trade', methods=['POST', 'GET'])
def add_trade():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    if request.method=="POST":
        data = request.get_json()
        trade_entry = TradeData(
            location_id = data['location_id'],
            product_id = data['trade_product'],
            trade_year = data['trade_year'],
            trade_quantity = data['trade_quantity']
        )
        db.session.add(trade_entry)
        db.session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "cant add trade ? error"}), 401

@app.route('/get-products-and-locations')
def get_product_and_location():
    locations = Location.query.all()
    products = Products.query.all()
    locations_data = [
        {
            'location_id': loc.location_id, 
            'location_name': loc.location_name,
         }
        for loc in locations
    ]
    products_data = [
        {
            'product_id': prod.product_id,
            'product_name': prod.product_name,
            'product_description': prod.product_description,
            'product_unit': prod.product_unit
        } for prod in products
    ]
    data = {
        'locations_data': locations_data,
        'products_data': products_data
    }
    return jsonify(data), 201

@app.route('/api/radar_chart_data')
def radar_chart_data():
    update_sales_statistics()
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 480
    # Assuming Products is your SQLAlchemy model for products
    products = db.session.query(Products.product_name).all()
    categories = [product[0] for product in products]
    sales_volume_by_product = db.session.query(
        Products.product_name,
        db.func.sum(SalesStatistics.sales_volume).label('total_sales_volume')
    ).outerjoin(SalesStatistics, SalesStatistics.product_id == Products.product_id)\
     .group_by(Products.product_name)\
     .all()
    # Create a dictionary to map product names to sales volumes
    sales_volume_map = {product: volume for product, volume in sales_volume_by_product}
    # Ensure the sales volume data aligns with the categories
    sales_data = [sales_volume_map.get(category, 0) for category in categories]
    response = {
        'series': [{
            'name': 'Sales Volume',
            'data': sales_data,
        }],
        'categories': categories
    }
    return jsonify(response), 201

@app.route('/api/area_chart_data')
def area_chart_data():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023']
    area_chart_data = {year: {product.product_name: 0 for product in Products.query.all()} for year in years}
    query_result = TradeData.query.\
        with_entities(Products.product_name, TradeData.trade_year, db.func.sum(TradeData.trade_quantity)).\
        join(Products, TradeData.product_id==Products.product_id).\
        group_by(Products.product_name, TradeData.trade_year).all()
    for product_name, trade_year, quantity in query_result:
        if trade_year in area_chart_data:
            area_chart_data[trade_year][product_name] = quantity
    product_names = [product.product_name for product in Products.query.all()]
    structured_data = {product_name: [area_chart_data[year][product_name] for year in years] for product_name in product_names}
    return jsonify({"data": structured_data, "years": years}), 201

@app.route('/api/bar_chart_data')
def get_bar_chart_data():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    bar_chart_data = defaultdict(list)
    # Initialize the data dictionary with zeros for each product at each location
    for product_name in [p.product_name for p in Products.query.all()]:
        for location_name in [l.location_name for l in Location.query.all()]:
            bar_chart_data[product_name].append(0)
    # Update the data dictionary with the actual values from the database query
    query_result = TradeData.query.\
        with_entities(Products.product_name, Location.location_name, db.func.sum(TradeData.trade_quantity)).\
        join(Products, TradeData.product_id == Products.product_id).\
        join(Location, TradeData.location_id == Location.location_id).\
        group_by(Products.product_name, Location.location_name).all()
    xaxis_categories = [l.location_name for l in Location.query.all()]
    for product_name, location_name, quantity in query_result:
        bar_chart_data[product_name][xaxis_categories.index(location_name)] = int(quantity)
    # Include the x-axis categories in the API response
    response_data = {
        "xaxis": {
            "categories": xaxis_categories
        },
        "data": bar_chart_data
    }
    return jsonify(response_data), 201

@app.route('/dashboard-items')
def dashboard_items():
    if not 'username' in session:
        return jsonify({"message": "Not logged in"}), 480
    products_count = Products.query.with_entities(func.count(distinct(Products.product_id))).scalar()
    sales_count = SalesStatistics.query.with_entities(func.count(distinct(SalesStatistics.stat_id))).scalar()
    trades_count = TradeData.query.with_entities(func.count(distinct(TradeData.trade_id))).scalar()
    location_count = Location.query.with_entities(func.count(distinct(Location.location_id))).scalar()
    admin_count = User.query.filter(User.login_type == 4096).count()
    guest_count = User.query.filter(User.login_type == 128).count()
    pending_account_count = User.query.filter(or_(User.login_type.is_(None), User.login_type == 0)).count()
    data = {
        'products_count': products_count,
        'sales_count': sales_count,
        'trades_count': trades_count,
        'location_count': location_count,
        'guest_count': guest_count,
        'pending_account_count': pending_account_count,
        'admin_count': admin_count
    }
    return jsonify(data), 201

@app.route('/home')
def home():
    if not 'username' in session:
        return redirect(url_for('index'))
    current_user = User.query.filter_by(username=session.get('username', "")).first()
    print(current_user.username)
    return render_template('home.html', current_user=current_user)

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    data = request.get_json()
    if User.log_in(data['username'], data['password']):
        current_user = User.query.filter_by(username=data['username']).first()
        if not current_user.login_type or current_user.login_type == 0:
            return jsonify({"message": "login failed | acccoutn not verified"}), 420        
        session['username'] = data['username']
        return jsonify({"message": "login success"}), 201
    return jsonify({"message": "login failed"}), 401
    
@app.route('/sign-up-entry', methods=['POST', 'GET'])
def sign_up_entry():
    data = request.get_json()
    check_user = User.query.filter_by(username=str(data['username'])).first()
    if check_user:
        return None
    user_entry = User(
        username=data['username'].strip(),
        password=data['password'].strip(),
        firstname=data['firstname'].strip(),
        surname=data['surname'].strip(),
        email=data['email'].strip(),
        phone=data['phone'].strip(),
        location_id=data['location_id']
    )
    if not user_entry:
        return jsonify({"message": "can't register entry"}), 401
    db.session.add(user_entry)
    db.session.commit()
    return jsonify({"message": "register success"}), 201

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/')
def index():
    session.clear()
    return render_template('auth.html')

if __name__ == "__main__":
    app.run(debug=True)