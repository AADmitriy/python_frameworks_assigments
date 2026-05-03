import json
from flask import Flask, render_template, flash, request, redirect, url_for
from forms import TourOperatorForm, DaysNumberForm, TourForm, SearchForm

# Create an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.secret_key = 'mysecretkey'


with open('data.json', 'r') as file:
    tours = json.load(file)


@app.route('/')
def home():
    return render_template("base.html")

@app.route('/index')
def index():
    return render_template("index.html", tours=tours)

@app.route('/search')
def search():
    form = SearchForm(request.args)
    form.name.choices = [('', 'Select...')] + [
        (s["tour_operator"], s["tour_operator"]) for s in tours
    ]

    search_option = request.args.get("search_option", None)
    tour_operator_name = request.args.get("name", None)
    days = request.args.get("days", None)
    fitting_tours = []

    form_validated = False
    if len(request.args):
        form_validated = form.validate()
        if not form_validated:
            flash("Enter valid search input", "danger")
            return render_template("search.html", form=form, tours=fitting_tours)
        else:
            form.search_option.data = search_option


    if search_option == "tour_operator" and tour_operator_name:
        form.name.data = tour_operator_name
        for t in tours:
            if t['tour_operator'] == tour_operator_name:
                fitting_tours.append(t)
                break

    if search_option == "days" and days:
        form.days.data = days
        n = int(days)
        for t in tours:
            if t['days'] >= n:
                fitting_tours.append(t)

    if search_option == "luxury":
        tour = None
        max = 0
        for t in tours:
            if t['country'] == "Turkey" and t['price'] > max:
                max = t['price']
                tour = t
        fitting_tours.append(tour)

    if form_validated:
        if len(fitting_tours) == 0:
            flash("No tours found for this criteria!", "warning")
        else:
            flash(f"{len(fitting_tours)} tours found!", "success")


    return render_template("search.html", form=form, tours=fitting_tours)


@app.route('/create_tour', methods=['GET', 'POST'])
def create_tour():
    form = TourForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            tours.append({
                "country": form.country.data,
                "tour_operator": form.tour_operator.data,
                "price": form.price.data,
                "days": form.days.data
            })
            flash("The tour was created!", "success")
            return redirect(url_for("index"))
        else:
            flash("Enter valid tour data", "danger")

    return render_template("create_tour.html", form=form)


@app.route('/tour')
def get_tour_operator():
    form = TourOperatorForm(request.args)
    form.name.choices = [('', 'Select...')] + [
        (s["tour_operator"], s["tour_operator"]) for s in tours
    ]
    tour_operator_name = request.args.get("name", None)

    form_validated = False
    if len(request.args):
        form_validated = form.validate()
        if not form_validated:
            flash("Enter valid search input", "danger")

    tour = None
    search_input = ''
    if form_validated and tour_operator_name:
        form.name.data = tour_operator_name
        search_input = 'for "' + tour_operator_name + '"'
        for t in tours:
            if t['tour_operator'] == tour_operator_name:
                tour = t
                break 

        if not tour:
            flash("The tour was not found!", "warning")
        else:
            flash("The tour was found!", "success")
    
    return render_template("tour.html", tour=tour, form=form, search_input=search_input)


@app.route('/tour_days/')
def get_tour_with_n_days():
    form = DaysNumberForm(request.args)
    fitting_tours = []
    days = request.args.get("days", None)

    form_validated = False
    if len(request.args):
        form_validated = form.validate()
        if not form_validated:
            flash("Enter valid search input", "danger")
        
        
    if form_validated and days:
        form.days.data = days
        n = int(days)
        for t in tours:
            if t['days'] >= n:
                fitting_tours.append(t)

        if len(fitting_tours) == 0:
            flash("No tours found for this criteria!", "warning")
        else:
            flash(f"{len(fitting_tours)} tours found!", "success")

    return render_template("tour_days.html", tours=fitting_tours, form=form)


@app.route('/turkey_luxury')
def get_turkey_best_tour():
    tour = None
    max = 0
    for t in tours:
        if t['country'] == "Turkey" and t['price'] > max:
            max = t['price']
            tour = t
    
    return render_template("tour.html", tour=tour)


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html"), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
