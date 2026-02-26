-- Очищаем таблицы
TRUNCATE organization_activity, organizations, activities, buildings RESTART IDENTITY CASCADE;

-- 1. Здания
INSERT INTO buildings (address, latitude, longitude) VALUES 
('ул. Ленина 1, Москва', 55.7558, 37.6176),
('ул. Тверская 5, Москва', 55.7658, 37.6076),
('пр-т Мира 10, Москва', 55.7834, 37.6316),
('ул. Арбат 15, Москва', 55.7512, 37.5903),
('Кутузовский пр-т 20, Москва', 55.7396, 37.5347);

-- 2. Деятельности
-- Уровень 0
INSERT INTO activities (name, parent_id) VALUES 
('Еда', NULL),
('Автомобили', NULL);

-- Уровень 1
INSERT INTO activities (name, parent_id) VALUES 
('Мясная продукция', 1),
('Молочная продукция', 1),
('Грузовые автомобили', 2),
('Легковые автомобили', 2);

-- Уровень 2
INSERT INTO activities (name, parent_id) VALUES 
('Колбасные изделия', 3),
('Сыры', 4),
('Запчасти', 6),
('Аксессуары', 6);

-- 3. Организации
INSERT INTO organizations (name, building_id, phone_numbers) VALUES 
('Мясной двор', 1, '["+7-495-123-45-67", "+7-495-765-43-21"]'::jsonb),
('Сыроварня', 2, '["+7-495-234-56-78"]'::jsonb),
('Автосалон', 3, '["+7-495-345-67-89", "+7-495-456-78-90"]'::jsonb),
('Автозапчасти', 4, '["+7-495-567-89-01"]'::jsonb),
('Универсальный магазин', 5, '["+7-495-678-90-12"]'::jsonb);

-- 4. Связи организаций с деятельностями
-- Мясной двор (id=1) -> Мясная продукция (3), Колбаса (7)
INSERT INTO organization_activity (organization_id, activity_id) VALUES 
(1, 3), (1, 7);

-- Сыроварня (2) -> Молочная продукция (4), Сыры (8)
INSERT INTO organization_activity (organization_id, activity_id) VALUES 
(2, 4), (2, 8);

-- Автосалон (3) -> Автомобили (2), Легковые (6)
INSERT INTO organization_activity (organization_id, activity_id) VALUES 
(3, 2), (3, 6);

-- Автозапчасти (4) -> Запчасти (9)
INSERT INTO organization_activity (organization_id, activity_id) VALUES 
(4, 9);

-- Универсальный (5) -> Еда (1), Мясная (3), Молочная (4)
INSERT INTO organization_activity (organization_id, activity_id) VALUES 
(5, 1), (5, 3), (5, 4);
