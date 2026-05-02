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
    return render_template("tour.html", tours=tours, operator=tour_operator_name)


@app.route('/turkey_luxury')
def get_turkey_best_tour():
    return render_template("tour.html", tours=tours, country="Turkey", find_max=True)


@app.route('/tour_days/<days_number>')
def get_tour_with_n_days(days_number):
    return render_template("tour_days.html", tours=tours, min_days=int(days_number))


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html"), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True) # debug=True enables the debugger and auto-reloader
