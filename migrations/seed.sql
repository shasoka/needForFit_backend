-- Добавление пользователей
INSERT INTO users (username, password) VALUES
    ('admin', 'admin_password');

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
INSERT INTO global_stats (uid, ttl_weight, ttl_reps, ttl_time, max_weight)
SELECT
    1,
    COALESCE(SUM(a.weight), 0),
    COALESCE(SUM(a.reps), 0),
    COALESCE(SUM(a.time), 0),
    COALESCE(MAX(a.weight), 0)
FROM approaches a
JOIN workouts w ON a.wid = w.id
WHERE w.uid = 1;
