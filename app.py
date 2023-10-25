from flask import Flask, redirect, render_template, url_for, session, request, jsonify

app = Flask(__name__)


bar_chart_data = {
    "Rice": [10, 20, 15, 25, 30, 18, 12, 24, 16],
    "Sugar": [5, 15, 10, 20, 25, 12, 8, 22, 14],
    "Oil": [8, 18, 13, 23, 28, 15, 10, 20, 12],
    "Vegetable": [12, 22, 17, 37, 32, 20, 14, 26, 18]
}

# Include the x-axis categories in the API response
xaxis_categories = ['Mamatid', 'Baclaran', 'Banay-banay', 'Gulod', 'SanIsidro', 'Pulo', 'Marinig', 'Butong', 'Niugan']

@app.route('/api/bar_chart_data')
def get_bar_chart_data():
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
    app.run(debug=True)