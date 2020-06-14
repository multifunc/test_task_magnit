
CREATE TABLE IF NOT EXISTS
    regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL
    );

CREATE INDEX idx_region on regions(name);

CREATE TABLE IF NOT EXISTS
    cities(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    region_id INT,
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE
    );

CREATE INDEX idx_city on cities(name);

CREATE TABLE IF NOT EXISTS
    comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    city_id INT(12) DEFAULT NULL,
    phone VARCHAR(25),
    email VARCHAR(50),
    comment TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
    );

CREATE INDEX idx_user on comments(last_name, first_name);


INSERT INTO regions(name)
VALUES ("Ставропольский край");
INSERT INTO regions(name)
VALUES ("Ростовская область");
INSERT INTO regions(name)
VALUES ("Краснодарский край");

INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Ростовская область" LIMIT 1), "Батайск");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Ростовская область" LIMIT 1), "Ростов");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Ростовская область" LIMIT 1), "Шахты");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Краснодарский край" LIMIT 1), "Славянск");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Краснодарский край" LIMIT 1), "Кропоткин");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Краснодарский край" LIMIT 1), "Краснодар");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Ставропольский край" LIMIT 1), "Пятигорск");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Ставропольский край" LIMIT 1), "Кисловодск");
INSERT INTO cities(region_id, name)
VALUES ((SELECT id FROM regions WHERE name = "Ставропольский край" LIMIT 1), "Ставрополь");

INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Петров", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Ростов" LIMIT 1), "Китай");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Баширов", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Ростов" LIMIT 1), "COVID-19");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Никифоренко", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Ростов" LIMIT 1), "Инвестиции");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Ким", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Кропоткин" LIMIT 1), "Эльбрус");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Шу", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Кропоткин" LIMIT 1), "FIDE");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Черная", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Кропоткин" LIMIT 1), "#СидимДома");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Малыш", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Краснодар" LIMIT 1), "Свободу!");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Лобунец", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Краснодар" LIMIT 1), "Сво-бо-ду!");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Лавров", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Краснодар" LIMIT 1), "Сво-бо-ду попугаям!");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Иванов", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Краснодар" LIMIT 1), "Карантин");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Саламонов", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Краснодар" LIMIT 1), "Отпуск в заперти!");
INSERT INTO comments(last_name, first_name, patronymic, city_id, comment) VALUES ("Кондратьев", "Александр", "Савельевич", (SELECT id FROM cities WHERE name = "Краснодар" LIMIT 1), "А я - итуичу.");

INSERT INTO comments(last_name, first_name, patronymic, phone, email, comment) VALUES ("Самойлов", "Александр", "Савельевич", "(861) 7789857", "adadas_13@ya.ru", "Ура!");
INSERT INTO comments(last_name, first_name, patronymic, phone, email, comment) VALUES ("Сидор", "Александр", "Савельевич", "(861) 7892453", "alibaba_13@ya.ru", "Заработало!");
INSERT INTO comments(last_name, first_name, patronymic, phone, email, comment) VALUES ("Белов", "Александр", "Савельевич", "(892) 6325894", "kfc_macauto13@ya.ru", "Наггетсы.");

