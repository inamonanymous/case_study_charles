from flask import Flask, redirect, render_template, url_for, session, request, jsonify
from model import db, TradeData, Products, Location, SalesStatistics
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/farmerdata_charles'
db.init_app(app)
migrate = Migrate(app, db)

#radar data
@app.route('/api/radar_chart_data')
def radar_chart_data():
    # Assume you are tracking data for years 2018 to 2023
    years = ['2018', '2019', '2020', '2021', '2022', '2023']
    series_data = {}

    query_results = SalesStatistics.query.all()
    for result in query_results:
        series_name = result.stat_series_name
        if series_name not in series_data:
            series_data[series_name] = [0] * len(years)
        year_index = years.index(result.stat_year)
        series_data[series_name][year_index] = result.stat_value

    return jsonify(series_data)

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

        
    """bar_chart_data = {
        "Rice": [10, 20, 15, 25, 30, 18, 12, 24, 16],
        "Sugar": [5, 15, 10, 20, 25, 12, 8, 22, 14],
        "Oil": [8, 18, 13, 23, 28, 15, 10, 20, 12],
        "Vegetable": [12, 22, 17, 37, 32, 20, 14, 26, 18]
    }"""

    # Include the x-axis categories in the API response
    xaxis_categories = [i.location_name for i in Location.query.all()]
    response_data = {
        "xaxis": {
            "categories": xaxis_categories  # Use the predefined x-axis categories
        },
        "data": bar_chart_data
    }
    return jsonify(response_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    """with app.app_context():
        db.create_all()"""
    app.run(debug=True)