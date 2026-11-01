#!/usr/bin/env python3

from app import app
from models import *
from datetime import date

with app.app_context():
# reset data and add new example data, committing to db 
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    exercises = [
        Exercise(name='Push-ups', category='Strength', equipment_needed=False),
        Exercise(name='Squats', category='Strength', equipment_needed=False),
        Exercise(name='Plank', category='Strength', equipment_needed=False),
        Exercise(name='Lifting Weights', category='Strength', equipment_needed=True),
    ]
    db.session.add_all(exercises)
    db.session.commit()

    workouts = [
        Workout(date=date(2023, 9, 1), duration_minutes=30, notes='Morning workout'),
        Workout(date=date(2023, 9, 2), duration_minutes=45, notes='Evening workout'),
        Workout(date=date(2024, 9, 3), duration_minutes=60)
    ]
    db.session.add_all(workouts)
    db.session.commit()

    workout_exercises = [
        WorkoutExercise(workout=workouts[0], exercise=exercises[0], sets=3, reps=15),
        WorkoutExercise(workout=workouts[0], exercise=exercises[1], sets=3, reps=20),
        WorkoutExercise(workout=workouts[1], exercise=exercises[2], sets=3, duration_seconds=60),
        WorkoutExercise(workout=workouts[1], exercise=exercises[3], sets=4, reps=12),
        WorkoutExercise(workout=workouts[2], exercise=exercises[0], sets=5, reps=20),
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()