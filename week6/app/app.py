from flask import Flask, render_template, request, redirect, abort
from flask.ext.script import Manager
import database_utils

app = Flask(__name__, static_url_path="/static")
app.debug = True

@app.route('/')
def index():
    return render_template('index.jinja2.html', message="Now Let's get tracking!", exist_error=False);

@app.route('/tracked_meals', methods=['POST'])
def home():
        if request.method == 'POST':
            form = request.form
            # Get the meal info from the form
            print form
            meal_info = dict()
            meal_info['UserName'] = form['UserName']
            meal_info['Meal'] = form['Meal']
            meal_info['Price'] = form['Price']
            meal_info['FoodType'] = form['FoodType']

            # Check to make sure that the 
            if meal_info['FoodType'] not in ['Food', 'Alcohol']:
                return render_template('index.jinja2.html', message="You have to enter 'Alcohol' or 'Food'",exist_error=True)

            try: 
                float(meal_info['Price'])
            except ValueError:
                return render_template('index.jinja2.html', message="The price that you entered is not valid please try again",exist_error=True)
            
            # insert meal into database
            database_utils.InsertMeal(meal_info)
            
            # Get the UserName and meals
            UserName = meal_info["UserName"]
            food_meals, alcohol_meals = database_utils.GetMeals(UserName)
            
            # Debug Purposes
            print "The UserName is", UserName
            print list(food_meals), list(alcohol_meals)

            # Now let's get the cost and all of the meals
            food_,alcohol_, entries = database_utils.GetValuesforDisplay(UserName)

            # Now let's sort the entires based on when they were input into the system,
            # we want to sort them so that the largest entries appear in the next section
            sorted_entries = sorted(entries, key=lambda k : k['Time'], reverse=True)
            print sorted_entries

            # Now add template rendering based on the data
        return render_template('trackedmeals.jinja2.html', food_vals=food_, alcohol_vals=alcohol_, entries=sorted_entries);

# This runs the app manager      
manager = Manager(app);

if __name__ == "__main__":
    manager.run()