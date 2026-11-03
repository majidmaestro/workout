from flask import Flask, make_response, request
from flask_migrate import Migrate
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=['workout_exercises'])
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=['workouts'])

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
    try:
        data = workout_schema.load(request.get_json())
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)
    
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return make_response(workout_schema.dump(workout), 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return make_response({}, 204)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercise = Exercise.query.all()
    data = exercises_schema.dump(exercise)
    return make_response(data, 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise is None:
        return make_response({"error": "Exercise not found"}, 404)
    data = exercise_schema.dump(exercise)
    return make_response(data, 200)

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