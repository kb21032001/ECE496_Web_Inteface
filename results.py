from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"


# Create the database instance
db = SQLAlchemy(app)

# Define the model for the table
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_label = db.Column(db.Float)
    house_sparrow = db.Column(db.Float)
    house_finch = db.Column(db.Float)

# Move db.create_all() inside the application context
with app.app_context():
    db.create_all()

@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        # Get JSON data from the request
        data_json = request.get_json()

        # Extract data from JSON
        no_label = data_json['No Label']
        house_sparrow = data_json['House Sparrow']
        house_finch = data_json['House Finch']

        no_label = float(no_label) * 100
        house_sparrow = float(house_sparrow) * 100
        house_finch = float(house_finch) * 100

        # Create a new Data instance
        new_data = Data(no_label=no_label, house_sparrow=house_sparrow, house_finch=house_finch)

        # Add the instance to the database
        db.session.add(new_data)

        # Commit the changes
        db.session.commit()

        test_query = get_all_results_from_database()
        print(f"Here is the database: {test_query}")

        return jsonify({'message': 'Data inserted successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_all_results_from_database():
    results_data = Data.query.all()

    # Make a dict for event details
    dict_of_results_data = {}
    for row in results_data:
        results_data = {}

        for column in row.__table__.columns:
            results_data[column.name] = str(getattr(row, column.name))

        dict_of_results_data[row.id] = results_data

    return dict_of_results_data

@app.route('/')
def display_data():
    # Query all data from the Data table
    data = Data.query.all()
    
    # Render the HTML template and pass the data to it
    return render_template('display_data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
