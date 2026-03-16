import json
from flask import Flask, render_template

# Create an instance of the Flask class
app = Flask(__name__)


with open('project/data.json', 'r') as file:
    tours = json.load(file)


@app.route('/')
def home():
    return render_template("base.html")


@app.route('/tour/<tour_operator_name>')
def get_tour_operator(tour_operator_name):
    tour = None
    for t in tours:
        if t['tour_operator'] == tour_operator_name:
            tour = t
            break 
    
    return render_template("tour.html", tour=tour)


@app.route('/turkey_luxury')
def get_turkey_best_tour():
    tour = None
    max = 0
    for t in tours:
        if t['country'] == "Turkey" and t['price'] > max:
            max = t['price']
            tour = t
    
    return render_template("tour.html", tour=tour)


@app.route('/tour_days/<days_number>')
def get_tour_with_n_days(days_number):
    n = int(days_number)
    fitting_tours = []
    for t in tours:
        if t['days'] >= n:
            fitting_tours.append(t)

    return render_template("tour_days.html", tours=fitting_tours)


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html"), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True) # debug=True enables the debugger and auto-reloader
