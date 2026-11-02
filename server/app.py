from flask import Flask, make_response, request
from flask_migrate import Migrate
from schemas import WorkoutSchema
from marshmallow import ValidationError

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=['workout_exercises'])

# Define Routes here
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workout = Workout.query.all()
    data = workouts_schema.dump(workout)
    return make_response(data, 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if workout is None:
        return make_response({"error": "Workout not found"}, 404)
    data = workout_schema.dump(workout)
    return make_response(data, 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    return make_response({}, 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return make_response({}, 204)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return make_response({}, 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    return make_response({}, 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    return make_response({}, 201)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return make_response({}, 204)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    return make_response({}, 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)