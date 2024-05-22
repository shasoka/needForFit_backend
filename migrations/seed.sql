-- Добавление пользователей
INSERT INTO users (username, password) VALUES
    ('admin', '$2b$12$0t9enudPMHYmlnRI04XNq.pA272KnUi.BD22yo46TjfHgXGhkC2dy');
    -- admin;admin

-- Добавление упражнений
INSERT INTO exercises (name, description, image) VALUES
    ('Squats', 'Basic exercise for the lower body', NULL),
    ('Bench Press', 'Exercise for the upper body', NULL),
    ('Deadlift', 'Complex exercise for the whole body', NULL),
    ('Overhead Barbell Press', 'Exercise for shoulders and triceps', NULL),
    ('Pull-Ups', 'Exercise for the upper body', NULL),
    ('Plank', 'Exercise for core stabilization', NULL),
    ('Hammer Curls', 'Isolation exercise for biceps', NULL),
    ('Lunges', 'Leg workout, emphasis on glutes and quadriceps', NULL),
    ('Dumbbell Row to Abdomen', 'Exercise for back and biceps', NULL),
    ('Push-Ups', 'Chest and triceps workout', NULL),
    ('Crunches', 'Abdominal workout', NULL),
    ('Leg Press', 'Leg workout, emphasis on thighs and glutes', NULL),
    ('Calf Raises', 'Isolation exercise for calves', NULL),
    ('Dips', 'Triceps and chest workout', NULL),
    ('Russian Twists', 'Workout for oblique abdominal muscles', NULL),
    ('Lat Pulldown', 'Back and biceps workout', NULL),
    ('Hammer Curls for Biceps', 'Isolation exercise for biceps', NULL),
    ('Reverse Crunches', 'Lower abdominal workout', NULL),
    ('Side Plank', 'Exercise for core stabilization', NULL),
    ('Triceps Extensions', 'Isolation exercise for triceps', NULL);


-- Добавление тренировок
INSERT INTO workouts (uid)
SELECT 1 FROM generate_series(1, 20);

-- Добавление подходов
INSERT INTO approaches (wid, eid, reps, weight, time)
SELECT
    w.id,
    e.id,
    CASE WHEN e.id % 2 = 0 THEN 10 ELSE 12 END,
    CASE WHEN e.id % 3 = 0 THEN 135 ELSE 115 END,
    NULL
FROM workouts w, exercises e
WHERE w.id <= 20;

-- Добавление глобальной статистики
INSERT INTO global_stats (uid, ttl_weight, ttl_reps, max_weight, ttl_workouts)
SELECT
    1,
    COALESCE(SUM(a.weight), 0) AS ttl_weight,
    COALESCE(SUM(a.reps), 0) AS ttl_reps,
    COALESCE(MAX(a.weight), 0) AS max_weight,
    COALESCE(COUNT(DISTINCT w.id), 0) AS ttl_workouts
FROM approaches a
JOIN workouts w ON a.wid = w.id
WHERE w.uid = 1;

-- Добавление типов упражнений
INSERT INTO exercise_types (name) VALUES
    ('Legs'),
    ('Chest'),
    ('Back'),
    ('Shoulders'),
    ('Arms'),
    ('Core');

-- Обновление таблицы упражнений (exercises) с добавлением типов
UPDATE exercises SET tid = 1 WHERE name IN ('Squats', 'Lunges', 'Leg Press', 'Calf Raises');
UPDATE exercises SET tid = 2 WHERE name IN ('Bench Press', 'Push-Ups', 'Dips');
UPDATE exercises SET tid = 3 WHERE name IN ('Deadlift', 'Dumbbell Row to Abdomen', 'Lat Pulldown', 'Pull-Ups');
UPDATE exercises SET tid = 4 WHERE name IN ('Overhead Barbell Press', 'Triceps Extensions');
UPDATE exercises SET tid = 5 WHERE name IN ('Hammer Curls', 'Hammer Curls for Biceps');
UPDATE exercises SET tid = 6 WHERE name IN ('Plank', 'Crunches', 'Russian Twists', 'Reverse Crunches', 'Side Plank');

INSERT INTO workout_types (name, uid) VALUES
                                     ('Strength', 1),
                                     ('Cardio', 1),
                                     ('Whole body', 1),
                                     ('Legs', 1),
                                     ('Chest', 1),
                                     ('Arms', 1);

INSERT INTO day_phrase (phrase, uid) VALUES
                                         ('First phrase', null),
                                         ('Second phrase', null),
                                         ('Third phrase', null);

UPDATE workouts SET tid = 1 WHERE id <= 3;
UPDATE workouts SET tid = 2 WHERE id <= 6 AND id > 3;
UPDATE workouts SET tid = 3 WHERE id <= 9 AND id > 6;
UPDATE workouts SET tid = 4 WHERE id <= 12 AND id > 9;
UPDATE workouts SET tid = 5 WHERE id <= 15 AND id > 12;
UPDATE workouts SET tid = 6 WHERE id > 15;
