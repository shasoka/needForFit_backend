DROP DATABASE IF EXISTS nff;

CREATE DATABASE nff WITH ENCODING 'UTF8';

\c nff;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(255) NOT NULL DEFAULT 'localhost:8000/static/images/users/profile_picture_placeholder.png',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workout_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    uid INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS day_phrase (
    id SERIAL PRIMARY KEY,
    phrase VARCHAR(255) NOT NULL,
    uid INTEGER REFERENCES users(id) UNIQUE
);

CREATE TABLE IF NOT EXISTS workouts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL DEFAULT 'New workout',
    uid INTEGER REFERENCES users(id),
    tid INTEGER REFERENCES workout_types(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS global_stats (
    id SERIAL PRIMARY KEY,
    uid INTEGER REFERENCES users(id),
    ttl_weight INTEGER NOT NULL,
    ttl_reps INTEGER NOT NULL,
    max_weight INTEGER NOT NULL,
    ttl_workouts INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS exercise_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    image VARCHAR(255),
    image_url VARCHAR(255),
    video_url VARCHAR(255),
    tid INTEGER REFERENCES exercise_types(id)
);

CREATE TABLE IF NOT EXISTS approaches (
    id SERIAL PRIMARY KEY,
    wid INTEGER REFERENCES workouts(id),
    eid INTEGER REFERENCES exercises(id),
    reps INTEGER,
    weight INTEGER,
    time DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS local_stats (
    id SERIAL PRIMARY KEY,
    wid INTEGER REFERENCES workouts(id) UNIQUE,
    exercises_count INTEGER,
    max_weights JSONB,
    max_reps JSONB,
    favorite_exercise VARCHAR(255),
    total_weight INTEGER
);
