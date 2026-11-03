# Workout Tracker API

A backend REST API for a workout tracking application used by personal trainers. It is built with Flask, SQLAlchemy and Marshmallow.

## Description

Trainers can create and view workouts, create and view reusable exercises, and add exercises to workouts with the number of sets, reps or duration for each one.

- A **Workout** is one training session (a date, how long it lasted, and optional notes).
- An **Exercise** is a reusable movement such as push-ups or squats. It is stored once and can appear in many workouts.
- A **WorkoutExercise** is the join table that links a workout to an exercise and stores the sets, reps and duration for that pairing.

The API validates data at three levels: the database (table constraints), the models (model validations) and the request layer (Marshmallow schema validations).

## Tech stack

- Python 3.8+ (developed on 3.12)
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite
- Pipenv

## Project structure

```
workout/
├── Pipfile
├── Pipfile.lock
├── README.md
└── server/
    ├── app.py          # Flask app and routes
    ├── models.py       # SQLAlchemy models, relationships, constraints, validations
    ├── schemas.py      # Marshmallow schemas for serialization and validation
    ├── seed.py         # Resets the database and adds example data
    └── migrations/     # Alembic/Flask-Migrate migration files
```

## Installation

1. Clone the repository and move into it:

   ```bash
   git clone https://github.com/majidmaestro/workout.git
   cd workout
   ```

2. Install the dependencies and open the virtual environment:

   ```bash
   pipenv install
   pipenv shell
   ```

3. Move into the `server` folder:

   ```bash
   cd server
   ```

4. Create the database tables by applying the migrations:

   ```bash
   flask db upgrade head
   ```

5. Seed the database with example data:

   ```bash
   python seed.py
   ```

   The seed file clears all three tables before adding data, so it can be run as many times as you like without creating duplicates.

## Running the app

From the `server` folder, inside the pipenv shell:

```bash
python app.py
```

The API runs at `http://127.0.0.1:5555`.

You can also use `flask run -p 5555`.

## Data model

### Exercise

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | required, unique |
| category | string | required |
| equipment_needed | boolean | required |

### Workout

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| date | date | required |
| duration_minutes | integer | required, must be greater than 0 |
| notes | text | optional |

### WorkoutExercise (join table)

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| workout_id | integer | foreign key to workouts, required |
| exercise_id | integer | foreign key to exercises, required |
| sets | integer | optional, must be greater than 0 if given |
| reps | integer | optional, must be greater than 0 if given |
| duration_seconds | integer | optional, must be greater than 0 if given |

### Relationships

- A `WorkoutExercise` belongs to a `Workout`.
- A `WorkoutExercise` belongs to an `Exercise`.
- A `Workout` has many `WorkoutExercise`s.
- An `Exercise` has many `WorkoutExercise`s.
- A `Workout` has many `Exercise`s through `WorkoutExercise`s.
- An `Exercise` has many `Workout`s through `WorkoutExercise`s.

Deleting a workout or an exercise also deletes its related `WorkoutExercise` rows (cascade delete).

## Validations

### Table constraints (database level)

- `exercises.name` must be unique.
- `workouts.duration_minutes` must be greater than 0 (check constraint).
- `workout_exercises.sets` must be greater than 0 (check constraint).
- `name`, `category`, `equipment_needed`, `date`, `duration_minutes`, `workout_id` and `exercise_id` cannot be null.

### Model validations (Python level)

- `Exercise.name` and `Exercise.category` cannot be empty.
- `Workout.duration_minutes` must be a positive number.
- `WorkoutExercise.sets`, `reps` and `duration_seconds` must be positive when provided.

### Schema validations (request level)

- `name` and `category` must be at least 1 character long.
- `duration_minutes` must be at least 1.
- `sets`, `reps` and `duration_seconds` must be at least 1 when provided.
- Required fields must be present, and dates must be valid (`YYYY-MM-DD`).

## API endpoints

### Workouts

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/workouts` | List all workouts (without their exercises) | 200 |
| GET | `/workouts/<id>` | Show one workout with its exercises, including sets, reps and duration | 200 |
| POST | `/workouts` | Create a workout | 201 |
| DELETE | `/workouts/<id>` | Delete a workout and its workout-exercise rows | 204 |

### Exercises

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/exercises` | List all exercises (without their workouts) | 200 |
| GET | `/exercises/<id>` | Show one exercise with the workouts it appears in | 200 |
| POST | `/exercises` | Create an exercise | 201 |
| DELETE | `/exercises/<id>` | Delete an exercise and its workout-exercise rows | 204 |

### Adding an exercise to a workout

| Method | Endpoint | Description | Success |
|---|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout, with sets, reps and/or duration | 201 |

The workout and exercise ids come from the URL. The request body only contains the optional `sets`, `reps` and `duration_seconds`.

### Error responses

| Status | When |
|---|---|
| 400 | The request body failed validation. The response has an `errors` object describing each problem. |
| 404 | The workout or exercise with the given id does not exist. |

## Example requests

Create a workout:

```bash
curl -X POST http://127.0.0.1:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-11-02", "duration_minutes": 40, "notes": "Leg day"}'
```

Response (201):

```json
{
  "date": "2026-11-02",
  "duration_minutes": 40,
  "id": 4,
  "notes": "Leg day",
  "workout_exercises": []
}
```

Create an exercise:

```bash
curl -X POST http://127.0.0.1:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Lunges", "category": "Strength", "equipment_needed": false}'
```

Add an exercise to a workout (exercise 3 to workout 3):

```bash
curl -X POST http://127.0.0.1:5555/workouts/3/exercises/3/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"sets": 2, "duration_seconds": 45}'
```

Invalid request (returns 400):

```bash
curl -X POST http://127.0.0.1:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-11-02", "duration_minutes": 0}'
```

```json
{
  "errors": {
    "duration_minutes": ["Must be greater than or equal to 1."]
  }
}
```

Delete a workout:

```bash
curl -i -X DELETE http://127.0.0.1:5555/workouts/4
```

## Resetting the data

Run `python seed.py` from the `server` folder at any time to wipe the database tables and restore the example data.

## Author

Abdulmajid ([@majidmaestro](https://github.com/majidmaestro))
