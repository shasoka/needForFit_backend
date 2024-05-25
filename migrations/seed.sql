-- Добавление пользователей
INSERT INTO users (username, password) VALUES
    ('admin', '$2b$12$0t9enudPMHYmlnRI04XNq.pA272KnUi.BD22yo46TjfHgXGhkC2dy');
    -- admin;admin

-- Добавление упражнений
INSERT INTO exercises (name, description, image) VALUES
    ('Приседания', 'Базовое упражнение для нижней части тела', NULL),
    ('Жим лежа', 'Упражнение для верхней части тела', NULL),
    ('Становая тяга', 'Комплексное упражнение для всего тела', NULL),
    ('Жим штанги над головой', 'Упражнение для плеч и трицепса', NULL),
    ('Подтягивания', 'Упражнение для верхней части тела', NULL),
    ('Планка', 'Упражнение для стабилизации ядра', NULL),
    ('Молотки', 'Изолирующее упражнение для бицепса', NULL),
    ('Выпады', 'Тренировка ног, акцент на ягодицы и квадрицепсы', NULL),
    ('Тяга гантели к животу', 'Упражнение для спины и бицепса', NULL),
    ('Отжимания', 'Тренировка груди и трицепса', NULL),
    ('Скручивания', 'Тренировка пресса', NULL),
    ('Лег-пресс', 'Тренировка ног, акцент на бедра и ягодицы', NULL),
    ('Подъемы на носки', 'Изолирующее упражнение для икр', NULL),
    ('Дипсы', 'Тренировка трицепса и груди', NULL),
    ('Русские скручивания', 'Тренировка для косых мышц живота', NULL),
    ('Тяга штанги к груди в наклоне', 'Тренировка спины и бицепса', NULL),
    ('Молотки для бицепса', 'Изолирующее упражнение для бицепса', NULL),
    ('Обратные скручивания', 'Тренировка нижнего пресса', NULL),
    ('Боковая планка', 'Упражнение для стабилизации ядра', NULL),
    ('Разгибание рук на блоке', 'Изолирующее упражнение для трицепса', NULL);

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

-- Вычисляем количество упражнений, максимальный вес, максимальное количество повторений и общий вес для каждой тренировки
WITH stats AS (
    SELECT
        wid,
        COUNT(DISTINCT eid) AS exercises_count,
        jsonb_object_agg(name, max_weight) AS max_weights,
        jsonb_object_agg(name, max_reps) AS max_reps,
        SUM(weight) AS total_weight
    FROM (
        SELECT
            approaches.wid,
            approaches.eid,
            exercises.name,
			approaches.weight,
            MAX(approaches.weight) AS max_weight,
            MAX(approaches.reps) AS max_reps
        FROM approaches
        JOIN exercises ON approaches.eid = exercises.id
        GROUP BY approaches.wid, approaches.eid, exercises.name, approaches.weight
    ) AS subquery
    GROUP BY wid
),

-- Вычисляем упражнение с максимальным количеством подходов для каждой тренировки
favourite_exercise AS (
    SELECT
        wid,
        eid,
        ROW_NUMBER() OVER(PARTITION BY wid ORDER BY COUNT(*) DESC) as rn
    FROM approaches
    GROUP BY wid, eid
)

-- Вставляем вычисленные статистики в таблицу local_stats
INSERT INTO local_stats (wid, exercises_count, max_weights, max_reps, favorite_exercise, total_weight)
SELECT
    s.wid,
    s.exercises_count,
    s.max_weights,
    s.max_reps,
    (SELECT name FROM exercises WHERE id = f.eid),
    s.total_weight
FROM stats s
JOIN favourite_exercise f ON s.wid = f.wid AND f.rn = 1;

-- Добавление типов упражнений
INSERT INTO exercise_types (name) VALUES
    ('Ноги'),
    ('Грудь'),
    ('Спина'),
    ('Плечи'),
    ('Руки'),
    ('Торс');

-- Обновление таблицы упражнений (exercises) с добавлением типов
UPDATE exercises SET tid = 1 WHERE name IN ('Приседания', 'Выпады', 'Лег-пресс', 'Подъемы на носки');
UPDATE exercises SET tid = 2 WHERE name IN ('Жим лежа', 'Отжимания', 'Дипсы');
UPDATE exercises SET tid = 3 WHERE name IN ('Становая тяга', 'Тяга гантели к животу', 'Тяга штанги к груди в наклоне', 'Подтягивания');
UPDATE exercises SET tid = 4 WHERE name IN ('Жим штанги над головой', 'Разгибание рук на блоке');
UPDATE exercises SET tid = 5 WHERE name IN ('Молотки', 'Молотки для бицепса');
UPDATE exercises SET tid = 6 WHERE name IN ('Планка', 'Скручивания', 'Русские скручивания', 'Обратные скручивания', 'Боковая планка');

-- Добавление типов тренировок --
INSERT INTO workout_types (name, uid) VALUES
                                     ('Силовая', 1),
                                     ('Кардио', 1),
                                     ('На все тело', 1),
                                     ('Ноги', 1),
                                     ('Грудь', 1),
                                     ('Руки', 1);

UPDATE workouts SET tid = 1 WHERE id <= 3;
UPDATE workouts SET tid = 2 WHERE id <= 6 AND id > 3;
UPDATE workouts SET tid = 3 WHERE id <= 9 AND id > 6;
UPDATE workouts SET tid = 4 WHERE id <= 12 AND id > 9;
UPDATE workouts SET tid = 5 WHERE id <= 15 AND id > 12;
UPDATE workouts SET tid = 6 WHERE id > 15;

-- Добавление фраз дня --
INSERT INTO day_phrase (phrase, uid) VALUES
                                         ('Запомни: всего одна ошибка – и ты ошибся', null),
                                         ('Никогда не сдавайтесь, идите к своей цели! А если будет сложно – сдавайтесь', null),
                                         ('Делай, как надо. Как не надо, не делай', null),
                                         ('Ты можешь все, что захочешь. Но не все, что захочешь, ты можешь', null),
                                         ('Если грустно - выпей чаю. Станет легче, отвечаю', null),
                                         ('Все будет, но не сразу...', null);
