from flask import Flask, redirect, render_template, url_for, session, request, jsonify
from model import db, TradeData, Products, Location, SalesStatistics, update_sales_statistics
from sqlalchemy import func, distinct
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/farmerdata_charles'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/add-trade', methods=['POST', 'GET'])
def add_trade():
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
    return jsonify({"message": "error"}), 401

@app.route('/get-products-and-locations')
def get_product_and_location():
    locations = Location.query.all()
    products = Products.query.all()
    locations_data = [
        {
            'location_id': loc.location_id, 
            'location_name': loc.location_name
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

    return jsonify(data)

@app.route('/api/reports_data')
def reports():
    locations = Location.query.all()
    products = Products.query.all()
    trade_data = TradeData.query.\
    with_entities(TradeData.trade_id,
                  TradeData.trade_year,
                  TradeData.trade_quantity,
                  Products.product_name,
                  Products.product_description,
                  Location.location_name, 
                  ).\
    join(Products, TradeData.product_id == Products.product_id).\
    join(Location, TradeData.location_id==Location.location_id).all()
    print(trade_data)
    sales_statistics = SalesStatistics.query.all()

    locations_list = [{'location_id': i.location_id, 
                       'location_name': i.location_name} for i in locations]
    
    products_list = [{'product_id': i.product_id, 
                      'product_name': i.product_name, 
                      'product_description': i.product_description, 
                      'product_unit': i.product_unit} for i in products]
    
    trades_list = [{'trade_id': i.trade_id, 
                    'location_name': i.location_name,
                    'product_name': i.product_name,
                    'trade_year': i.trade_year, 
                    'trade_quantity': i.trade_quantity} for i in trade_data]
    
    stat_list = [{'stat_id': i.stat_id, 
                       'stat_year': i.stat_year,
                       'stat_series_name': i.stat_series_name,
                       'stat_value': i.stat_value} for i in sales_statistics]
    

    reports = {
        'locations': locations_list,
        'products': products_list,
        'trade_data': trades_list,
        'sales_statistics': stat_list
    }

    return jsonify(reports)

#radar data
@app.route('/api/radar_chart_data')
def radar_chart_data():
    # Here we assume you are comparing sales volume across different products
    sales_volume_by_product = db.session.query(
        Products.product_name,
        db.func.sum(SalesStatistics.sales_volume).label('total_sales_volume')
    ).join(SalesStatistics, SalesStatistics.product_id == Products.product_id)\
     .group_by(Products.product_name)\
     .all()

    # Format for ApexCharts radar chart
    response = {
        'series': [{
            'name': 'Sales Volume',
            'data': [volume for _, volume in sales_volume_by_product],
        }],
        'categories': [product for product, _ in sales_volume_by_product]
    }

    return jsonify(response)

#trade data 
@app.route('/api/area_chart_data')
def area_chart_data():
    years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023']
    area_chart_data = {year: {product.product_name: 0 for product in Products.query.all()} for year in years}
    print(area_chart_data)
    query_result = TradeData.query.\
        with_entities(Products.product_name, TradeData.trade_year, db.func.sum(TradeData.trade_quantity)).\
        join(Products, TradeData.product_id==Products.product_id).\
        group_by(Products.product_name, TradeData.trade_year).all()

    for product_name, trade_year, quantity in query_result:
        if trade_year in area_chart_data:
            area_chart_data[trade_year][product_name] = quantity

    product_names = [product.product_name for product in Products.query.all()]
    structured_data = {product_name: [area_chart_data[year][product_name] for year in years] for product_name in product_names}
    print(structured_data)
    return jsonify({"data": structured_data, "years": years})
#farmers trade
@app.route('/api/bar_chart_data')
def get_bar_chart_data():
    bar_chart_data = {}
    query_result = TradeData.query.\
        with_entities(Products.product_name, Location.location_name, db.func.sum(TradeData.trade_quantity)).\
        join(Products, TradeData.product_id== Products.product_id).\
        join(Location, TradeData.location_id==Location.location_id)\
        .group_by(Products.product_name, Location.location_name).all()
    
    print(query_result)
    for i, j, x in query_result:
        if i not in bar_chart_data:
            bar_chart_data[i] = []
        bar_chart_data[i].append(x)
       
    # Include the x-axis categories in the API response
    xaxis_categories = [i.location_name for i in Location.query.all()]
    response_data = {
        "xaxis": {
            "categories": xaxis_categories  # Use the predefined x-axis categories
        },
        "data": bar_chart_data
    }
    return jsonify(response_data)

@app.route('/dashboard-items')
def dashboard_items():
    products_count = Products.query.with_entities(func.count(distinct(Products.product_id))).scalar()
    sales_count = SalesStatistics.query.with_entities(func.count(distinct(SalesStatistics.stat_id))).scalar()
    trades_count = TradeData.query.with_entities(func.count(distinct(TradeData.trade_id))).scalar()
    location_count = Location.query.with_entities(func.count(distinct(Location.location_id))).scalar()
    
    data = {
        'products_count': products_count,
        'sales_count': sales_count,
        'trades_count': trades_count,
        'location_count': location_count
    }
    
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    """with app.app_context():
        db.create_all()"""
    app.run(debug=True)