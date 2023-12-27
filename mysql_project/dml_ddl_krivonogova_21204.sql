DROP DATABASE IF EXISTS test_dml_ddl;
CREATE DATABASE test_dml_ddl;;

USE test_dml_ddl;

#creating of schema
CREATE TABLE Судно (
    Идентификатор INT PRIMARY KEY AUTO_INCREMENT,
    Название VARCHAR(50) NOT NULL,
    Порт_приписки VARCHAR(50) NOT NULL,
    Льгота FLOAT NOT NULL CHECK ( Льгота >= 0 AND Льгота <= 100 )
);

CREATE TABLE Место_погрузки (
    Идентификатор INT PRIMARY KEY AUTO_INCREMENT,
    Причал VARCHAR(50) NOT NULL,
    Порт VARCHAR(50) NOT NULL,
    Отчисления_на_погрузку FLOAT NOT NULL CHECK ( Отчисления_на_погрузку >= 0 AND Отчисления_на_погрузку <= 100 )
);

CREATE TABLE Груз (
    Идентификатор INT PRIMARY KEY AUTO_INCREMENT,
    Название VARCHAR(50) NOT NULL,
    Порт_складирования VARCHAR(50) NOT NULL,
    Стоимость INT NOT NULL CHECK ( Стоимость >= 0 ),
    Максимальное_количество INT NOT NULL CHECK ( Максимальное_количество >= 0 )
);

CREATE TABLE Погрузка (
    Номер_ведомости INT PRIMARY KEY AUTO_INCREMENT,
    Дата DATE,
    Судно INT,
    Место_погрузки INT,
    Груз INT NOT NULL,
    Количество INT NOT NULL CHECK ( Количество >= 0 ),
    Стоимость INT NOT NULL CHECK ( Стоимость >= 0 )
);

ALTER TABLE Погрузка ADD CONSTRAINT погрузка_судно_внешний_ключ
    FOREIGN KEY ( Судно ) REFERENCES Судно ( Идентификатор ) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Погрузка ADD CONSTRAINT погрузка_место_погрузки_внешний_ключ
    FOREIGN KEY ( Судно ) REFERENCES Место_погрузки ( Идентификатор ) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Погрузка ADD CONSTRAINT погрузка_груз_внешний_ключ
    FOREIGN KEY ( Судно ) REFERENCES Груз ( Идентификатор ) ON DELETE SET NULL ON UPDATE CASCADE;


#inserting data into tables
INSERT INTO Судно( Идентификатор, Название, Порт_приписки, Льгота )
    VALUES (1, 'ADMIRAL NAHIMOV','VLADIVOSTOK', 3),
    (2, 'BISTRY',         'NAHODKA',     2),
    (3, 'ADM TRADING 1',  'NEW YORK',    4),
    (4, 'POLAR STAR',     'BALTIMORE',   5),
    (5, 'JOHN GREY',      'NEW ORLEANS', 1),
    (6, 'LUCKY',          'TORONTO',     1),
    (7, 'LUNA',           'SAKHALIN',    7),
    (8, 'NADEZHNY',       'YUZHNY',      4),
    (9, 'PETROV',         'RIGA',        5);


INSERT INTO Место_погрузки( Идентификатор, Причал, Порт, Отчисления_на_погрузку )
    VALUES (1, 'PRICHAL 1','VLADIVOSTOK',3),
    (2, 'PRICHAL 2','VLADIVOSTOK',4),
    (3, 'PRICHAL 4','VLADIVOSTOK',5),
    (4, 'PRICHAL 1','NAHODKA',6),
    (5, 'PRICHAL 3','NAHODKA',3),
    (6, 'PRICHAL 8','NEW YORK',5),
    (7, 'PRICHAL 2','NEW YORK',8),
    (8, 'PRICHAL 3','BALTIMORE',4),
    (9, 'PRICHAL 6','BALTIMORE',4),
    (10, 'PRICHAL 1','SAKHALIN',4),
    (11, 'PRICHAL 2','SAKHALIN',7),
    (12, 'PRICHAL 3','RIGA',3);


INSERT INTO Груз( Идентификатор, Название, Порт_складирования, Стоимость, Максимальное_количество )
    VALUES (1, 'COMPUTERS',     'RIGA',       3000000, 10000),
    (2, 'PRODUCTI',      'SAKHALIN',   430000,  12300 ),
    (3, 'NEFT',          'NEW ORLEANS',10000000,40030),
    (4, 'LES',           'YUZHNY',     653000,  50000),
    (5, 'ORUZHIE',       'NEW YORK',   460000,  98000),
    (6, 'METALL',        'NAHODKA',    830000,  400000),
    (7, 'GAZ',           'VLADIVOSTOK',750000,  410000),
    (8, 'STROIMATERIALI','TORONTO',    750400,  8900000 ),
    (9, 'ZHIVOTNIE',     'NAHODKA',    1900000, 350000 ),
    (10, 'HIMIKATI',     'YUZHNY',     484200,  50430),
    (11, 'MEDPREPARATI', 'SAKHALIN',   7592300, 463000),
    (12, 'TOVARI',       'RIGA',       753000,  100000);


INSERT INTO Погрузка( Номер_ведомости, Дата, Судно, Место_погрузки, Груз, Количество, Стоимость )
    VALUES (1  ,STR_TO_DATE('5.05.2002', '%d.%m.%Y'),1 , 1, 2 , 6000,  5600000),
    (2  ,STR_TO_DATE('8.06.2002', '%d.%m.%Y'),1 ,12, 2 , 7000,  4356000),
    (3  ,STR_TO_DATE('14.07.2002', '%d.%m.%Y'),2 , 3, 4 , 45000, 1200000),
    (4  ,STR_TO_DATE('17.07.2002', '%d.%m.%Y'),3 , 4, 5 , 34000, 328800),
    (5  ,STR_TO_DATE('24.07.2002', '%d.%m.%Y'),1 , 5, 8 , 45000, 370000),
    (6  ,STR_TO_DATE('4.08.2002', '%d.%m.%Y'),4 , 6, 12, 50089, 4100000),
    (7  ,STR_TO_DATE('7.08.2002', '%d.%m.%Y'),5 , 4, 2 , 30000, 8500000),
    (8  ,STR_TO_DATE('14.08.2002', '%d.%m.%Y'),1 , 8, 4 , 20000, 2600000),
    (9  ,STR_TO_DATE('19.08.2002', '%d.%m.%Y'),6 , 9, 7 , 67000, 4200000),
    (10 ,STR_TO_DATE('25.08.2002', '%d.%m.%Y'),8 ,11, 8 , 67008, 3400000),
    (11 ,STR_TO_DATE('5.09.2002', '%d.%m.%Y'),9 ,12, 3 , 10000, 850000),
    (12 ,STR_TO_DATE('9.09.2002', '%d.%m.%Y'),9 ,1 , 6 , 13000, 34000000),
    (13 ,STR_TO_DATE('1.10.2002', '%d.%m.%Y'),5 ,2 , 7 , 78000, 4200000),
    (14 ,STR_TO_DATE('7.10.2002', '%d.%m.%Y'),4 ,3 , 3 , 50000, 948000),
    (15 ,STR_TO_DATE('15.10.2002', '%d.%m.%Y'),3 ,7 , 9 , 43000, 5340000),
    (16 ,STR_TO_DATE('21.10.2002', '%d.%m.%Y'),2 ,6 , 4 , 9000,  3260000),
    (17 ,STR_TO_DATE('8.11.2002', '%d.%m.%Y'),2 ,3 , 1 , 7000,  4270000),
    (18 ,STR_TO_DATE('18.11.2002', '%d.%m.%Y'),8 ,4 , 9 , 50000, 5400000),
    (19 ,STR_TO_DATE('27.11.2002', '%d.%m.%Y'),7 ,5 , 10, 60000, 4300000),
    (20 ,STR_TO_DATE('8.12.2002', '%d.%m.%Y'),7 ,6 , 11, 45000, 4360000),
    (21 ,STR_TO_DATE('18.12.2002', '%d.%m.%Y'),9 ,2 , 11, 83000, 150000);



#query 1
SELECT DISTINCT Название, Льгота, Порт, Причал
FROM Судно
    LEFT JOIN Погрузка
        ON Судно.Идентификатор = Погрузка.Судно
    LEFT JOIN Место_погрузки
        ON Погрузка.Место_погрузки = Место_погрузки.Идентификатор
ORDER BY Название;



#query 2
SELECT Название, Место_погрузки.Причал
FROM Судно
    INNER JOIN Погрузка
        ON Судно.Идентификатор = Погрузка.Судно
    INNER JOIN Место_погрузки
        ON Погрузка.Место_погрузки = Место_погрузки.Идентификатор
WHERE Отчисления_на_погрузку > 3
  AND Место_погрузки.Порт <> Судно.Порт_приписки
ORDER BY Название;



#query 3
WITH места_погрузки_владивосток AS (
    SELECT Идентификатор
    FROM Место_погрузки
    WHERE Порт LIKE 'VLADIVOSTOK'
),
судна_погрузки_владивосток AS (
    SELECT DISTINCT Название
    FROM Судно
        INNER JOIN Погрузка
            ON Судно.Идентификатор = Погрузка.Судно
    WHERE Место_погрузки IN (SELECT *
                             FROM места_погрузки_владивосток)
)
SELECT Название, Порт, Причал
FROM Судно
LEFT JOIN Погрузка
    ON Судно.Идентификатор = Погрузка.Судно
LEFT JOIN Место_погрузки
    ON Погрузка.Место_погрузки = Место_погрузки.Идентификатор
WHERE Название NOT IN (
    SELECT * FROM судна_погрузки_владивосток
)
ORDER BY Порт;



#query 4
WITH погрузки_за_период AS (
    SELECT * FROM Погрузка
    WHERE Дата BETWEEN '2002-06-01' AND '2002-09-01'
),
максимальная_стоимость AS (
    SELECT MAX(Стоимость)
    FROM погрузки_за_период
),
судна_с_самой_дорогой_погрузкой AS (
    SELECT *
    FROM погрузки_за_период
    WHERE Стоимость = (
        SELECT * FROM максимальная_стоимость
    )
)
SELECT Название, Порт_приписки
FROM Судно
WHERE Судно.Идентификатор IN (
    SELECT Судно
    FROM судна_с_самой_дорогой_погрузкой
)
ORDER BY Название;



#query 5
WITH погрузки_за_период AS (
    SELECT * FROM Погрузка
    WHERE Дата BETWEEN '2002-05-01' AND '2002-10-15'
),
судна_рига_балтимор AS (
    SELECT Идентификатор
    FROM Судно
    WHERE Судно.Порт_приписки IN ('RIGA', 'BALTIMORE')
),
места_погрузки_рига_балтимор AS (
    SELECT Место_погрузки
    FROM погрузки_за_период
    WHERE Судно IN (
        SELECT * FROM судна_рига_балтимор
    )
)
SELECT Порт, Причал
FROM Место_погрузки
WHERE Идентификатор IN (
    SELECT *
    FROM места_погрузки_рига_балтимор
)
ORDER BY Порт;



#query 6
WITH места_погрузки_находка_владивосток AS (
    SELECT Идентификатор
    FROM Место_погрузки
    WHERE Порт IN ('NAHODKA', 'VLADIVOSTOK')
),
судна_находка_владивосток AS (
    SELECT DISTINCT Судно
    FROM Погрузка
    WHERE Место_погрузки IN (
        SELECT *
        FROM места_погрузки_находка_владивосток
    )
),
средняя_льгота AS (
    SELECT AVG(Льгота)
    FROM Судно
)
SELECT Название
FROM Судно
WHERE Идентификатор IN (
    SELECT * FROM судна_находка_владивосток
)
AND Льгота < (
    SELECT *
    FROM средняя_льгота
)
ORDER BY Название;



#deleting of schema
ALTER TABLE Погрузка DROP CONSTRAINT погрузка_судно_внешний_ключ;
ALTER TABLE Погрузка DROP CONSTRAINT погрузка_место_погрузки_внешний_ключ;
ALTER TABLE Погрузка DROP CONSTRAINT погрузка_груз_внешний_ключ;
DROP TABLE Судно;
DROP TABLE Место_погрузки;
DROP TABLE Груз;
DROP TABLE Погрузка;
