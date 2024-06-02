import mysql.connector
from mysql.connector import errorcode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    window.geometry(f'{width}x{height}+{x}+{y}')


# настройки по умолчанию для подключения к локальному серверу
host = "localhost"
port = 3306
root = None
admin_window = None
mydb = None

def save_settings():
    global host, port, user, password
    host = host_entry.get()
    port = port_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    settings_window.destroy()
    connect_to_database()

def on_closing_settings():
    settings_window.destroy()
    print("Завершение работы приложения")
    try:
        exit(0)
    except:
        print("Работа приложения завершена")

def set_style_button(widget):
    widget.configure(bg='lightgray', font=('Arial', 12))

def set_style_frame(widget):
    widget.configure(bg='lightblue')

def set_style_label(widget):
    widget.configure(font=('Arial', 12))

def set_style_entry(widget):
    widget.configure(font=('Arial', 12))

def open_settings_window():
    global host_entry, port_entry, user_entry, password_entry, settings_window
    settings_window = tk.Tk()
    settings_window.protocol("WM_DELETE_WINDOW", on_closing_settings)
    settings_window.geometry("400x400")
    settings_window.title("Настройки базы данных")
    settings_window.configure(bg='lightblue')
    center_window(settings_window, 400, 400)

    frame = tk.Frame(settings_window)
    frame.pack(expand=True)

    host_label = ttk.Label(frame, text="Хост:")
    host_label.pack()
    set_style_label(host_label)
    host_entry = ttk.Entry(frame)
    host_entry.insert(0, host)
    host_entry.pack()
    set_style_entry(host_entry)

    port_label = ttk.Label(frame, text="Порт:")
    port_label.pack()
    set_style_label(port_label)
    port_entry = ttk.Entry(frame)
    port_entry.insert(0, port)
    port_entry.pack()
    set_style_entry(port_entry)

    user_label = ttk.Label(frame, text="Пользователь:")
    user_label.pack()
    set_style_label(user_label)
    user_entry = ttk.Entry(frame)
    user_entry.pack()
    set_style_entry(user_entry)

    password_label = ttk.Label(frame, text="Пароль:")
    password_label.pack()
    set_style_label(password_label)
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack()
    set_style_entry(password_entry)

    save_button = tk.Button(frame, text="Подключиться", command=save_settings)
    save_button.pack()
    set_style_button(save_button)

    settings_window.focus_force()
    settings_window.mainloop()
    try:
        exit(0)
    except:
        print("Работа приложения завершена")


# Установка соединения с базой данных
def connect_to_database():
    try:
        global mydb
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        
    except mysql.connector.Error as err:        
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror(
                    "Error", "Неверные учетные данные")
            exit_function()
            
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            messagebox.showerror(
                    "Error", "База данных не существует")
            exit_function()
        else:
            messagebox.showerror("Error", err)
            exit_function()


    if (user == "root"):
        with mydb.cursor() as mycursor:
            try:
                # Создание базы данных db_project
                mycursor.execute("DROP DATABASE IF EXISTS medical_organisations_db;")
                mycursor.execute("CREATE DATABASE IF NOT EXISTS medical_organisations_db;")
                mycursor.execute("USE medical_organisations_db;")

                # Создание роли для администратора
                mycursor.execute("DROP USER IF EXISTS 'admin'@'localhost';")
                mycursor.execute("DROP ROLE IF EXISTS 'admin_role';")
                mycursor.execute("CREATE ROLE 'admin_role';")
                mycursor.execute("GRANT CREATE USER ON *.* TO 'admin_role' WITH GRANT OPTION;")
                mycursor.execute("GRANT ALL PRIVILEGES ON medical_organisations_db.* TO 'admin_role' WITH GRANT OPTION;")
                mycursor.execute("GRANT SUPER ON *.* TO 'admin_role' WITH GRANT OPTION;")

                mycursor.execute("CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';")
                mycursor.execute("GRANT 'admin_role' TO 'admin'@'localhost';")
                mycursor.execute("SET DEFAULT ROLE ALL TO 'admin'@'localhost';")

                # Создание таблиц
                mycursor.execute("CREATE TABLE \
                                Doctor (doctor_id int PRIMARY KEY AUTO_INCREMENT, \
                                last_name varchar(50) NOT NULL, \
                                name varchar(50) NOT NULL, \
                                patronymic varchar(50), \
                                phone varchar(11), \
                                work_experience int CHECK (work_experience >= 0))")

                mycursor.execute("CREATE TABLE \
                                Medical_organisation (medical_organisation_id int PRIMARY KEY AUTO_INCREMENT, \
                                name varchar(100) NOT NULL, \
                                address varchar(100) NOT NULL, \
                                phone varchar(11))")

                mycursor.execute("CREATE TABLE \
                                Hospital (medical_organisation_id int PRIMARY KEY AUTO_INCREMENT, \
                                medical_corps_amount int NOT NULL CHECK(medical_corps_amount >= 1))")

                mycursor.execute("CREATE TABLE \
                                Polyclinic (medical_organisation_id int PRIMARY KEY AUTO_INCREMENT, \
                                district varchar(50) NOT NULL)")

                mycursor.execute("CREATE TABLE \
                                Doctor_Medical_organisation (doctor_id int NOT NULL, \
                                medical_organisation_id int NOT NULL, \
                                hire_date date NOT NULL, \
                                PRIMARY KEY (doctor_id, medical_organisation_id, hire_date))")

                mycursor.execute("CREATE TABLE \
                                Patient (patient_id int PRIMARY KEY AUTO_INCREMENT, \
                                last_name varchar(50) NOT NULL, \
                                name varchar(50) NOT NULL, \
                                patronymic varchar(50), \
                                birthday date NOT NULL, \
                                phone varchar(11), \
                                address varchar(100) NOT NULL, \
                                policy_number varchar(16), \
                                polyclinic_id int)")

                mycursor.execute("CREATE TABLE \
                                Treatment (treatment_id int PRIMARY KEY AUTO_INCREMENT, \
                                patient_id int NOT NULL, \
                                doctor_id int NOT NULL, \
                                medical_organisation_id int NOT NULL, \
                                disease varchar(100) NOT NULL, \
                                date date NOT NULL, \
                                description varchar(1000))")

                mycursor.execute("CREATE TABLE \
                                Diseases_history (record_id int PRIMARY KEY AUTO_INCREMENT, \
                                patient_id int NOT NULL, \
                                disease varchar(100) NOT NULL, \
                                date_of_diagnosis date NOT NULL)")

                mycursor.execute("CREATE TABLE \
                                Treatment_registration (registration_id int PRIMARY KEY AUTO_INCREMENT, \
                                patient_id int NOT NULL, \
                                doctor_id int NOT NULL, \
                                medical_organisation_id int NOT NULL, \
                                date date NOT NULL, \
                                completed BOOLEAN NOT NULL DEFAULT 0)")

                mycursor.execute("CREATE TABLE \
                                User_patient (login varchar(100) NOT NULL, \
                                patient_id int NOT NULL, \
                                PRIMARY KEY (patient_id))")
                
                mycursor.execute("CREATE TABLE \
                                User_Doctor (login varchar(100) NOT NULL, \
                                doctor_id int NOT NULL, \
                                PRIMARY KEY (doctor_id))")
                
                mycursor.execute("CREATE TABLE \
                                User_medical_organisation (login varchar(100) NOT NULL, \
                                medical_organisation_id int NOT NULL, \
                                PRIMARY KEY (medical_organisation_id))")

                # Добавление внешних ключей
                mycursor.execute("ALTER TABLE Polyclinic \
                                ADD CONSTRAINT polyclinic_medical_organisation \
                                FOREIGN KEY ( medical_organisation_id ) REFERENCES Medical_organisation ( medical_organisation_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")

                mycursor.execute("ALTER TABLE Hospital \
                                ADD CONSTRAINT hospital_medical_organisation \
                                FOREIGN KEY ( medical_organisation_id ) REFERENCES Medical_organisation ( medical_organisation_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")

                mycursor.execute("ALTER TABLE Doctor_Medical_organisation \
                                ADD CONSTRAINT doctor_medical_organisation_medical_organisation \
                                FOREIGN KEY ( medical_organisation_id ) REFERENCES Medical_organisation ( medical_organisation_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                mycursor.execute("ALTER TABLE Doctor_Medical_organisation \
                                ADD CONSTRAINT doctor_medical_organisation_doctor \
                                FOREIGN KEY ( doctor_id ) REFERENCES Doctor ( doctor_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")

                mycursor.execute("ALTER TABLE Patient \
                                ADD CONSTRAINT patient_polyclinic \
                                FOREIGN KEY ( polyclinic_id ) REFERENCES Polyclinic ( medical_organisation_id ) \
                                ON DELETE SET NULL ON UPDATE CASCADE")

                mycursor.execute("ALTER TABLE Treatment \
                                ADD CONSTRAINT treatment_patient \
                                FOREIGN KEY ( patient_id ) REFERENCES Patient ( patient_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                mycursor.execute("ALTER TABLE Treatment \
                                ADD CONSTRAINT treatment_doctor \
                                FOREIGN KEY ( doctor_id ) REFERENCES Doctor ( doctor_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                mycursor.execute("ALTER TABLE Treatment \
                                ADD CONSTRAINT treatment_medical_organisation \
                                FOREIGN KEY ( medical_organisation_id ) REFERENCES Medical_organisation ( medical_organisation_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")

                mycursor.execute("ALTER TABLE Treatment_registration \
                                ADD CONSTRAINT treatment_registration_patient \
                                FOREIGN KEY ( patient_id ) REFERENCES Patient ( patient_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                mycursor.execute("ALTER TABLE Treatment_registration \
                                ADD CONSTRAINT treatment_registration_doctor \
                                FOREIGN KEY ( doctor_id ) REFERENCES Doctor ( doctor_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                mycursor.execute("ALTER TABLE Treatment_registration \
                                ADD CONSTRAINT treatment_registration_medical_organisation \
                                FOREIGN KEY ( medical_organisation_id ) REFERENCES Medical_organisation ( medical_organisation_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")

                mycursor.execute("ALTER TABLE Diseases_history \
                                ADD CONSTRAINT diseases_history_patient \
                                FOREIGN KEY ( patient_id ) REFERENCES Patient ( patient_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                
                mycursor.execute("ALTER TABLE User_patient \
                                ADD CONSTRAINT user_patient_patient \
                                FOREIGN KEY ( patient_id ) REFERENCES Patient ( patient_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                
                mycursor.execute("ALTER TABLE User_Doctor \
                                ADD CONSTRAINT user_doctor_doctor \
                                FOREIGN KEY ( doctor_id ) REFERENCES Doctor ( doctor_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")
                
                mycursor.execute("ALTER TABLE User_medical_organisation \
                                ADD CONSTRAINT user_medical_organisation_medical_organisation \
                                FOREIGN KEY ( medical_organisation_id ) REFERENCES Medical_organisation ( medical_organisation_id ) \
                                ON DELETE CASCADE ON UPDATE CASCADE")

                # Создание триггеров
                mycursor.execute("CREATE TRIGGER treatment_after_insert AFTER INSERT \
                                ON Treatment \
                                FOR EACH ROW \
                                INSERT INTO Diseases_history(patient_id, disease, date_of_diagnosis) \
                                VALUES (NEW.patient_id, NEW.disease, NEW.date);")

                mycursor.execute("CREATE TRIGGER treatment_after_update AFTER UPDATE \
                                ON Treatment \
                                FOR EACH ROW \
                                UPDATE Diseases_history SET patient_id = NEW.patient_id, \
                                disease = NEW.disease, date_of_diagnosis = NEW.date \
                                WHERE patient_id = OLD.patient_id and disease = OLD.disease \
                                and date_of_diagnosis = OLD.date;")
                
                mycursor.execute("CREATE TRIGGER complete_treatment AFTER INSERT \
                                ON Treatment \
                                FOR EACH ROW \
                                UPDATE Treatment_registration SET completed = 1 \
                                WHERE Treatment_registration.patient_id = NEW.patient_id and Treatment_registration.doctor_id = NEW.doctor_id \
                                and Treatment_registration.medical_organisation_id = NEW.medical_organisation_id and Treatment_registration.date = NEW.date")

                mycursor.execute("CREATE TRIGGER polyclinic_after_delete AFTER DELETE \
                                ON Polyclinic \
                                FOR EACH ROW \
                                DELETE FROM Medical_organisation \
                                WHERE OLD.medical_organisation_id = Medical_organisation.medical_organisation_id;")

                mycursor.execute("CREATE TRIGGER hospital_after_delete AFTER DELETE \
                                ON Hospital \
                                FOR EACH ROW \
                                DELETE FROM Medical_organisation \
                                WHERE OLD.medical_organisation_id = Medical_organisation.medical_organisation_id;")

                mycursor.execute("CREATE TRIGGER doctor_name_before_insert \
                                BEFORE INSERT ON Doctor \
                                FOR EACH ROW \
                                SET NEW.last_name = CONCAT(UCASE(SUBSTRING(NEW.last_name, 1, 1)),LCASE(SUBSTRING(NEW.last_name, 2))), \
                                NEW.name = CONCAT(UCASE(SUBSTRING(NEW.name, 1, 1)),LCASE(SUBSTRING(NEW.name, 2))), \
                                NEW.patronymic = CONCAT(UCASE(SUBSTRING(NEW.patronymic, 1, 1)),LCASE(SUBSTRING(NEW.patronymic, 2)));")
                
                mycursor.execute("CREATE TRIGGER doctor_name_before_update \
                                BEFORE UPDATE ON Doctor \
                                FOR EACH ROW \
                                SET NEW.last_name = CONCAT(UCASE(SUBSTRING(NEW.last_name, 1, 1)),LCASE(SUBSTRING(NEW.last_name, 2))), \
                                NEW.name = CONCAT(UCASE(SUBSTRING(NEW.name, 1, 1)),LCASE(SUBSTRING(NEW.name, 2))), \
                                NEW.patronymic = CONCAT(UCASE(SUBSTRING(NEW.patronymic, 1, 1)),LCASE(SUBSTRING(NEW.patronymic, 2)));")

                mycursor.execute("CREATE TRIGGER patient_name_before_insert \
                                BEFORE INSERT ON Patient \
                                FOR EACH ROW \
                                SET NEW.last_name = CONCAT(UCASE(SUBSTRING(NEW.last_name, 1, 1)),LCASE(SUBSTRING(NEW.last_name, 2))), \
                                NEW.name = CONCAT(UCASE(SUBSTRING(NEW.name, 1, 1)),LCASE(SUBSTRING(NEW.name, 2))), \
                                NEW.patronymic = CONCAT(UCASE(SUBSTRING(NEW.patronymic, 1, 1)),LCASE(SUBSTRING(NEW.patronymic, 2)));")
                
                mycursor.execute("CREATE TRIGGER patient_name_before_update \
                                BEFORE UPDATE ON Patient \
                                FOR EACH ROW \
                                SET NEW.last_name = CONCAT(UCASE(SUBSTRING(NEW.last_name, 1, 1)),LCASE(SUBSTRING(NEW.last_name, 2))), \
                                NEW.name = CONCAT(UCASE(SUBSTRING(NEW.name, 1, 1)),LCASE(SUBSTRING(NEW.name, 2))), \
                                NEW.patronymic = CONCAT(UCASE(SUBSTRING(NEW.patronymic, 1, 1)),LCASE(SUBSTRING(NEW.patronymic, 2)));")

                # Создание хранимых процедур
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_treatment_statistics( \
                                IN current_medical_organisation_id INT, \
                                IN start_date DATE, \
                                IN end_date DATE) \
                                    SELECT t.treatment_id, p.last_name AS patient_last_name, p.name AS patient_name, p.patronymic AS patient_patronymic, \
                                            d.last_name AS doctor_last_name, d.name AS doctor_name, d.patronymic AS doctor_patronymic, \
                                            disease, date \
                                    FROM Treatment t \
                                    INNER JOIN Patient p ON t.patient_id = p.patient_id \
                                    INNER JOIN Doctor d ON t.doctor_id = d.doctor_id \
                                    INNER JOIN Medical_organisation mo ON t.medical_organisation_id = mo.medical_organisation_id \
                                    WHERE t.medical_organisation_id = current_medical_organisation_id \
                                    AND (DATE(date) BETWEEN DATE(start_date) AND DATE(end_date));")

                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_treatment_description( \
                                IN treatment_id INT) \
                                    SELECT t.description \
                                    FROM Treatment t \
                                    WHERE t.treatment_id = treatment_id")

                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_registered_patients_list( \
                                IN current_doctor_id INT, \
                                IN current_medical_organisation_id INT) \
                                SELECT Patient.patient_id, Patient.last_name, Patient.name, Patient.patronymic \
                                FROM Treatment_registration \
                                INNER JOIN Patient ON Treatment_registration.patient_id = Patient.patient_id \
                                WHERE doctor_id = current_doctor_id \
                                AND medical_organisation_id = current_medical_organisation_id \
                                AND date = CURRENT_DATE() \
                                AND completed = 0;")
                
                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.add_polyclinic(
                    name varchar(100),
                    address varchar(100),
                    phone varchar(11),
                    district varchar(50)
                )
                BEGIN
                    DECLARE new_id INT;
                    DECLARE new_user_name VARCHAR(150);
                    
                    DECLARE EXIT HANDLER FOR SQLEXCEPTION
                    BEGIN
                        ROLLBACK;
                        RESIGNAL SET MESSAGE_TEXT = 'Error creating user';
                    END;

                    START TRANSACTION;

                    INSERT INTO Medical_organisation(name, address, phone)
                    VALUES(name, address, phone);

                    SET new_id = LAST_INSERT_ID();

                    INSERT INTO Polyclinic(medical_organisation_id, district)
                    VALUES(new_id, district);

                    SET new_user_name = CONCAT(REPLACE(name, ' ', ''), '_', new_id);

                    BEGIN
                        DECLARE user_count INT;
                        DECLARE CONTINUE HANDLER FOR SQLSTATE '42000'
                        BEGIN
                            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error creating user.';
                        END;

                        SET user_count = (SELECT COUNT(*) FROM mysql.user WHERE User = new_user_name);
                        
                        IF user_count > 0 THEN
                            SIGNAL SQLSTATE '45000'
                            SET MESSAGE_TEXT = 'Error creating user.';
                        ELSE
                            SET @create_user_query = CONCAT('CREATE USER ', new_user_name, '@\\\'localhost\\\' IDENTIFIED BY \\\'', new_user_name, '\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('GRANT \\\'medical_organisation_role\\\' TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('SET DEFAULT ROLE ALL TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            INSERT INTO User_medical_organisation(login, medical_organisation_id) VALUES(new_user_name, new_id);
                            COMMIT;
                        END IF;
                        
                    END;
                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")


                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.add_hospital(
                    name varchar(100),
                    address varchar(100),
                    phone varchar(11),
                    medical_corps_amount varchar(50)
                )
                BEGIN
                    DECLARE new_id INT;
                    DECLARE new_user_name VARCHAR(150);
                    
                    DECLARE EXIT HANDLER FOR SQLEXCEPTION
                    BEGIN
                        ROLLBACK;
                        RESIGNAL SET MESSAGE_TEXT = 'Error creating user';
                    END;

                    START TRANSACTION;

                    INSERT INTO Medical_organisation(name, address, phone)
                    VALUES(name, address, phone);

                    SET new_id = LAST_INSERT_ID();

                    INSERT INTO Hospital(medical_organisation_id, medical_corps_amount)
                    VALUES(new_id, medical_corps_amount);

                    SET new_user_name = CONCAT(REPLACE(name, ' ', ''), '_', new_id);

                    BEGIN
                        DECLARE user_count INT;
                        DECLARE CONTINUE HANDLER FOR SQLSTATE '42000'
                        BEGIN
                            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error creating user.';
                        END;

                        SET user_count = (SELECT COUNT(*) FROM mysql.user WHERE User = new_user_name);
                        
                        IF user_count > 0 THEN
                            SIGNAL SQLSTATE '45000'
                            SET MESSAGE_TEXT = 'Error creating user.';
                        ELSE
                            SET @create_user_query = CONCAT('CREATE USER ', new_user_name, '@\\\'localhost\\\' IDENTIFIED BY \\\'', new_user_name, '\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('GRANT \\\'medical_organisation_role\\\' TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('SET DEFAULT ROLE ALL TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            INSERT INTO User_medical_organisation(login, medical_organisation_id) VALUES(new_user_name, new_id);
                            COMMIT;
                        END IF;
                        
                    END;
                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")


                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.delete_medical_organisation(
                    IN medical_organisation_id INT
                )
                BEGIN
                    DECLARE deleted_user_login VARCHAR(255);
                    DECLARE num_records INT;

                    START TRANSACTION;
                    
                    SELECT login INTO deleted_user_login FROM User_medical_organisation WHERE User_medical_organisation.medical_organisation_id = medical_organisation_id;

                    DELETE FROM User_medical_organisation WHERE User_medical_organisation.login = deleted_user_login AND User_medical_organisation.medical_organisation_id = medical_organisation_id;

                    SET @create_user_query = CONCAT('DROP USER IF EXISTS ', deleted_user_login, '@\\\'localhost\\\'');
                    PREPARE create_user_stmt FROM @create_user_query;
                    EXECUTE create_user_stmt;
                    DEALLOCATE PREPARE create_user_stmt;

                    DELETE FROM Medical_organisation WHERE Medical_organisation.medical_organisation_id = medical_organisation_id;
                    COMMIT;
                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")


                mycursor.execute("CREATE PROCEDURE medical_organisations_db.add_existed_doctor( \
                                IN doctor_id INT, \
                                IN medical_organisation_id INT) \
                                    INSERT INTO Doctor_Medical_organisation(doctor_id, medical_organisation_id, hire_date) \
                                    VALUES(doctor_id, medical_organisation_id, CURRENT_DATE());")

                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.update_doctor_in_medical_organisation( \
                                    doctor_id int, \
                                    last_name varchar(50), \
                                    name varchar(50), \
                                    patronymic varchar(50), \
                                    phone varchar(11), \
                                    work_experience int, \
                                    medical_organisation_id int \
                                ) \
                                UPDATE Doctor AS d \
                                    INNER JOIN Doctor_Medical_organisation AS dmo \
                                        ON d.doctor_id = dmo.doctor_id \
                                    SET d.last_name = last_name, \
                                        d.name = name, \
                                        d.patronymic = patronymic, \
                                        d.phone = phone, \
                                        d.work_experience = work_experience, \
                                        dmo.medical_organisation_id = medical_organisation_id \
                                    WHERE d.doctor_id = doctor_id AND d.doctor_id = dmo.doctor_id;")

                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.delete_doctor_from_medical_organisation(
                    IN doctor_id INT, IN medical_organisation_id INT
                )
                BEGIN
                    DECLARE deleted_user_login VARCHAR(255);
                    DECLARE num_records INT;

                    START TRANSACTION;
                    
                    DELETE FROM Doctor_Medical_organisation WHERE Doctor_Medical_organisation.doctor_id = doctor_id AND Doctor_Medical_organisation.medical_organisation_id = medical_organisation_id;
                    
                    SELECT COUNT(*) INTO num_records FROM Doctor_Medical_organisation WHERE Doctor_Medical_organisation.doctor_id = doctor_id;
                    IF num_records = 0 THEN
                    BEGIN
                        SELECT login INTO deleted_user_login FROM User_Doctor WHERE User_Doctor.doctor_id = doctor_id;

                        DELETE FROM User_Doctor WHERE User_Doctor.login = deleted_user_login AND User_Doctor.doctor_id = doctor_id;

                        SET @create_user_query = CONCAT('DROP USER IF EXISTS ', deleted_user_login, '@\\\'localhost\\\'');
                        PREPARE create_user_stmt FROM @create_user_query;
                        EXECUTE create_user_stmt;
                        DEALLOCATE PREPARE create_user_stmt;

                        DELETE FROM Doctor WHERE Doctor.doctor_id = doctor_id;
                    END; END IF;
                    COMMIT;
                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")


                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.insert_doctor_to_medical_organisation(
                    last_name varchar(50),
                    name varchar(50),
                    patronymic varchar(50),
                    phone varchar(11),
                    work_experience int,
                    medical_organisation_id int
                )
                BEGIN
                    DECLARE new_id INT;
                    DECLARE new_user_name VARCHAR(150);
                    
                    DECLARE EXIT HANDLER FOR SQLEXCEPTION
                    BEGIN
                        ROLLBACK;
                        RESIGNAL SET MESSAGE_TEXT = 'Error creating user.';
                    END;

                    START TRANSACTION;

                    INSERT INTO Doctor(last_name, name, patronymic, phone, work_experience)
                    VALUES(last_name, name, patronymic, phone, work_experience);

                    SET new_id = LAST_INSERT_ID();

                    INSERT INTO Doctor_Medical_organisation(doctor_id, medical_organisation_id, hire_date)
                    VALUES(new_id, medical_organisation_id, CURRENT_DATE());

                    SET new_user_name = CONCAT(REPLACE(last_name, ' ', ''), '_', REPLACE(name, ' ', ''), '_', new_id);

                    BEGIN
                        DECLARE user_count INT;
                        DECLARE CONTINUE HANDLER FOR SQLSTATE '42000'
                        BEGIN
                            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error creating user.';
                        END;

                        SET user_count = (SELECT COUNT(*) FROM mysql.user WHERE User = new_user_name);
                        
                        IF user_count > 0 THEN
                            SIGNAL SQLSTATE '45000'
                            SET MESSAGE_TEXT = 'Error creating user.';
                        ELSE
                            SET @create_user_query = CONCAT('CREATE USER ', new_user_name, '@\\\'localhost\\\' IDENTIFIED BY \\\'', new_user_name, '\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('GRANT \\\'doctor_role\\\' TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('SET DEFAULT ROLE ALL TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            INSERT INTO User_Doctor(login, doctor_id) VALUES(new_user_name, new_id);
                            COMMIT;
                        END IF;
                        
                    END;
                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")

                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_patients_registrations( \
                                IN patient_id INT) \
                                    SELECT  d.last_name, \
                                            d.name, \
                                            d.patronymic, \
                                            mo.name as medical_organisation_name, \
                                            mo.address, \
                                            t.date \
                                    FROM Treatment_registration as t \
                                        INNER JOIN Doctor as d ON t.doctor_id = d.doctor_id \
                                        INNER JOIN Medical_organisation as mo ON t.medical_organisation_id = mo.medical_organisation_id \
                                    WHERE t.patient_id = patient_id AND date >= CURRENT_DATE() AND completed = 0;")
                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_medical_organisations_by_doctor( \
                                IN doctor_id INT) \
                                    SELECT  mo.medical_organisation_id, \
                                            mo.name, \
                                            mo.address \
                                    FROM Doctor_Medical_organisation as dmo \
                                        INNER JOIN Doctor as d ON dmo.doctor_id = d.doctor_id \
                                        INNER JOIN Medical_organisation as mo ON dmo.medical_organisation_id = mo.medical_organisation_id \
                                    WHERE d.doctor_id = doctor_id;")
                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_doctors_by_medical_organisation( \
                                IN medical_organisation_id INT) \
                                    SELECT  DISTINCT d.doctor_id, \
                                            d.last_name, \
                                            d.name, \
                                            d.patronymic \
                                    FROM Doctor_Medical_organisation as dmo \
                                        INNER JOIN Doctor as d ON dmo.doctor_id = d.doctor_id \
                                        INNER JOIN Medical_organisation as mo ON dmo.medical_organisation_id = mo.medical_organisation_id \
                                    WHERE mo.medical_organisation_id = medical_organisation_id;")
                

                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.add_patient_to_polyclinic(
                                    last_name varchar(50),
                                    name varchar(50),
                                    patronymic varchar(50),
                                    birthday date,
                                    phone varchar(11),
                                    address varchar(100),
                                    policy_number varchar(16),
                                    polyclinic_id int
                )
                BEGIN
                    DECLARE new_id INT;
                    DECLARE new_user_name VARCHAR(150);

                    DECLARE EXIT HANDLER FOR SQLEXCEPTION
                    BEGIN
                        ROLLBACK;
                        RESIGNAL SET MESSAGE_TEXT = 'Error creating user.';
                    END;

                    START TRANSACTION;

                    INSERT INTO Patient(last_name, name, patronymic, birthday, phone, address, policy_number, polyclinic_id)
                            VALUES(last_name, name, patronymic, birthday, phone, address, policy_number, polyclinic_id);

                    SET new_id = LAST_INSERT_ID();

                    SET new_user_name = CONCAT(REPLACE(last_name, ' ', ''), '_', REPLACE(name, ' ', ''), '_', new_id);

                    BEGIN
                        DECLARE user_count INT;
                        DECLARE CONTINUE HANDLER FOR SQLSTATE '42000'
                        BEGIN
                            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error creating user.';
                        END;

                        SET user_count = (SELECT COUNT(*) FROM mysql.user WHERE User = new_user_name);
                        
                        IF user_count > 0 THEN
                            SIGNAL SQLSTATE '45000'
                            SET MESSAGE_TEXT = 'Error creating user.';
                        ELSE
                            SET @create_user_query = CONCAT('CREATE USER ', new_user_name, '@\\\'localhost\\\' IDENTIFIED BY \\\'', new_user_name, '\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('GRANT \\\'patient_role\\\' TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;

                            SET @create_user_query = CONCAT('SET DEFAULT ROLE ALL TO ', new_user_name, '@\\\'localhost\\\'');
                            PREPARE create_user_stmt FROM @create_user_query;
                            EXECUTE create_user_stmt;
                            DEALLOCATE PREPARE create_user_stmt;
                            
                            INSERT INTO User_patient(login, patient_id) VALUES(new_user_name, new_id);

                            COMMIT;
                        END IF;
                        
                    END;
                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")

                mycursor.execute("CREATE PROCEDURE medical_organisations_db.update_patient_in_polyclinic( \
                                    patient_id int, \
                                    last_name varchar(50), \
                                    name varchar(50), \
                                    patronymic varchar(50), \
                                    birthday date, \
                                    phone varchar(11), \
                                    address varchar(100), \
                                    policy_number varchar(16), \
                                    polyclinic_id int \
                                ) \
                                UPDATE Patient AS p \
                                    SET p.last_name = last_name, \
                                        p.name = name, \
                                        p.patronymic = patronymic, \
                                        p.birthday = birthday, \
                                        p.phone = phone, \
                                        p.address = address, \
                                        p.policy_number = policy_number, \
                                        p.polyclinic_id = IF(polyclinic_id != -1, polyclinic_id, p.polyclinic_id) \
                                WHERE p.patient_id = patient_id;")

                
                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE PROCEDURE medical_organisations_db.delete_patient(
                                    id int
                )
                BEGIN
                    DECLARE deleted_patient_login VARCHAR(255);

                    SELECT login INTO deleted_patient_login FROM User_patient WHERE User_patient.patient_id = id;

                    SET @drop_patient_query = CONCAT('DROP USER IF EXISTS ', deleted_patient_login, '@\\\'localhost\\\'');
                    PREPARE drop_patient_stmt FROM @drop_patient_query;
                    EXECUTE drop_patient_stmt;
                    DEALLOCATE PREPARE drop_patient_stmt;

                    DELETE FROM User_patient WHERE User_patient.login = deleted_patient_login AND User_patient.patient_id = id;

                    DELETE FROM Patient WHERE Patient.patient_id = id;

                    COMMIT;

                END;
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")
                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.add_treatment( \
                                    patient_id int, \
                                    doctor_id int, \
                                    medical_organisation_id int, \
                                    disease varchar(100), \
                                    description varchar(100) \
                                ) \
                                INSERT INTO Treatment(patient_id, doctor_id, medical_organisation_id, disease, date, description) \
                                VALUES (patient_id, doctor_id, medical_organisation_id, disease, CURRENT_DATE(), description);")
                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_patient_user_id( \
                                    login varchar(100) \
                                ) \
                                SELECT patient_id \
                                FROM User_patient AS u \
                                    WHERE u.login = login;")
                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_doctor_user_id( \
                                    login varchar(100) \
                                ) \
                                SELECT doctor_id \
                                FROM User_Doctor AS u \
                                    WHERE u.login = login;")
                
                mycursor.execute("CREATE PROCEDURE medical_organisations_db.get_medical_organisation_user_id( \
                                    login varchar(100) \
                                ) \
                                SELECT medical_organisation_id \
                                FROM User_medical_organisation AS u \
                                    WHERE u.login = login;")
                
                # Создание хранимых функций
                mycursor.execute("SET autocommit = 0")
                create_function_query = """
                CREATE FUNCTION medical_organisations_db.get_patients_count_by_disease(current_disease VARCHAR(100), current_medical_organisation_id INT)
                RETURNS INT
                READS SQL DATA
                BEGIN
                    DECLARE patients_count INT;
                    SELECT COUNT(DISTINCT patient_id) INTO patients_count
                    FROM Treatment
                    WHERE disease = current_disease AND medical_organisation_id = current_medical_organisation_id;
                    RETURN patients_count;
                END
                """
                mycursor.execute(create_function_query)
                mycursor.execute("SET autocommit = 1")

                # # Создание внешней схемы для роли Пациент   
                mycursor.execute("CREATE VIEW Doctor_PatientUser_View \
                                AS SELECT  DISTINCT d.doctor_id, \
                                            d.last_name, \
                                            d.name, \
                                            d.patronymic, \
                                            mo.name as medical_organisation_name, \
                                            mo.address \
                                FROM Doctor as d INNER JOIN Doctor_Medical_organisation as dmo \
                                            ON d.doctor_id = dmo.doctor_id \
                                                INNER JOIN Medical_organisation as mo \
                                            ON dmo.medical_organisation_id = mo.medical_organisation_id") 
                
                mycursor.execute("CREATE VIEW Polyclinic_PatientUser_View \
                                AS SELECT  Polyclinic.medical_organisation_id, \
                                            name, \
                                            address, \
                                            phone, \
                                            district \
                                FROM   Medical_organisation INNER JOIN Polyclinic \
                                        ON Medical_organisation.medical_organisation_id = \
                                            Polyclinic.medical_organisation_id")
                
                mycursor.execute("CREATE VIEW Hospital_PatientUser_View \
                                AS SELECT  Hospital.medical_organisation_id, \
                                            name, \
                                            address, \
                                            phone, \
                                            medical_corps_amount \
                                FROM   Medical_organisation INNER JOIN Hospital \
                                        ON Medical_organisation.medical_organisation_id = \
                                            Hospital.medical_organisation_id")
                
                
                mycursor.execute("CREATE VIEW Treatment_registration_PatientUser_View \
                                AS SELECT  patient_id, \
                                            doctor_id, \
                                            medical_organisation_id, \
                                            date \
                                FROM Treatment_registration")
                
                # Создание внешней схемы для роли Руководитель медицинской организации
                mycursor.execute("CREATE VIEW Doctor_MedicalOrganisationUser_View \
                                AS SELECT  DISTINCT Doctor.doctor_id, \
                                            last_name, \
                                            name, \
                                            patronymic, \
                                            phone, \
                                            work_experience, \
                                            medical_organisation_id \
                                FROM Doctor INNER JOIN Doctor_Medical_organisation on Doctor.doctor_id = Doctor_Medical_organisation.doctor_id")
                
                # Создание внешней схемы для роли Врач
                mycursor.execute("CREATE VIEW Patient_DoctorUser_View \
                                AS SELECT  p.patient_id, \
                                            p.last_name, \
                                            p.name, \
                                            p.patronymic, \
                                            p.birthday, \
                                            p.phone, \
                                            p.address, \
                                            p.policy_number, \
                                            mo.name as Polyclinic_name \
                                FROM Patient AS p INNER JOIN Medical_organisation AS mo ON mo.medical_organisation_id = p.polyclinic_id") 
                
                mycursor.execute("CREATE VIEW Polyclinic_DoctorUser_View \
                                AS SELECT  Polyclinic.medical_organisation_id, \
                                            name, \
                                            address \
                                FROM   Medical_organisation INNER JOIN Polyclinic \
                                        ON Medical_organisation.medical_organisation_id = \
                                            Polyclinic.medical_organisation_id")
                
                # Создание внешней схемы для роли Администратор
                mycursor.execute("CREATE VIEW Medical_Organisation_AdminUser_View \
                                AS SELECT medical_organisation_id, \
                                            name, \
                                            address \
                                FROM Medical_organisation")
                
                # Заполнение таблиц данными
                doctor_data = [
                    ('Иванов', 'Иван', 'Иванович', '79991234567', 650),
                    ('Петров', 'Петр', 'Петрович', '79876543210', 4200),
                    ('Сидорова', 'Ольга', 'Владимировна', '79261112233', 300),
                    ('Козлов', 'Алексей', 'Сергеевич', '79105554433', 3900),
                    ('Михайлова', 'Екатерина', 'Андреевна', '79157778899', 3200),
                    ('Михайлов', 'Семен', 'Игоревич', '73583874861', 1040),
                    ('Иванова', 'Анна', 'Сергеевна', '79123456789', 879),
                    ('Петров', 'Игорь', 'Владимирович', '79234567890', 20),
                    ('Сидорова', 'Елена', 'Александровна', '79345678901', 410),
                    ('Козлов', 'Артем', 'Дмитриевич', '79456789012', 5450),
                    ('Михайлова', 'Ольга', 'Николаевна', '79567890123', 4000),
                ]

                medical_organisation_data = [
                    ('Центральная клиническая больница', 'Пирогова, 25/1', '73833304321'),
                    ('Бердская центральная городская больница',
                    'Новосибирская, 10', '73834155610'),
                    ('Городская клиническая больница №12',
                    'Морской проспект, 25', '88002000200'),
                    ('Новосибирская клиническая центральная районная больница',
                    'Магистральная, 3a', '79061959432'),
                    ('Городская клиническая больница №2', 'Ползунова, 21', '73833639507'),
                    ('Консультативно-диагностическая поликлиника №2',
                    'Морской проспект, 25', '73833066657'),
                    ('ЦНМТ', 'Пирогова, 25/4', '73833630183'),
                    ('Поликлиническое отделение №1', 'Шукшина, 3', '73833389747'),
                    ('Городская клиническая поликлиника №14', 'Демакова, 2', '73833047444'),
                    ('Клиника Санитас', 'Николаева, 12/3', '73832336600')
                ]

                hospital_data = [
                    (1, 2),
                    (2, 4),
                    (3, 1),
                    (4, 1),
                    (5, 6)
                ]

                polyclinic_data = [
                    (6, "Советский"),
                    (7, "Советский"),
                    (8, "Октябрьский"),
                    (9, "Советский"),
                    (10, "Советский")
                ]

                doctor_medical_organisation_data = [
                    (3, 5, datetime(2023, 12, 18)),
                    (8, 1, datetime(2010, 8, 19)),
                    (1, 9, datetime(2020, 6, 8)),
                    (2, 2, datetime(2014, 8, 14)),
                    (6, 8, datetime(2022, 10, 1)),
                    (4, 4, datetime(2016, 10, 21)),
                    (5, 5, datetime(2017, 12, 8)),
                    (3, 5, datetime(2021, 1, 19)),
                    (9, 1, datetime(2015, 9, 13)),
                    (7, 9, datetime(2018, 5, 5)),
                    (2, 2, datetime(2022, 3, 29)),
                    (10, 7, datetime(2024, 9, 30)),
                    (4, 4, datetime(2019, 4, 25)),
                    (10, 10, datetime(2017, 6, 2))
                ]

                patient_data = [
                    ('Смирнова', 'Ольга', 'Александровна', datetime(1987, 11, 25),
                    '79998887766', 'город Новосибирск, ул. Кирова 20', '1234567891234567', 7),
                    ('Кузнецов', 'Игорь', 'Петрович', datetime(1995, 4, 3), '79876543210',
                    'город Новосибирск, пр. Ленина 25', '9876543219876543', 9),
                    ('Николаева', 'Мария', 'Владимировна', datetime(1980, 9, 15),
                    '79112223344', 'город Новосибирск, ул. Пушкина 5', '5432167895432167', 6),
                    ('Павлов', 'Артем', 'Сергеевич', datetime(1983, 6, 30), '79255554433',
                    'город Новосибирск, ул. Гагарина 15', '2468135792468135', 8),
                    ('лебедев', 'иван', 'дмитриевич', datetime(1979, 2, 20), '79167778899',
                    'город Новосибирск, пр. Ленина 30', '1357924681357924', 10)
                ]

                treatment_registration_data = [
                    (1, 8, 6, datetime(2024, 2, 27)),
                    (3, 2, 2, datetime(2024, 1, 7)),
                    (2, 9, 7, datetime(2024, 3, 12)),
                    (3, 10, 10, datetime(2024, 3, 13)),
                    (4, 4, 4, datetime(2024, 3, 6)),
                    (4, 6, 8, datetime(2024, 1, 11)),
                    (2, 5, 5, datetime(2024, 2, 4)),
                    (1, 3, 9, datetime(2024, 3, 17)),
                    (3, 4, 4, datetime(2024, 2, 5)),
                    (4, 1, 9, datetime(2024, 3, 14)),
                    (5, 1, 8, datetime(2024, 4, 29)),
                    (1, 2, 2, datetime(2024, 4, 30)), 
                    (2, 3, 1, datetime(2024, 5, 1)),
                    (3, 4, 4, datetime(2024, 5, 2)),
                    (4, 5, 3, datetime(2024, 5, 3)),
                    (5, 6, 1, datetime(2024, 5, 4)),
                    (1, 7, 1, datetime(2024, 4, 29)),
                    (2, 8, 6, datetime(2024, 4, 30)), 
                    (3, 9, 7, datetime(2024, 5, 1)),
                    (4, 10, 10, datetime(2024, 5, 2)),
                    (5, 1, 8, datetime(2024, 5, 3)),
                    (1, 7, 10, datetime(2024, 5, 20)),
                    (2, 7, 10, datetime(2024, 5, 20)),
                    (3, 7, 10, datetime(2024, 5, 20)),
                    (4, 7, 10, datetime(2024, 5, 20)),
                    (5, 7, 10, datetime(2024, 5, 20))
                ]

                treatment_data = [
                    (1, 8, 6, "Пневмония", datetime(2024, 2, 27)),
                    (3, 1, 2, "Грипп", datetime(2024, 1, 8)),
                    (2, 9, 3, "Туберкулез", datetime(2024, 3, 12)),
                    (3, 10, 7, "Перелом руки", datetime(2024, 3, 13)),
                    (4, 4, 10, "Ангина", datetime(2024, 3, 6)),
                    (2, 6, 8, "Миопия", datetime(2024, 1, 13)),
                    (2, 5, 4, "Аллергия", datetime(2024, 2, 4)),
                    (1, 3, 9, "Стоматит", datetime(2024, 3, 17)),
                    (3, 4, 7, "Герпесная инфекция", datetime(2024, 2, 5)),
                    (4, 1, 5, "ОРВИ", datetime(2024, 3, 10)),
                    (1, 1, 5, "ОРВИ", datetime(2024, 3, 7)),
                    (2, 1, 5, "ОРВИ", datetime(2024, 3, 1)),
                    (2, 1, 5, "ОРВИ", datetime(2024, 3, 4))
                ]

                for data in doctor_data:
                    mycursor.execute(
                        "INSERT INTO Doctor(last_name, name, patronymic, phone, work_experience) VALUES (%s, %s, %s, %s, %s)", data)

                for data in medical_organisation_data:
                    mycursor.execute(
                        "INSERT INTO Medical_organisation(name, address, phone) VALUES (%s, %s, %s)", data)

                for data in hospital_data:
                    mycursor.execute(
                        "INSERT INTO Hospital(medical_organisation_id, medical_corps_amount) VALUES (%s, %s)", data)

                for data in polyclinic_data:
                    mycursor.execute(
                        "INSERT INTO Polyclinic(medical_organisation_id, district) VALUES (%s, %s)", data)

                for data in doctor_medical_organisation_data:
                    mycursor.execute(
                        "INSERT INTO Doctor_Medical_organisation(doctor_id, medical_organisation_id, hire_date) VALUES (%s, %s, %s)", data)

                for data in patient_data:
                    mycursor.execute(
                        "INSERT INTO Patient(last_name, name, patronymic, birthday, phone, address, policy_number, polyclinic_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", data)

                for data in treatment_registration_data:
                    mycursor.execute(
                        "INSERT INTO Treatment_registration(patient_id, medical_organisation_id, doctor_id, date) VALUES (%s, %s, %s, %s)", data)

                for data in treatment_data:
                    mycursor.execute(
                        "INSERT INTO Treatment(patient_id, medical_organisation_id, doctor_id, disease, date) VALUES (%s, %s, %s, %s, %s)", data)

                mydb.commit()

                messagebox.showinfo(
                    "Info", "База данных успешно создана.\nЛогин администратора: admin\nПароль администратора: admin\nПожалуйста, передайте администратору учетные данные для создания ролей и тестовых пользователей.")

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", err)
                try:
                    exit(0)
                except:
                    print("Работа приложения завершена")

        exit_function()
    # Здесь заканчивается работа системного администратора


    ######################### Пользователи системы: Руководители медицинских организаций, Врачи, Пациенты ################################
    # Подключение пользователя к базе данных
    with mydb.cursor() as mycursor:
        try:
            mycursor.execute("USE medical_organisations_db;")
            global role
            mycursor.execute("SELECT CURRENT_ROLE();")
            role = mycursor.fetchone()[0]
            role = role.split('@')[0][1:-1]
            print(role)

            if (role == 'admin_role'):
                # Окно администратора для создания пользовательских ролей и тестовых пользователей
                def on_closing():
                    try:
                        admin_window.destroy()
                        print("Окно администора закрыто")
                    except:
                        print("Окно администратора закрыто или не существует")
                    try:
                        mydb.close()
                        print("Соединение с базой данных закрыто")
                    except:
                        print("Не удалось закрыть соединение с базой данных")

                    print("Завершение работы приложения")
                    try:
                        exit(0)
                    except:
                        print("Работа приложения завершена")
                    
                def create_roles():
                    # Создание пользовательских ролей
                    with mydb.cursor() as mycursor:
                        try:
                            mycursor.execute("DROP ROLE IF EXISTS 'medical_organisation_role', 'doctor_role', 'patient_role';")
                            mycursor.execute("CREATE ROLE 'medical_organisation_role', 'doctor_role', 'patient_role';")

                            # Руководитель медицинской организации
                            mycursor.execute("GRANT CREATE USER ON *.* TO 'medical_organisation_role';")
                            mycursor.execute("GRANT SUPER ON *.* TO 'medical_organisation_role';")
                            mycursor.execute("GRANT SELECT, INSERT, DELETE ON medical_organisations_db.User_Doctor TO 'medical_organisation_role';")
                            mycursor.execute("GRANT SELECT ON medical_organisations_db.Doctor_MedicalOrganisationUser_View TO 'medical_organisation_role';")
                            
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_treatment_statistics TO 'medical_organisation_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_treatment_description TO 'medical_organisation_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.add_existed_doctor TO 'medical_organisation_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.update_doctor_in_medical_organisation TO 'medical_organisation_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.delete_doctor_from_medical_organisation TO 'medical_organisation_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.insert_doctor_to_medical_organisation TO 'medical_organisation_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_medical_organisation_user_id TO 'medical_organisation_role';")

                            mycursor.execute("GRANT EXECUTE ON FUNCTION medical_organisations_db.get_patients_count_by_disease TO 'medical_organisation_role';")
                            
                            # Врач
                            mycursor.execute("GRANT SELECT ON medical_organisations_db.Patient_DoctorUser_View TO 'doctor_role';")
                            mycursor.execute("GRANT SELECT ON medical_organisations_db.Polyclinic_DoctorUser_View TO 'doctor_role';")
                            
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_medical_organisations_by_doctor TO 'doctor_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_registered_patients_list TO 'doctor_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.add_patient_to_polyclinic TO 'doctor_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.update_patient_in_polyclinic TO 'doctor_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.delete_patient TO 'doctor_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.add_treatment TO 'doctor_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_doctor_user_id TO 'doctor_role';")

                            # Пациент
                            mycursor.execute("GRANT SELECT ON medical_organisations_db.Doctor_PatientUser_View TO 'patient_role';")
                            mycursor.execute("GRANT SELECT ON medical_organisations_db.Polyclinic_PatientUser_View TO 'patient_role';")
                            mycursor.execute("GRANT SELECT ON medical_organisations_db.Hospital_PatientUser_View TO 'patient_role';")
                            mycursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON medical_organisations_db.Treatment_registration_PatientUser_View TO 'patient_role';")
                            
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_patients_registrations TO 'patient_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_doctors_by_medical_organisation TO 'patient_role';")
                            mycursor.execute("GRANT EXECUTE ON PROCEDURE medical_organisations_db.get_patient_user_id TO 'patient_role';")


                            messagebox.showinfo("Info", "Роли созданы")
                            test_users_button['state'] = tk.NORMAL

                        except mysql.connector.Error as err:
                                messagebox.showerror("Error", f"Ошибка при создании пользовательских ролей: {err}")
                                exit_function()

                def create_test_users():
                    user_patient_data = [
                        ("Смирнова_Ольга_1", 1),
                        ("Кузнецов_Игорь_2", 2),
                        ("Николаева_Мария_3", 3),
                        ("Павлов_Артем_4", 4),
                        ("Лебедев_Иван_5", 5)
                    ]

                    user_doctor_data = [
                        ("Иванов_Иван_1", 1),
                        ("Петров_Петр_2", 2),
                        ("Сидорова_Ольга_3", 3),
                        ("Козлов_Алексей_4", 4),
                        ("Михайлова_Екатерина_5", 5),
                        ("Михайлов_Семен_6", 6),
                        ("Иванова_Анна_7", 7),
                        ("Петров_Игорь_8", 8),
                        ("Сидорова_Елена_9", 9),
                        ("Козлов_Артем_10", 10),
                        ("Михайлова_Ольга_11", 11)
                    ]

                    user_medical_organisation_data = [
                        ("цкб", 1),
                        ("бцгб", 2),
                        ("гкб", 3),
                        ("ткцрб", 4),
                        ("гкб2", 5),
                        ("кдп", 6),
                        ("цнмт", 7),
                        ("по", 8),
                        ("гкп", 9),
                        ("кс", 10)
                    ]

                    # Создание тестовых пользователей
                    with mydb.cursor() as mycursor:
                        try:
                            mycursor.execute("USE medical_organisations_db;")
                            for data in user_patient_data:
                                mycursor.execute(
                                    "INSERT INTO User_patient(login, patient_id) VALUES (%s, %s)", data)
                                
                            for data in user_doctor_data:
                                mycursor.execute(
                                    "INSERT INTO User_Doctor(login, doctor_id) VALUES (%s, %s)", data)
                                
                            for data in user_medical_organisation_data:
                                mycursor.execute(
                                    "INSERT INTO User_medical_organisation(login, medical_organisation_id) VALUES (%s, %s)", data)
                                

                            # Руководители медицинской организации
                            for data in user_medical_organisation_data:
                                mycursor.execute("DROP USER IF EXISTS %s@'localhost';", (data[0],))

                                mycursor.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s;", (data[0], data[0]))
                                mycursor.execute("GRANT 'medical_organisation_role' TO %s@'localhost';", (data[0],))
                                mycursor.execute("SET DEFAULT ROLE ALL TO %s@'localhost';", (data[0],))

                            # Врачи
                            for data in user_doctor_data:
                                mycursor.execute("DROP USER IF EXISTS %s@'localhost';", (data[0],))

                                mycursor.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s;", (data[0], data[0]))
                                mycursor.execute("GRANT 'doctor_role' TO %s@'localhost';", (data[0],))
                                mycursor.execute("SET DEFAULT ROLE ALL TO %s@'localhost';", (data[0],))

                            # Пациенты
                            for data in user_patient_data:
                                mycursor.execute("DROP USER IF EXISTS %s@'localhost';", (data[0],))

                                mycursor.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s;", (data[0], data[0]))
                                mycursor.execute("GRANT 'patient_role' TO %s@'localhost';", (data[0],))
                                mycursor.execute("SET DEFAULT ROLE ALL TO %s@'localhost';", (data[0],))


                            messagebox.showinfo("Info", "Тестовые пользователи созданы. Система готова к использованию")

                        except mysql.connector.Error as err:
                                messagebox.showerror("Error", f"Ошибка при создании тестовых пользователей: {err}")

                def create_polyclinic():
                    polyclinic_window = tk.Toplevel(admin_window)
                    polyclinic_window.title("Поликлиника")
                    polyclinic_window.geometry("400x400")
                    polyclinic_window.configure(bg='lightblue')
                    center_window(polyclinic_window, 400, 400)
                    polyclinic_window.focus_force()

                    def add_polyclinic():
                        name = name_entry.get()
                        address = address_entry.get()
                        phone = phone_entry.get()
                        district = district_entry.get()

                        if (name == "" or address == "" or district == ""):
                            messagebox.showinfo(
                                "Error", "Введите обязательные поля: Название, Адрес, Район")
                        else:
                            if (phone == ""):
                                phone = None

                            val = (name, address, phone, district)
                            try:
                                with mydb.cursor() as mycursor:
                                    mydb.commit()
                                    mycursor.callproc("add_polyclinic", val)
                                    mycursor.execute("SELECT LAST_INSERT_ID();")
                                    new_id = mycursor.fetchone()[0]
                                    new_user_name = name.replace(" ", "") + '_' + str(new_id)

                            except mysql.connector.Error as err:
                                messagebox.showerror(
                                    "Error", f"Ошибка сохранения руководителя медицинской организации: {err}. Возможно, имя занято. Попробуйте еще раз.")
                                
                            else:
                                mydb.commit()

                                messagebox.showinfo(
                                    "Success", f"Медицинская организация сохранена. Сообщите руководителю логин: {new_user_name} и пароль: {new_user_name} для входа.")
                                name_entry.delete(0, 'end')
                                address_entry.delete(0, 'end')
                                phone_entry.delete(0, 'end')
                                district_entry.delete(0, 'end')

                                polyclinic_window.destroy()
                                

                    help_label = tk.Label(polyclinic_window, text="Поля, помеченные *, обязательны для заполнения.")
                    help_label.pack()
                    name_label = tk.Label(polyclinic_window, text="*Название*:")
                    name_label.pack()
                    set_style_label(name_label)
                    name_entry = tk.Entry(polyclinic_window)
                    name_entry.pack()
                    set_style_entry(name_entry)

                    address_label = tk.Label(polyclinic_window, text="*Адрес*:")
                    address_label.pack()
                    set_style_label(address_label)
                    address_entry = tk.Entry(polyclinic_window)
                    address_entry.pack()
                    set_style_entry(address_entry)

                    phone_label = tk.Label(polyclinic_window,
                                        text="Номер телефона:")
                    phone_label.pack()
                    set_style_label(phone_label)
                    phone_entry = tk.Entry(polyclinic_window)
                    phone_entry.pack()
                    set_style_entry(phone_entry)

                    district_label = tk.Label(polyclinic_window, text="*Район*:")
                    district_label.pack()
                    set_style_label(district_label)
                    district_entry = tk.Entry(polyclinic_window)
                    district_entry.pack()
                    set_style_entry(district_entry)

                    add_polyclinic_button = tk.Button(
                        polyclinic_window, text="Сохранить", command=add_polyclinic)
                    add_polyclinic_button.pack()
                    set_style_button(add_polyclinic_button)

                def create_hospital():
                    hospital_window = tk.Toplevel(admin_window)
                    hospital_window.title("Больница")
                    hospital_window.geometry("400x400")
                    hospital_window.configure(bg='lightblue')
                    center_window(hospital_window, 400, 400)
                    hospital_window.focus_force()

                    def add_hospital():
                        name = name_entry.get()
                        address = address_entry.get()
                        phone = phone_entry.get()
                        medical_corps_amount = medical_corps_amount_entry.get()

                        if (name == "" or address == "" or medical_corps_amount == ""):
                            messagebox.showinfo(
                                "Error", "Введите обязательные поля: Название, Адрес, Количество корпусов")
                        else:
                            if (phone == ""):
                                phone = None

                            val = (name, address, phone, medical_corps_amount)
                            try:
                                with mydb.cursor() as mycursor:
                                    mydb.commit()
                                    mycursor.callproc("add_hospital", val)
                                    mycursor.execute("SELECT LAST_INSERT_ID();")
                                    new_id = mycursor.fetchone()[0]
                                    new_user_name = name.replace(" ", "") + '_' + str(new_id)

                            except mysql.connector.Error as err:
                                messagebox.showerror(
                                    "Error", f"Ошибка сохранения руководителя медицинской организации: {err}. Возможно, имя занято. Попробуйте еще раз.")
                                
                            else:
                                mydb.commit()

                                messagebox.showinfo(
                                    "Success", f"Медицинская организация сохранена. Сообщите руководителю логин: {new_user_name} и пароль: {new_user_name} для входа.")
                                name_entry.delete(0, 'end')
                                address_entry.delete(0, 'end')
                                phone_entry.delete(0, 'end')
                                medical_corps_amount_entry.delete(0, 'end')

                                hospital_window.destroy()

                    help_label = tk.Label(hospital_window, text="Поля, помеченные *, обязательны для заполнения.")
                    help_label.pack()
                    name_label = tk.Label(hospital_window, text="*Название*:")
                    name_label.pack()
                    set_style_label(name_label)
                    name_entry = tk.Entry(hospital_window)
                    name_entry.pack()
                    set_style_entry(name_entry)

                    address_label = tk.Label(hospital_window, text="*Адрес*:")
                    address_label.pack()
                    set_style_label(address_label)
                    address_entry = tk.Entry(hospital_window)
                    address_entry.pack()
                    set_style_entry(address_entry)

                    phone_label = tk.Label(hospital_window,
                                        text="Номер телефона:")
                    phone_label.pack()
                    set_style_label(phone_label)
                    phone_entry = tk.Entry(hospital_window)
                    phone_entry.pack()
                    set_style_entry(phone_entry)

                    medical_corps_amount_label = tk.Label(
                    hospital_window, text="*Количество корпусов*:")
                    medical_corps_amount_label.pack()
                    set_style_label(medical_corps_amount_label)
                    medical_corps_amount_entry = tk.Entry(hospital_window)
                    medical_corps_amount_entry.pack()
                    set_style_entry(medical_corps_amount_entry)

                    add_hospital_button = tk.Button(
                        hospital_window, text="Сохранить", command=add_hospital)
                    add_hospital_button.pack()
                    set_style_button(add_hospital_button)

                def delete_medical_organisation():
                    # функция отображения текцщих данных о медицинских организациях
                    def show_medical_organisations_admin_user(list_medical_organisations):
                        with mydb.cursor() as mycursor:
                            mycursor.execute("SELECT * FROM Medical_Organisation_AdminUser_View")
                            rows = mycursor.fetchall()

                            list_medical_organisations.delete(*list_medical_organisations.get_children())
                            list_medical_organisations["columns"] = ("id", "name", "address")
                            list_medical_organisations.heading("id", text="Идентификатор")
                            list_medical_organisations.heading("name", text="Медицинская организация")
                            list_medical_organisations.heading("address", text="Адрес")

                            for row in rows:
                                list_medical_organisations.insert("", "end", text=row[0], values=(row[0], row[1], row[2]))

                        # Добавляем возможность сортировки по столбцам
                        for col in ("id", "name", "address"):
                            list_medical_organisations.heading(col, text=col, command=lambda c=col: sort_treeview(list_medical_organisations, c, False))


                    medical_organisations_window = tk.Toplevel(admin_window)
                    medical_organisations_window.title("Медицинские организации")
                    medical_organisations_window.geometry("1300x500")

                    list_medical_organisations = ttk.Treeview(medical_organisations_window, columns=("id", "name", "address"), show="headings")
                    list_medical_organisations.place(y = 50, width=1250, height=420)
                    help_label = tk.Label(medical_organisations_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
                    help_label.place(x=0, y=470)

                    vsb = ttk.Scrollbar(medical_organisations_window, orient="vertical", command=list_medical_organisations.yview)
                    vsb.place(x=1250, y=0, height=500)
                    list_medical_organisations.configure(yscrollcommand=vsb.set)

                    show_polyclinics_patient_user(list_medical_organisations)

                    show_medical_organisations_admin_user(list_medical_organisations)

                    def delete_med_org():
                        id = list_medical_organisations.item(list_medical_organisations.selection(), "text")

                        if (id == ""):
                            messagebox.showinfo(
                                "Error", "Выделите запись для удаления")
                        else:
                            val = (id,)
                            try:
                                with mydb.cursor() as mycursor:
                                    mydb.commit()
                                    mycursor.callproc("delete_medical_organisation", val)

                                    messagebox.showinfo(
                                        "Success", "Медицинская организация удалена")

                                    show_medical_organisations_admin_user(list_medical_organisations)
                            except mysql.connector.Error as err:
                                messagebox.showerror(
                                    "Error", f"Ошибка удаления медицинской организации: {err}")
                                
                    delete_med_org_button = tk.Button(
                        medical_organisations_window, text="Удалить", command=delete_med_org)
                    delete_med_org_button.place(x=550, y=0)
                    set_style_button(delete_med_org_button)


                def manage_med_org():
                    create_med_org_window = tk.Tk()
                    create_med_org_window.title("Управление медицинскими организациями")
                    create_med_org_window.geometry("400x400")
                    create_med_org_window.configure(bg='lightblue')
                    center_window(create_med_org_window, 400, 400)

                    create_med_org_frame = tk.Frame(create_med_org_window)
                    create_med_org_frame.pack(expand=True)

                    create_polyclinic_button = tk.Button(create_med_org_frame, text="Добавить поликлинику", command=create_polyclinic)
                    create_polyclinic_button.pack()
                    set_style_button(create_polyclinic_button)

                    create_hospital_button = tk.Button(create_med_org_frame, text="Добавить больницу", command=create_hospital)
                    create_hospital_button.pack()
                    set_style_button(create_hospital_button)

                    delete_medical_organisation_button = tk.Button(create_med_org_frame, text="Удалить медицинскую организацию", command=delete_medical_organisation)
                    delete_medical_organisation_button.pack()
                    set_style_button(delete_medical_organisation_button)


                    create_med_org_window.mainloop()

                # Создание главного окна
                global admin_window

                admin_window = tk.Tk()
                admin_window.protocol("WM_DELETE_WINDOW", on_closing)
                admin_window.title("Окно администратора")
                admin_window.geometry("800x400")
                admin_window.configure(bg='lightblue')
                center_window(admin_window, 800, 400)

                admin_frame = tk.Frame(admin_window)
                admin_frame.pack(expand=True)

                help_label = tk.Label(admin_frame, text="Перед использованием системы запустите 'Создать роли' и затем 'Создать тестовых пользователей'.")
                help_label.pack()
    
                roles_button = tk.Button(admin_frame, text="Создать роли", command=create_roles)
                roles_button.pack()
                set_style_button(roles_button)

                test_users_button = tk.Button(admin_frame, text="Создать тестовых пользователей", command=create_test_users, state=tk.DISABLED)
                test_users_button.pack()
                set_style_button(test_users_button)

                help_label2 = tk.Label(admin_frame, text="Для добавления и удаления медицинских организаций перейдите в окно 'Управление медицинскими организациями'.")
                help_label2.pack()

                manage_button = tk.Button(admin_frame, text="Управление медицинскими организациями", command=manage_med_org)
                manage_button.pack()
                set_style_button(manage_button)

                exit_button = tk.Button(admin_frame, text="Выйти из системы", command=exit_function)
                set_style_button(exit_button)
                exit_button.pack()

                admin_window.mainloop()

            elif (role == 'patient_role'): 
                mycursor.callproc("get_patient_user_id", (user,))
                for result in mycursor.stored_results():
                    rows = result.fetchall()
                
            elif (role == 'doctor_role'): 
                mycursor.callproc("get_doctor_user_id", (user,))
                for result in mycursor.stored_results():
                    rows = result.fetchall()

            elif (role == 'medical_organisation_role'): 
                mycursor.callproc("get_medical_organisation_user_id", (user,))
                for result in mycursor.stored_results():
                    rows = result.fetchall()
                    
            global user_id
            user_id = rows[0][0]

            if user_id:
                messagebox.showinfo("Info", "Пользователь успешно авторизован")
            else:
                messagebox.showerror("Error", "Неизвестный пользователь. Пожалуйста, попробуйте еще раз.")
                exit_function()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Невозможно авторизовать пользователя: {err}. Пожалуйста, попробуйте еще раз.")
            exit_function()


    def on_closing_root():
        try:
            root.destroy()
        except:
            print("Главное окно закрыто или не существует")
        try:
            mydb.close()
        except:
            print("Не удалось закрыть соединение с базой данных")
        
        print("Завершение работы приложения")
        try:
            exit(0)
        except:
            print("Работа приложения завершена")

    global root
    # главное окно приложения для пользователя Пациент
    if role == "patient_role":
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", on_closing_root)
        root.geometry("600x300")
        root.title("Главное окно")
        root.configure(bg='lightblue')
        center_window(root, 600, 300)

        frame = tk.Frame(root)
        frame.pack(expand=True)
        set_style_frame(frame)

        treatment_registration_button = tk.Button(frame, text="Записаться на прием", command=open_treatment_registration_window_patient_user)
        set_style_button(treatment_registration_button)
        treatment_registration_button.pack()

        polyclinics_button = tk.Button(frame, text="Информация о поликлиниках", command=open_polyclinics_window_patient_user)
        set_style_button(polyclinics_button)
        polyclinics_button.pack()

        hospitals_button = tk.Button(frame, text="Информация о больницах", command=open_hospitals_window_patient_user)
        set_style_button(hospitals_button)
        hospitals_button.pack()

        doctors_button = tk.Button(frame, text="Информация о врачах", command=open_doctors_window_patient_user)
        set_style_button(doctors_button)
        doctors_button.pack()

        exit_button = tk.Button(frame, text="Выйти из системы", command=exit_function)
        set_style_button(exit_button)
        exit_button.pack()


    # главное окно приложения для пользователя Руководитель мед. организации
    elif role == "medical_organisation_role":
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", on_closing_root)
        root.geometry("600x300")
        root.title("Главное окно")
        root.configure(bg='lightblue')
        center_window(root, 600, 300)

        frame = tk.Frame(root)
        frame.pack(expand=True)
        set_style_frame(frame)

        treatment_statistics_button = tk.Button(frame, text="Получить список обслуженных за промежуток времени пациентов", command=open_get_treatment_statistics_window)
        set_style_button(treatment_statistics_button)
        treatment_statistics_button.pack()

        patients_by_disease_button = tk.Button(frame, text="Получить количество пациентов, перенесших заболевание", command=open_get_patients_count_by_disease_window)
        set_style_button(patients_by_disease_button)
        patients_by_disease_button.pack()

        doctors_button = tk.Button(frame, text="Сотрудники", command=open_doctors_window_medicalOrganisationUser)
        set_style_button(doctors_button)
        doctors_button.pack()

        exit_button = tk.Button(frame, text="Выйти из системы", command=exit_function)
        set_style_button(exit_button)
        exit_button.pack()

    # главное окно приложения для пользователя Врач
    elif role == "doctor_role":
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", on_closing_root)
        root.geometry("600x300")
        root.title("Главное окно")
        root.configure(bg='lightblue')
        center_window(root, 600, 300)

        frame = tk.Frame(root)
        frame.pack(expand=True)
        set_style_frame(frame)

        patients_button = tk.Button(frame, text="Пациенты", command=open_patients_window_DoctorUser)
        set_style_button(patients_button)
        patients_button.pack()

        registered_patients_button = tk.Button(frame, text="Список записавшихся пациентов", command=open_get_registered_patients_list_window)
        set_style_button(registered_patients_button)
        registered_patients_button.pack()

        exit_button = tk.Button(frame, text="Выйти из системы", command=exit_function)
        set_style_button(exit_button)
        exit_button.pack()

    root.focus_force()
    root.mainloop()


def exit_function():
    global role, user, password, root, admin_window, mydb
    try:
        admin_window.destroy()
        print('Окно администратора закрыто')
    except:
        print('Окно администратора закрыто или не существует')
    try:
        root.destroy()
        print('Главное окно закрыто')
    except:
        print('Главное окно закрыто или не существует')

    
    role = None
    user = None
    password = None
    try:
        mydb.close()
        print("Соединение с базой данных закрыто")
    except:
        print("Не удалось закрыть соединение с базой данных")

    open_settings_window()


# Создание Tkinter приложения
############################################################################################
def sort_treeview(tree, col, reverse):
    data = [(tree.set(child, col), child) for child in tree.get_children("")]
    data.sort(reverse=reverse)
    for index, (val, child) in enumerate(data):
        tree.move(child, "", index)

        # Переключаем направление сортировки
        tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))

# функция отображения текцщих данных о поликлиниках
def show_polyclinics_patient_user(list_polyclinics):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT name, address, phone, district FROM Polyclinic_PatientUser_View")
        rows = mycursor.fetchall()

        list_polyclinics.delete(*list_polyclinics.get_children())
        list_polyclinics["columns"] = ("name", "address", "phone", "district")
        list_polyclinics.heading("name", text="Медицинская организация")
        list_polyclinics.heading("address", text="Адрес")
        list_polyclinics.heading("phone", text="Телефон")
        list_polyclinics.heading("district", text="Район")

        for row in rows:
            row = list(row)
            if (row[2] == None):
                row[2] = ""
            list_polyclinics.insert("", "end", values=(row[0], row[1], row[2], row[3]))

    # Добавляем возможность сортировки по столбцам
    for col in ("name", "address", "phone", "district"):
        list_polyclinics.heading(col, text=col, command=lambda c=col: sort_treeview(list_polyclinics, c, False))


# функция отображения текущих данных о поликлиниках
def open_polyclinics_window_patient_user():
    polyclinics_window = tk.Toplevel(root)
    polyclinics_window.title("Поликлиники")
    polyclinics_window.geometry("1300x500")
    center_window(polyclinics_window, 1300, 500)

    list_polyclinics = ttk.Treeview(polyclinics_window, columns=("name", "address", "phone", "district"), show="headings")
    list_polyclinics.place(width=1250, height=450)
    help_label = tk.Label(polyclinics_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(polyclinics_window, orient="vertical", command=list_polyclinics.yview)
    vsb.place(x=1250, y=0, height=500)
    list_polyclinics.configure(yscrollcommand=vsb.set)

    show_polyclinics_patient_user(list_polyclinics)


##################################################################################
# функция отображения текущих данных о больницах
def show_hospitals_patient_user(list_hospitals):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT name, address, phone, medical_corps_amount FROM Hospital_PatientUser_View")
        rows = mycursor.fetchall()

        list_hospitals.delete(*list_hospitals.get_children())
        list_hospitals["columns"] = ("name", "address", "phone", "medical_corps_amount")
        list_hospitals.heading("name", text="Медицинская организация")
        list_hospitals.heading("address", text="Адрес")
        list_hospitals.heading("phone", text="Телефон")
        list_hospitals.heading("medical_corps_amount", text="Количество корпусов")

        for row in rows:
            row = list(row)
            if (row[2] == None):
                row[2] = ""
            list_hospitals.insert("", "end", values=(row[0], row[1], row[2], row[3]))

    # Добавляем возможность сортировки по столбцам
    for col in ("name", "address", "phone", "medical_corps_amount"):
        list_hospitals.heading(col, text=col, command=lambda c=col: sort_treeview(list_hospitals, c, False))


# окно для просмотра данных о больницах
def open_hospitals_window_patient_user():
    hospitals_window = tk.Toplevel(root)
    hospitals_window.title("Больницы")
    hospitals_window.geometry("1300x500")
    center_window(hospitals_window, 1300, 500)

    list_hospitals = ttk.Treeview(hospitals_window, columns=("name", "address", "phone", "medical_corps_amount"), show="headings")
    list_hospitals.grid(row=1, column=0, rowspan=3, columnspan=4)
    list_hospitals.place(width=1250, height=450)
    help_label = tk.Label(hospitals_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(hospitals_window, orient="vertical", command=list_hospitals.yview)
    vsb.place(x=1250, y=0, height=500)
    list_hospitals.configure(yscrollcommand=vsb.set)

    show_hospitals_patient_user(list_hospitals)


##########################################################################################
# функция отображения текущих данных о врачебном персонале
def show_doctors(list_doctors):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT DISTINCT doctor_id, last_name, name, patronymic, phone, work_experience FROM Doctor_MedicalOrganisationUser_View WHERE medical_organisation_id = %s", (user_id,))
        rows = mycursor.fetchall()

        list_doctors.delete(*list_doctors.get_children())
        list_doctors["columns"] = ("doctor_id", "last_name", "name", "patronymic", "phone", "work_experience")
        list_doctors.heading("doctor_id", text="Идентификатор")
        list_doctors.heading("last_name", text="Фамилия")
        list_doctors.heading("name", text="Имя")
        list_doctors.heading("patronymic", text="Отчество")
        list_doctors.heading("phone", text="Телефон")
        list_doctors.heading("work_experience", text="Стаж работы")

        for row in rows:
            row = list(row)
            if (row[3] == None):
                row[3] = ""
            if (row[4] == None):
                row[4] = ""
            if (row[5] == None):
                row[5] = ""
            list_doctors.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))

    # Добавляем возможность сортировки по столбцам
    for col in ("doctor_id", "last_name", "name", "patronymic", "phone", "work_experience"):
        list_doctors.heading(col, text=col, command=lambda c=col: sort_treeview(list_doctors, c, False))


# функция отображения текущих данных о врачебном персонале
def show_doctors_patient_user(list_doctors):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT last_name, name, patronymic, medical_organisation_name, address FROM Doctor_PatientUser_View")
        rows = mycursor.fetchall()

        list_doctors.delete(*list_doctors.get_children())
        list_doctors["columns"] = ("last_name", "name", "patronymic", "medical_organisation_name", "address")
        list_doctors.heading("last_name", text="Фамилия")
        list_doctors.heading("name", text="Имя")
        list_doctors.heading("patronymic", text="Отчество")
        list_doctors.heading("medical_organisation_name", text="Медицинская организация")
        list_doctors.heading("address", text="Адрес")

        for row in rows:
            row = list(row)
            if (row[2] == None):
                row[2] = ""
            list_doctors.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

    # Добавляем возможность сортировки по столбцам
    for col in ("last_name", "name", "patronymic", "medical_organisation_name", "address"):
        list_doctors.heading(col, text=col, command=lambda c=col: sort_treeview(list_doctors, c, False))

# окно для просмотра данных о врачах пользователем Пациент
def open_doctors_window_patient_user():
    doctors_window = tk.Toplevel(root)
    doctors_window.title("Врачи")
    doctors_window.geometry("1300x500")
    center_window(doctors_window, 1300, 500)

    list_doctors = ttk.Treeview(doctors_window, columns=("last_name", "name", "patronymic", "medical_organisation_name", "address"), show="headings")
    list_doctors.grid(row=1, column=0, rowspan=3, columnspan=4)
    list_doctors.place(width=1250, height=450)
    help_label = tk.Label(doctors_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(doctors_window, orient="vertical", command=list_doctors.yview)
    vsb.place(x=1250, y=0, height=500)
    list_doctors.configure(yscrollcommand=vsb.set)

    show_doctors_patient_user(list_doctors)

# функция для отображения данных о врачах
def show_doctors_selection_patient_user(list_doctors, medical_organisation_id):
    with mydb.cursor() as mycursor:
        mycursor.callproc("get_doctors_by_medical_organisation", (medical_organisation_id,))
        for result in mycursor.stored_results():
            rows = result.fetchall()

        list_doctors.delete(*list_doctors.get_children())
        list_doctors["columns"] = ("last_name", "name", "patronymic")
        list_doctors.heading("#0", text="ID")
        list_doctors.heading("last_name", text="Фамилия")
        list_doctors.heading("name", text="Имя")
        list_doctors.heading("patronymic", text="Отчество")

        for row in rows:
            row = list(row)
            if (row[3] == None):
                row[3] = ""
            list_doctors.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))

    # Добавляем возможность сортировки по столбцам
    for col in ("last_name", "name", "patronymic"):
        list_doctors.heading(col, text=col, command=lambda c=col: sort_treeview(list_doctors, c, False))


# окно выбора врача
def open_doctor_selection_window(callback, medical_organisation_id):
    doctors_selection_window = tk.Toplevel(root)
    doctors_selection_window.title("Выбрать врача")
    doctors_selection_window.geometry("1300x500")
    center_window(doctors_selection_window, 1300, 500)

    list_doctors = ttk.Treeview(doctors_selection_window, columns=("last_name", "name", "patronymic"), show="headings")
    list_doctors.grid(row=2, column=0, rowspan=3, columnspan=4)
    help_label = tk.Label(doctors_selection_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(doctors_selection_window, orient="vertical", command=list_doctors.yview)
    vsb.grid(row=2, column=4, rowspan=3, sticky='ns')
    list_doctors.configure(yscrollcommand=vsb.set)

    show_doctors_selection_patient_user(list_doctors, medical_organisation_id)

    def select_doctor():
        selected_item = list_doctors.selection()
        doctor_id = list_doctors.item(selected_item, "text")
        callback(doctor_id)
        doctors_selection_window.destroy()

    select_button = tk.Button(doctors_selection_window, text="Выбрать врача", bg='lightblue', command=select_doctor)
    select_button.grid(row=1, column=1)


# функция для отображения данных о медицинских организациях
def show_medical_organisations_selection_patient_user(list_medical_organisations):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT medical_organisation_id, name, address FROM Polyclinic_PatientUser_View")
        rows = mycursor.fetchall()

        list_medical_organisations.delete(*list_medical_organisations.get_children())
        list_medical_organisations["columns"] = ("medical_organisation_name", "address")
        list_medical_organisations.heading("#0", text="ID")
        list_medical_organisations.heading("medical_organisation_name", text="Мед. организация")
        list_medical_organisations.heading("address", text="Адрес")

        for row in rows:
            list_medical_organisations.insert("", "end", text=row[0], values=(row[1], row[2]))

    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT medical_organisation_id, name, address FROM Hospital_PatientUser_View")
        rows = mycursor.fetchall()

        for row in rows:
            list_medical_organisations.insert("", "end", text=row[0], values=(row[1], row[2]))

    # Добавляем возможность сортировки по столбцам
    for col in ("medical_organisation_name", "address"):
        list_medical_organisations.heading(col, text=col, command=lambda c=col: sort_treeview(list_medical_organisations, c, False))


# окно выбора медицинской организации
def open_medical_organisation_selection_window(role, callback):
    medical_organisation_selection_window = tk.Toplevel(root)
    medical_organisation_selection_window.title("Выбрать медицинскую организацию")
    medical_organisation_selection_window.geometry("1300x500")
    center_window(medical_organisation_selection_window, 1300, 500)


    list_medical_organisations = ttk.Treeview(medical_organisation_selection_window, columns=("medical_organisation_name", "address"), show="headings")
    list_medical_organisations.grid(row=2, column=0, rowspan=3, columnspan=6)
    help_label = tk.Label(medical_organisation_selection_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(medical_organisation_selection_window, orient="vertical", command=list_medical_organisations.yview)
    vsb.grid(row=2, column=6, rowspan=3, sticky='ns')
    list_medical_organisations.configure(yscrollcommand=vsb.set)

    if (role == "patient"):
        show_medical_organisations_selection_patient_user(list_medical_organisations)
    elif (role == "doctor"):
        show_medical_organisations_selection_doctor_user(list_medical_organisations)

    def select_medical_organisation():
        selected_item = list_medical_organisations.selection()
        medical_organisation_id = list_medical_organisations.item(selected_item, "text")
        callback(medical_organisation_id)
        medical_organisation_selection_window.destroy()


    select_button = tk.Button(medical_organisation_selection_window, text="Выбрать медицинскую организацию", bg='lightblue', command=select_medical_organisation)
    select_button.grid(row=1, column=1)


# функция для отображения данных о поликлиниках
def show_polyclinic_selection_doctor_user(list_medical_organisations):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT medical_organisation_id, name, address FROM Polyclinic_DoctorUser_View")
        rows = mycursor.fetchall()

        list_medical_organisations.delete(*list_medical_organisations.get_children())
        list_medical_organisations["columns"] = ("polyclinic_name", "address")
        list_medical_organisations.heading("#0", text="ID")
        list_medical_organisations.heading("polyclinic_name", text="Поликлиника")
        list_medical_organisations.heading("address", text="Адрес")

        for row in rows:
            list_medical_organisations.insert("", "end", text=row[0], values=(row[1], row[2]))

    # Добавляем возможность сортировки по столбцам
    for col in ("polyclinic_name", "address"):
        list_medical_organisations.heading(col, text=col, command=lambda c=col: sort_treeview(list_medical_organisations, c, False))


# окно для выбора поликлиники
def open_polyclinic_selection_window(callback):
    polyclinic_selection_window = tk.Toplevel(root)
    polyclinic_selection_window.title("Выбрать поликлинику")
    polyclinic_selection_window.geometry("1300x500")
    center_window(polyclinic_selection_window, 1300, 500)


    list_polyclinic = ttk.Treeview(polyclinic_selection_window, columns=("polyclinic_name", "address"), show="headings")
    list_polyclinic.grid(row=2, column=0, rowspan=3, columnspan=6)
    help_label = tk.Label(polyclinic_selection_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(polyclinic_selection_window, orient="vertical", command=list_polyclinic.yview)
    vsb.grid(row=2, column=6, rowspan=3, sticky='ns')
    list_polyclinic.configure(yscrollcommand=vsb.set)

    show_polyclinic_selection_doctor_user(list_polyclinic)

    def select_polyclinic():
        selected_item = list_polyclinic.selection()
        polyclinic_id = list_polyclinic.item(selected_item, "text")
        callback(polyclinic_id)
        polyclinic_selection_window.destroy()


    select_button = tk.Button(polyclinic_selection_window, text="Выбрать поликлинику", bg='lightblue', command=select_polyclinic)
    select_button.grid(row=1, column=1)


# функция отображения текущих записей пациента на прием
def show_registrations_patient_user(list_treatment_registration):
    with mydb.cursor() as mycursor:
        val = (user_id,)
        mycursor.callproc("get_patients_registrations", val)
        for result in mycursor.stored_results():
            rows = result.fetchall()

        list_treatment_registration.delete(*list_treatment_registration.get_children())

        list_treatment_registration["columns"] = ("last_name", "name", "patronymic", "medical_organisation_name", "address", "date")
        list_treatment_registration.heading("last_name", text="Фамилия")
        list_treatment_registration.heading("name", text="Имя")
        list_treatment_registration.heading("patronymic", text="Отчество")
        list_treatment_registration.heading("medical_organisation_name", text="Медицинская организация")
        list_treatment_registration.heading("address", text="Адрес")
        list_treatment_registration.heading("date", text="Дата")

        for row in rows:
            row = list(row)
            if (row[2] == None):
                row[2] = ""
            list_treatment_registration.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5]))

    # Добавляем возможность сортировки по столбцам
    for col in ("last_name", "name", "patronymic", "medical_organisation_name", "address", "date"):
        list_treatment_registration.heading(col, text=col, command=lambda c=col: sort_treeview(list_treatment_registration, c, False))

# окно для записи на прием
def open_treatment_registration_window_patient_user():
    treatment_registration_window = tk.Toplevel(root)
    treatment_registration_window.title("Запись на приём")
    treatment_registration_window.geometry("1300x500")
    center_window(treatment_registration_window, 1300, 500)

    list_treatment_registration = ttk.Treeview(treatment_registration_window, columns=("last_name", "name", "patronymic", "medical_organisation_name", "address", "date"), show="headings")
    list_treatment_registration.grid(row=5, column=0, rowspan=3, columnspan=4)
    help_label = tk.Label(treatment_registration_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(treatment_registration_window, orient="vertical", command=list_treatment_registration.yview)
    vsb.grid(row=5, column=4, rowspan=3, sticky='ns')
    list_treatment_registration.configure(yscrollcommand=vsb.set)

    show_registrations_patient_user(list_treatment_registration)

    def add_registration():
        doctor_id = doctor_id_entry.get()
        medical_organisation_id = medical_organisation_id_entry.get()
        date = date_entry.get()

        if (doctor_id == "не выбрано" or medical_organisation_id == "не выбрано" or date == "не выбрано"):
            messagebox.showinfo(
                "Error", "Введите обязательные поля: Медицинская организация, Врач, Дата")
        else:
            current_date = datetime.now().date()
            date = datetime.strptime(date, '%Y-%m-%d').date()

            if date < current_date:
                messagebox.showinfo(
                "Error", "Запись на прошедшие даты недоступна")
                return

            sql = "INSERT INTO Treatment_registration_PatientUser_View(patient_id, doctor_id, medical_organisation_id, date) \
                                                                            VALUES (%s, %s, %s, %s)"
            val = (user_id, doctor_id, medical_organisation_id, date)
            try:
                with mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    mydb.commit()
                    messagebox.showinfo(
                        "Success", "Запись сохранена")
                    doctor_id_entry.delete(0, 'end')
                    medical_organisation_id_entry.delete(0, 'end')
                    date_entry.delete(0, 'end')
                    doctor_id_entry['bg'] = "indianred1"
                    doctor_id_entry.insert(0, "не выбрано")
                    medical_organisation_id_entry['bg'] = "indianred1"
                    medical_organisation_id_entry.insert(0, "не выбрано")
                    date_entry.insert(0, "не выбрано")

                    show_registrations_patient_user(list_treatment_registration)

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка сохранения записи: {err}")


    # Создаем поля для ввода данных
    def update_doctor_entry(doctor_id):
        doctor_id_entry.delete(0, 'end')
        if (doctor_id == ""):
            doctor_id_entry['bg'] = "indianred1"
            doctor_id_entry.insert(0, "не выбрано")
        else:
            doctor_id_entry['bg'] = "lightgreen"
            doctor_id_entry.insert(0, doctor_id)

    def update_medical_organisation_entry(medical_organisation_id):
        medical_organisation_id_entry.delete(0, 'end')
        if (medical_organisation_id == ""):
            medical_organisation_id_entry['bg'] = "indianred1"
            medical_organisation_id_entry.insert(0, "не выбрано")
        else:
            medical_organisation_id_entry['bg'] = "lightgreen"
            medical_organisation_id_entry.insert(0, medical_organisation_id)

    help_label = tk.Label(treatment_registration_window, text="Выберите медицинскую организацию, затем врача и дату для записи на прием.")
    help_label.grid(row=0, columnspan=3)
    medical_organisation_id_label = tk.Label(treatment_registration_window, text="Медицинская организация:")
    medical_organisation_id_label.grid(row=1, column=0)
    medical_organisation_select_button = tk.Button(treatment_registration_window, text="Выбрать", bg='lightblue', command=lambda: open_medical_organisation_selection_window("patient", update_medical_organisation_entry))
    medical_organisation_select_button.grid(row=1, column=2)
    medical_organisation_id_entry = tk.Entry(treatment_registration_window, bg='indianred1')
    medical_organisation_id_entry.grid(row=1, column=1)
    medical_organisation_id_entry.insert(0, "не выбрано")

    def check_medical_organisation_selected():
        if (medical_organisation_id_entry.get() == "не выбрано"):
            messagebox.showinfo(
                        "Warning", "Выберите медицинскую организацию")
        else:
            open_doctor_selection_window(update_doctor_entry, medical_organisation_id_entry.get())

    doctor_id_label = tk.Label(treatment_registration_window, text="Врач:")
    doctor_id_label.grid(row=2, column=0)
    doctor_select_button = tk.Button(treatment_registration_window, text="Выбрать", bg='lightblue', command=check_medical_organisation_selected)
    doctor_select_button.grid(row=2, column=2)
    doctor_id_entry = tk.Entry(treatment_registration_window, bg='indianred1')
    doctor_id_entry.grid(row=2, column=1)
    doctor_id_entry.insert(0, "не выбрано")

    date_label = tk.Label(treatment_registration_window, text="Дата (YYYY-MM-DD):")
    date_label.grid(row=3, column=0)
    date_entry = tk.Entry(treatment_registration_window, borderwidth=2)
    date_entry.grid(row=3, column=1)
    date_entry.insert(0, "не выбрано")

    current_registrations_label = tk.Label(treatment_registration_window, text="Текущие записи:")
    current_registrations_label.grid(row=4, column=0)

    add_registration_button = tk.Button(
        treatment_registration_window, text="Записаться", bg='lightblue', command=add_registration)
    add_registration_button.grid(row=1, column=3)


# окно для ввода данных о врачебном персонале
def open_doctors_window_medicalOrganisationUser():
    doctors_window = tk.Toplevel(root)
    doctors_window.title("Сотрудники")
    doctors_window.geometry("1300x500")
    center_window(doctors_window, 1300, 500)

    list_doctors = ttk.Treeview(doctors_window, columns=("last_name", "name", "patronymic", "medical_organisation_name", "address"), show="headings")
    list_doctors.grid(row=10, column=0, rowspan=3, columnspan=4)
    help_label = tk.Label(doctors_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=470)

    vsb = ttk.Scrollbar(doctors_window, orient="vertical", command=list_doctors.yview)
    vsb.grid(row=10, column=4, rowspan=3, sticky='ns')
    list_doctors.configure(yscrollcommand=vsb.set)

    show_doctors(list_doctors)

    def add_doctor():
        last_name = last_name_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        phone = phone_entry.get()
        work_experience = work_experience_entry.get()

        if (last_name == "" or name == ""):
            messagebox.showinfo(
                "Error", "Введите обязательные поля: Фамилия, Имя")
        else:
            if (patronymic == ""):
                patronymic = None
            if (phone == ""):
                phone = None
            if (work_experience == ""):
                work_experience = None

            val = (last_name, name, patronymic, phone, work_experience, user_id)
            try:
                with mydb.cursor() as mycursor:
                    mydb.commit()
                    mycursor.callproc("insert_doctor_to_medical_organisation", val)
                    mycursor.execute("SELECT LAST_INSERT_ID();")
                    new_id = mycursor.fetchone()[0]
                    new_user_name = last_name.replace(" ", "") + '_' + name.replace(" ", "") + '_' + str(new_id)

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка сохранения сотрудника: {err}. Возможно, имя занято. Попробуйте еще раз.")
                
            else:
                mydb.commit()

                messagebox.showinfo(
                    "Success", f"Сотрудник сохранен. Сообщите ему логин: {new_user_name} и пароль: {new_user_name} для входа.")
                last_name_entry.delete(0, 'end')
                name_entry.delete(0, 'end')
                patronymic_entry.delete(0, 'end')
                phone_entry.delete(0, 'end')
                work_experience_entry.delete(0, 'end')

            show_doctors(list_doctors)
            

    def delete_doctor():
        id = list_doctors.item(list_doctors.selection(), "text")

        if (id == ""):
            messagebox.showinfo(
                "Error", "Выделите запись для удаления")
        else:
            val = (user_id, id)
            try:
                with mydb.cursor() as mycursor:
                    mycursor.execute("SELECT * FROM Doctor_MedicalOrganisationUser_View WHERE medical_organisation_id=%s AND doctor_id=%s", val)
                    rows = mycursor.fetchall()
                    if (rows == []):
                        messagebox.showwarning(
                            "Warning", "Врач не относится к вашей организации")
                    else:
                        mydb.commit()
                        mycursor.callproc("delete_doctor_from_medical_organisation", (id, user_id))

                        messagebox.showinfo(
                            "Success", "Сотрудник удален")
                    
                    last_name_entry.delete(0, 'end')
                    name_entry.delete(0, 'end')
                    patronymic_entry.delete(0, 'end')
                    phone_entry.delete(0, 'end')
                    work_experience_entry.delete(0, 'end')

                    show_doctors(list_doctors)
            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка удаления сотрудника: {err}")

    def update_doctor():
        id = list_doctors.item(list_doctors.selection(), "text")
        last_name = last_name_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        phone = phone_entry.get()
        work_experience = work_experience_entry.get()

        if (id == ""):
            messagebox.showinfo(
                "Error", "Выделите запись для обновления")
        elif (last_name == "" and name == "" and patronymic == "" and phone == "" and work_experience == ""):
            messagebox.showinfo(
                "Warning", "Нет данных для изменения. Заполните поля, требующие обновления.")
        else:
            try:
                with mydb.cursor() as mycursor:
                    val = (user_id, id)
                    mycursor.execute("SELECT * FROM Doctor_MedicalOrganisationUser_View WHERE medical_organisation_id=%s AND doctor_id=%s", val)
                    rows = mycursor.fetchall()
                    if (rows == []):
                        messagebox.showwarning(
                            "Warning", "Врач не относится к вашей организации")
                    else:
                        mycursor.execute("SELECT last_name, name, patronymic, phone, work_experience FROM Doctor_MedicalOrganisationUser_View WHERE doctor_id = %s", (id,))
                        old = mycursor.fetchone()
                        if (last_name == ""): last_name = old[0]
                        if (name == ""): name = old[1]
                        if (patronymic == ""): patronymic = old[2]
                        if (phone == ""): phone = old[3]
                        if (work_experience == ""): work_experience = old[4]
                        val = (id, last_name, name, patronymic, phone, work_experience, user_id)
                        
                        mycursor.callproc("update_doctor_in_medical_organisation", val)
                        mydb.commit()
                        messagebox.showinfo(
                            "Success", "Данные сотрудника обновлены")
                    
                    last_name_entry.delete(0, 'end')
                    name_entry.delete(0, 'end')
                    patronymic_entry.delete(0, 'end')
                    phone_entry.delete(0, 'end')
                    work_experience_entry.delete(0, 'end')

                    show_doctors(list_doctors)
            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка обновления данных сотрудника: {err}")
                
    def add_existed_doctor():
        # функция отображения текущих данных о врачебном персонале
        def show_existed_doctors(list_existed_doctors):
            with mydb.cursor() as mycursor:
                mycursor.execute("SELECT DISTINCT doctor_id, last_name, name, patronymic, phone, work_experience \
                                 FROM Doctor_MedicalOrganisationUser_View \
                                 WHERE doctor_id NOT IN ( \
                                    SELECT doctor_id \
                                    FROM Doctor_MedicalOrganisationUser_View \
                                    WHERE medical_organisation_id = %s)", (user_id,))
                rows = mycursor.fetchall()

                list_existed_doctors.delete(*list_existed_doctors.get_children())
                list_existed_doctors["columns"] = ("doctor_id", "last_name", "name", "patronymic", "phone", "work_experience")
                list_existed_doctors.heading("doctor_id", text="Идентификатор")
                list_existed_doctors.heading("last_name", text="Фамилия")
                list_existed_doctors.heading("name", text="Имя")
                list_existed_doctors.heading("patronymic", text="Отчество")
                list_existed_doctors.heading("phone", text="Телефон")
                list_existed_doctors.heading("work_experience", text="Стаж работы")

                for row in rows:
                    row = list(row)
                    if (row[3] == None):
                        row[3] = ""
                    if (row[4] == None):
                        row[4] = ""
                    if (row[5] == None):
                        row[5] = ""
                    list_existed_doctors.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))

            # Добавляем возможность сортировки по столбцам
            for col in ("doctor_id", "last_name", "name", "patronymic", "phone", "work_experience"):
                list_existed_doctors.heading(col, text=col, command=lambda c=col: sort_treeview(list_existed_doctors, c, False))

        def add_existed_doctor_to_current_medical_organisation():
            id = list_existed_doctors.item(list_existed_doctors.selection(), "text")
            if (id == ""):
                messagebox.showinfo(
                    "Info", f"Выделите сотрудника для добавления")
            else:
                val = (id, user_id)
                try:
                    with mydb.cursor() as mycursor:
                        mycursor.callproc("add_existed_doctor", val)
                        mydb.commit()

                        messagebox.showinfo(
                            "Success", "Сотрудник добавлен")
                        
                        show_existed_doctors(list_existed_doctors)
                        show_doctors(list_doctors)

                except mysql.connector.Error as err:
                    messagebox.showerror(
                        "Error", f"Ошибка добавления сотрудника: {err}")


        existed_doctors_window = tk.Toplevel(root)
        existed_doctors_window.title("Сотрудники из других медицинских организаций")
        doctors_window.geometry("1300x500")
        center_window(existed_doctors_window, 1300, 500)

        list_existed_doctors = ttk.Treeview(existed_doctors_window, columns=("last_name", "name", "patronymic", "medical_organisation_name", "address"), show="headings")
        list_existed_doctors.grid(row=9, column=0, rowspan=3, columnspan=4)
        help_label = tk.Label(existed_doctors_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
        help_label.place(x=0, y=450)

        vsb = ttk.Scrollbar(existed_doctors_window, orient="vertical", command=list_existed_doctors.yview)
        vsb.grid(row=9, column=4, rowspan=3, sticky='ns')
        list_existed_doctors.configure(yscrollcommand=vsb.set)

        show_existed_doctors(list_existed_doctors)

        add_existed_doctor_button = tk.Button(
        existed_doctors_window, text="Добавить", bg='lightblue', command=add_existed_doctor_to_current_medical_organisation)
        add_existed_doctor_button.grid(row=4, column=3)

    # Создаем поля для ввода данных
    help_label = tk.Label(doctors_window, text="Для добавления нового сотрудника введите его данные и нажмите 'Сохранить'. Поля Фамилия, Имя обязательны для заполнения.")
    help_label.grid(row=0, columnspan=3)
    help_label.configure(highlightcolor='blue')
    help_label = tk.Label(doctors_window, text="Для обновления данных сотрудника выделите запись для изменения, заполните необходимые поля и нажмите 'Обновить'.")
    help_label.grid(row=1, columnspan=3)
    help_label = tk.Label(doctors_window, text="Для удаления данных сотрудника выделите запись и нажмите 'Удалить'.")
    help_label.grid(row=2, columnspan=3)
    help_label = tk.Label(doctors_window, text="Для добавления сотрудника, который уже зарегистрирован в другой медицинской организации, перейдите в окно 'Добавить сотрудника из другой медицинской организации'.")
    help_label.grid(row=3, columnspan=3)

    add_existed_doctor_button = tk.Button(
        doctors_window, text="Добавить сотрудника из другой медицинской организации", bg='lightblue', command=add_existed_doctor)
    add_existed_doctor_button.grid(row=4, column=1)

    last_name_label = tk.Label(doctors_window, text="Фамилия:")
    last_name_label.grid(row=5, column=1)
    last_name_entry = tk.Entry(doctors_window)
    last_name_entry.grid(row=5, column=2)

    name_label = tk.Label(doctors_window, text="Имя:")
    name_label.grid(row=6, column=1)
    name_entry = tk.Entry(doctors_window)
    name_entry.grid(row=6, column=2)

    patronymic_label = tk.Label(doctors_window, text="Отчество:")
    patronymic_label.grid(row=7, column=1)
    patronymic_entry = tk.Entry(doctors_window)
    patronymic_entry.grid(row=7, column=2)

    phone_label = tk.Label(doctors_window, text="Номер телефона:")
    phone_label.grid(row=8, column=1)
    phone_entry = tk.Entry(doctors_window)
    phone_entry.grid(row=8, column=2)

    work_experience_label = tk.Label(
        doctors_window, text="Стаж работы:")
    work_experience_label.grid(row=9, column=1)
    work_experience_entry = tk.Entry(doctors_window)
    work_experience_entry.grid(row=9, column=2)

    add_doctor_button = tk.Button(
        doctors_window, text="Сохранить", bg='lightblue', command=add_doctor)
    add_doctor_button.grid(row=5, column=3)

    update_doctor_button = tk.Button(
        doctors_window, text="Обновить", bg='lightblue', command=update_doctor)
    update_doctor_button.grid(row=6, column=3)

    delete_doctor_button = tk.Button(
        doctors_window, text="Удалить", bg='lightblue', command=delete_doctor)
    delete_doctor_button.grid(row=7, column=3)


# окно для получения списка обслуженных за период пациентов
def open_get_treatment_statistics_window():
    get_treatment_statistics_window = tk.Toplevel(root)
    get_treatment_statistics_window.title(
        "Список обслуженных за промежуток времени пациентов")
    get_treatment_statistics_window.geometry("1300x500")
    center_window(get_treatment_statistics_window, 1300, 500)

    list_treatment_statistics = ttk.Treeview(get_treatment_statistics_window, columns=("patient", "doctor", "disease", "date"), show="headings", selectmode='browse')
    list_treatment_statistics.grid(row=3, column=0, rowspan=3, columnspan=4)
    help_label = tk.Label(get_treatment_statistics_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)

    vsb = ttk.Scrollbar(get_treatment_statistics_window, orient="vertical", command=list_treatment_statistics.yview)
    vsb.grid(row=3, column=4, rowspan=3, sticky='ns')
    list_treatment_statistics.configure(yscrollcommand=vsb.set)

    def get_treatment_statistics():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        if (start_date == "" or end_date == ""):
            messagebox.showinfo(
                "Error", "Введите обязательные поля: Начальная дата, Конечная дата")
        else:
            try:
                with mydb.cursor() as mycursor:
                    val = (user_id,
                           start_date, end_date)
                    mycursor.callproc("get_treatment_statistics", val)

                    for result in mycursor.stored_results():
                        rows = result.fetchall()

                    list_treatment_statistics.delete(*list_treatment_statistics.get_children())
                    list_treatment_statistics["columns"] = ("patient", "doctor", "disease", "date")
                    list_treatment_statistics.heading("patient", text="Пациент")
                    list_treatment_statistics.heading("doctor", text="Врач")
                    list_treatment_statistics.heading("disease", text="Болезнь")
                    list_treatment_statistics.heading("date", text="Дата")

                    for row in rows:
                        row = list(row)
                        if (row[3] == None):
                            row[3] = ""
                        if (row[6] == None):
                            row[6] = ""
                        list_treatment_statistics.insert("", "end", text=row[0], values=(row[1] + " " + row[2] + " " + row[3], 
                                                                            row[4] + " " + row[5] + " " + row[6], 
                                                                            row[7], row[8]))

                    # Добавляем возможность сортировки по столбцам
                    for col in ("patient", "doctor", "disease", "date"):
                        list_treatment_statistics.heading(col, text=col, command=lambda c=col: sort_treeview(list_treatment_statistics, c, False))

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка выполнения процедуры: {err}")
                
    def get_treatment_description():
        id = list_treatment_statistics.item(list_treatment_statistics.selection(), "text")
        if (id == ""):
            messagebox.showinfo(
                "Error", "Запросите статистику и выделите запись, для которой хотите получить подробное описание")
        else:
            treatment_description_window = tk.Toplevel(get_treatment_statistics_window)
            treatment_description_window.title(
                "Подробное описание лечения")
            treatment_description_window.geometry("1300x500")
            center_window(treatment_description_window, 1300, 500)

            description_field = tk.Text(treatment_description_window, height=20, width=150)
            description_field.pack(side='left')

            scroll = ttk.Scrollbar(treatment_description_window, orient="vertical", command=description_field.yview)
            scroll.pack(side='left', fill='y')
            description_field.configure(yscrollcommand=vsb.set)
            try:
                with mydb.cursor() as mycursor:
                    val = (id,)
                    mycursor.callproc("get_treatment_description", val)

                    for result in mycursor.stored_results():
                        rows = result.fetchall()

                    if (rows[0] == (None,)):
                        description_field.insert(1.0, "Нет подробного описания")
                    else:
                        for row in rows:
                            description_field.insert(1.0, row)

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка выполнения процедуры: {err}")


    # Создаем поля для ввода данных
    help_label = tk.Label(get_treatment_statistics_window, text="Введите начальную и конечную дату периода, за который хотите получить отчёт. После этого вы сможете выделить запись для получения подробного описания.")
    help_label.grid(row=0, columnspan=2)
    start_date_label = tk.Label(
        get_treatment_statistics_window, text="Начальная дата (YYYY-MM-DD):")
    start_date_label.grid(row=1, column=0)
    start_date_entry = tk.Entry(get_treatment_statistics_window)
    start_date_entry.grid(row=1, column=1)

    end_date_label = tk.Label(
        get_treatment_statistics_window, text="Конечная дата (YYYY-MM-DD):")
    end_date_label.grid(row=2, column=0)
    end_date_entry = tk.Entry(get_treatment_statistics_window)
    end_date_entry.grid(row=2, column=1)

    get_treatment_statistics_button = tk.Button(
        get_treatment_statistics_window, text="Найти", bg='lightblue', command=get_treatment_statistics)
    get_treatment_statistics_button.grid(row=1, column=2)

    get_treatment_statistics_button = tk.Button(
        get_treatment_statistics_window, text="Получить подробное описание", bg='lightblue', command=get_treatment_description)
    get_treatment_statistics_button.grid(row=2, column=2)


# функция для отображения данных о медицинских организациях
def show_medical_organisations_selection_doctor_user(list_medical_organisations):
    with mydb.cursor() as mycursor:
        mycursor.callproc("get_medical_organisations_by_doctor", (user_id,))
        for result in mycursor.stored_results():
            rows = result.fetchall()

        list_medical_organisations.delete(*list_medical_organisations.get_children())
        list_medical_organisations["columns"] = ("medical_organisation_name", "address")
        list_medical_organisations.heading("#0", text="ID")
        list_medical_organisations.heading("medical_organisation_name", text="Мед. организация")
        list_medical_organisations.heading("address", text="Адрес")

        for row in rows:
            list_medical_organisations.insert("", "end", text=row[0], values=(row[1], row[2]))

    # Добавляем возможность сортировки по столбцам
    for col in ("medical_organisation_name", "address"):
        list_medical_organisations.heading(col, text=col, command=lambda c=col: sort_treeview(list_medical_organisations, c, False))


# окно для вызова процедуры для получения списка записавшихся пациентов
def open_get_registered_patients_list_window():
    get_registered_patients_list_window = tk.Toplevel(root)
    get_registered_patients_list_window.title(
        "Получить список записавшихся пациентов")
    get_registered_patients_list_window.geometry("1300x500")
    center_window(get_registered_patients_list_window, 1300, 500)

    list_registered_patients = ttk.Treeview(get_registered_patients_list_window, columns=("last_name", "name", "patronymic"), show="headings")
    list_registered_patients.grid(row=3, column=0, rowspan=3, columnspan=6)
    help_label = tk.Label(get_registered_patients_list_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=450)
    
    vsb = ttk.Scrollbar(get_registered_patients_list_window, orient="vertical", command=list_registered_patients.yview)
    vsb.grid(row=3, column=6, rowspan=3, sticky='ns')
    list_registered_patients.configure(yscrollcommand=vsb.set)

    def show_registered_patients_list():
        current_medical_organisation_id = medical_organisation_id_entry.get()

        if (current_medical_organisation_id == "не выбрано"):
            messagebox.showinfo(
                "Error", "Введите обязательные поля: Идентификатор медицинской организации")
        else:
            try:
                with mydb.cursor() as mycursor:
                    val = (user_id, current_medical_organisation_id)
                    mycursor.callproc("get_registered_patients_list", val)

                    for result in mycursor.stored_results():
                        rows = result.fetchall()

                    list_registered_patients.delete(*list_registered_patients.get_children())
                    list_registered_patients["columns"] = ("patient_id", "last_name", "name", "patronymic")
                    list_registered_patients.heading("patient_id", text="Идентификатор")
                    list_registered_patients.heading("last_name", text="Фамилия")
                    list_registered_patients.heading("name", text="Имя")
                    list_registered_patients.heading("patronymic", text="Отчество")

                    for row in rows:
                        row = list(row)
                        if (row[3] == None):
                            row[3] = ""
                        list_registered_patients.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3]))

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка выполнения процедуры: {err}")

    # Создаем поля для ввода данных
    def update_medical_organisation_entry(medical_organisation_id):
        medical_organisation_id_entry.delete(0, 'end')
        if (medical_organisation_id == ""):
            medical_organisation_id_entry['bg'] = "indianred1"
            medical_organisation_id_entry.insert(0, "не выбрано")
        else:
            medical_organisation_id_entry['bg'] = "lightgreen"
            medical_organisation_id_entry.insert(0, medical_organisation_id)


    # окно для ввода результатов лечения пациента
    def add_treatment_window():
        if (list_registered_patients.item(list_registered_patients.selection(), "text") == "" or medical_organisation_id_entry.get() == "не выбрано"):
            messagebox.showinfo(
                    "Error", "Выберите пациента и медицинскую организацию")
            return
        treatment_window = tk.Toplevel(root)
        treatment_window.title("Добавить запись о лечении")
        treatment_window.geometry("1300x500")
        center_window(treatment_window, 1300, 500)

        def save_treatment():
            disease = disease_entry.get()
            description = description_entry.get("1.0", "end-1c")

            if (disease == ""):
                messagebox.showinfo(
                    "Error", "Введите обязательные поля: Заболевание")
            else:
                if (description == ""): description = None
                val = (list_registered_patients.item(list_registered_patients.selection(), "text"), 
                       user_id, medical_organisation_id_entry.get(), disease, description)
                try:
                    with mydb.cursor() as mycursor:
                        mycursor.callproc("add_treatment", val)
                        mydb.commit()

                        messagebox.showinfo(
                            "Success", "Запись сохранена")
                        
                        show_registered_patients_list()

                        disease_entry.delete(0, 'end')
                        description_entry.delete("1.0", "end")
                        treatment_window.destroy()
                        medical_organisation_id_entry.delete(0, 'end')
                        medical_organisation_id_entry['bg'] = "indianred1"
                        medical_organisation_id_entry.insert(0, "не выбрано")

                except mysql.connector.Error as err:
                    messagebox.showerror(
                        "Error", f"Ошибка сохранения: {err}")

        help_label = tk.Label(treatment_window, text="Поля, помеченные *, обязательны для заполнения.")
        help_label.grid(row=0, columnspan=2)
        disease_label = tk.Label(treatment_window, text="*Заболевание*:")
        disease_label.grid(row=1, column=0)
        disease_entry = tk.Entry(treatment_window)
        disease_entry.grid(row=1, column=1)

        description_label = tk.Label(treatment_window, text="Описание:")
        description_label.grid(row=2, column=0)
        description_entry = tk.Text(treatment_window, height=20, width=140)
        description_entry.grid(row=2, column=1)

        select_button = tk.Button(treatment_window, text="Сохранить запись", bg='lightblue', command=save_treatment)
        select_button.grid(row=3, column=1)

        treatment_window.mainloop()


    help_label = tk.Label(get_registered_patients_list_window, text="Выберите медицинскую организацию, для которой хотите получить список пациентов.")
    help_label.grid(row=0, columnspan=6)
    medical_organisation_id_label = tk.Label(get_registered_patients_list_window, text="Медицинская организация:")
    medical_organisation_id_label.grid(row=1, column=1)
    medical_organisation_select_button = tk.Button(get_registered_patients_list_window, text="Выбрать", bg='lightblue', command=lambda: open_medical_organisation_selection_window("doctor", update_medical_organisation_entry))
    medical_organisation_select_button.grid(row=1, column=2)
    medical_organisation_id_entry = tk.Entry(get_registered_patients_list_window, bg='indianred1')
    medical_organisation_id_entry.grid(row=1, column=3)
    medical_organisation_id_entry.insert(0, "не выбрано")

    get_registered_patients_button = tk.Button(
        get_registered_patients_list_window, text="Выполнить", bg='lightblue', command=show_registered_patients_list)
    get_registered_patients_button.grid(row=1, column=4)

    get_treatment_statistics_button = tk.Button(
        get_registered_patients_list_window, text="Принять пациента", bg='lightblue', 
        command=lambda: add_treatment_window())
    get_treatment_statistics_button.grid(row=1, column=6)


# окно для получения количества пациентов, перенесших заболевание
def open_get_patients_count_by_disease_window():
    get_patients_count_by_disease_window = tk.Toplevel(root)
    get_patients_count_by_disease_window.title(
        "Количество пациентов, перенесших заболевание")
    get_patients_count_by_disease_window.geometry("1300x500")
    center_window(get_patients_count_by_disease_window, 1300, 500)

    list_patients_count = ttk.Treeview(get_patients_count_by_disease_window, columns=("count"), show="headings")
    list_patients_count.grid(row=2, column=0, rowspan=3, columnspan=4)

    def get_patients_count_by_disease_list():
        disease = disease_entry.get()

        if (disease == ""):
            messagebox.showinfo(
                "Error", "Введите обязательные поля: Название заболевания")
        else:
            try:
                with mydb.cursor() as mycursor:
                    sql = "SELECT get_patients_count_by_disease(%s, %s);"
                    val = (disease, user_id)
                    mycursor.execute(sql, val)
                    rows = mycursor.fetchall()

                    list_patients_count.delete(*list_patients_count.get_children())
                    list_patients_count["columns"] = ("count")
                    list_patients_count.heading("count", text="Количество пациентов")

                    for row in rows:
                        list_patients_count.insert("", "end", values=(row[0]))

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка выполнения функции: {err}")

    # Создаем поля для ввода данных
    help_label = tk.Label(get_patients_count_by_disease_window, text="Введите название заболевание, для которого хотите получить статистику.")
    help_label.grid(row=0, columnspan=3)
    disease_label = tk.Label(
        get_patients_count_by_disease_window, text="Название заболевания:")
    disease_label.grid(row=1, column=1)
    disease_entry = tk.Entry(get_patients_count_by_disease_window)
    disease_entry.grid(row=1, column=2)

    get_treatment_statistics_button = tk.Button(
        get_patients_count_by_disease_window, text="Найти", bg='lightblue', command=get_patients_count_by_disease_list)
    get_treatment_statistics_button.grid(row=1, column=3)


##########################################################################################
# функция отображения текущих данных о пациентах
def show_patients(list_patients):
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT * FROM Patient_DoctorUser_View")
        rows = mycursor.fetchall()

        list_patients.delete(*list_patients.get_children())
        list_patients["columns"] = ("patient_id", "name", "birthday", "phone", "address", "policy_number", "polyclinic_id")
        list_patients.heading("patient_id", text="Идентификатор")
        list_patients.heading("name", text="ФИО")
        list_patients.heading("birthday", text="Дата рождения")
        list_patients.heading("phone", text="Телефон")
        list_patients.heading("address", text="Адрес")
        list_patients.heading("policy_number", text="Медицинский полис")
        list_patients.heading("polyclinic_id", text="Поликлиника")

        for row in rows:
            row = list(row)
            if (row[3] == None):
                row[3] = ""
            if (row[5] == None):
                row[5] = ""
            if (row[7] == None):
                row[7] = ""
            if (row[8] == None):
                row[8] = ""
            list_patients.insert("", "end", text=row[0], values=(row[0], row[1] + " " + row[2] + " " + row[3], row[4], row[5], row[6], row[7], row[8]))

    # Добавляем возможность сортировки по столбцам
    for col in ("patient_id", "name", "birthday", "phone", "address", "policy_number", "polyclinic_id"):
        list_patients.heading(col, text=col, command=lambda c=col: sort_treeview(list_patients, c, False))

# окно для ввода данных о пациентах
def open_patients_window_DoctorUser():
    patients_window = tk.Toplevel(root)
    patients_window.title("Пациенты")
    patients_window.geometry("1500x500")
    center_window(patients_window, 1500, 500)

    list_patients = ttk.Treeview(patients_window, columns=("last_name", "name", "patronymic", "medical_organisation_name", "address"), show="headings")
    list_patients.grid(row=12, column=0, rowspan=3, columnspan=4)
    help_label = tk.Label(patients_window, text="Нажмите на заголовок столбца для сортировки. Повторное нажатие сменит направление сортировки.")
    help_label.place(x=0, y=475)

    vsb = ttk.Scrollbar(patients_window, orient="vertical", command=list_patients.yview)
    vsb.grid(row=12, column=4, rowspan=3, sticky='ns')
    list_patients.configure(yscrollcommand=vsb.set)

    show_patients(list_patients)

    def add_patient():
        last_name = last_name_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        birthday = birthday_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        policy_number = policy_number_entry.get()
        polyclinic_id = polyclinic_id_entry.get()

        if (last_name == "" or name == "" or birthday == "" or address == ""):
            messagebox.showinfo(
                "Error", "Введите обязательные поля: Фамилия, Имя, Дата рождения, Адрес")
        else:
            if (patronymic == ""):
                patronymic = None
            if (phone == ""):
                phone = None
            if (policy_number == ""):
                policy_number = None
            if (polyclinic_id == ""):
                polyclinic_id = None

            val = (last_name, name, patronymic, birthday,
                   phone, address, policy_number, polyclinic_id)
            try:
                with mydb.cursor() as mycursor:
                    mydb.commit()
                    mycursor.callproc("add_patient_to_polyclinic", val)

                    mycursor.execute("SELECT LAST_INSERT_ID();")
                    new_id = mycursor.fetchone()[0]
                    new_user_name = last_name.replace(" ", "") + '_' + name.replace(" ", "") + '_' + str(new_id)

                    messagebox.showinfo(
                        "Success", f"Пациент сохранен. Сообщите ему логин: {new_user_name} и пароль: {new_user_name} для входа.")
                    last_name_entry.delete(0, 'end')
                    name_entry.delete(0, 'end')
                    patronymic_entry.delete(0, 'end')
                    birthday_entry.delete(0, 'end')
                    phone_entry.delete(0, 'end')
                    address_entry.delete(0, 'end')
                    policy_number_entry.delete(0, 'end')
                    polyclinic_id_entry.delete(0, 'end')
                    polyclinic_id_entry.insert(0, "не выбрано")

                    show_patients(list_patients)

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка сохранения пациента: {err}. Возможно, имя занято. Попробуйте еще раз.")

    def delete_patient():
        id = list_patients.item(list_patients.selection(), "text")

        if (id == ""):
            messagebox.showinfo(
                "Error", "Введите идентификатор записи для удаления")
        else:
            try:
                with mydb.cursor() as mycursor:
                    print(id)
                    mydb.commit()
                    mycursor.callproc("delete_patient", (id,))
                    mydb.commit()

                    messagebox.showinfo(
                        "Success", "Пациент удален")
                    last_name_entry.delete(0, 'end')
                    name_entry.delete(0, 'end')
                    patronymic_entry.delete(0, 'end')
                    birthday_entry.delete(0, 'end')
                    phone_entry.delete(0, 'end')
                    address_entry.delete(0, 'end')
                    policy_number_entry.delete(0, 'end')
                    polyclinic_id_entry.delete(0, 'end')
                    polyclinic_id_entry.insert(0, "не выбрано")

                    show_patients(list_patients)
            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка удаления пациента: {err}")

    def update_patient():
        id = list_patients.item(list_patients.selection(), "text")
        last_name = last_name_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        birthday = birthday_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        policy_number = policy_number_entry.get()
        polyclinic_id = polyclinic_id_entry.get()

        if (id == ""):
            messagebox.showinfo(
                "Error", "Введите идентификатор записи для обновления")
        elif (last_name == "" and name == "" and patronymic == "" and birthday == "" and phone == "" and address == "" and policy_number == "" and (polyclinic_id == "" or polyclinic_id == "не выбрано")):
            messagebox.showinfo(
                "Warning", "Нет данных для изменения. Заполните поля, требующие обновления.")
        else:
            try:
                with mydb.cursor() as mycursor:
                    val = (id,)
                    mycursor.execute("SELECT * FROM Patient_DoctorUser_View WHERE patient_id=%s", val)
                    rows = mycursor.fetchall()
                    if (rows == []):
                        messagebox.showwarning(
                            "Warning", "Неправильный идентификатор")
                    else:
                        mycursor.execute("SELECT last_name, name, patronymic, birthday, phone, address, policy_number FROM Patient_DoctorUser_View WHERE patient_id = %s", (id,))
                        old = mycursor.fetchone()
                        if (last_name == ""): last_name = old[0]
                        if (name == ""): name = old[1]
                        if (patronymic == ""): patronymic = old[2]
                        if (birthday == ""): birthday = old[3]
                        if (phone == ""): phone = old[4]
                        if (address == ""): address = old[5]
                        if (policy_number == ""): policy_number = old[6]
                        if (polyclinic_id == ""): polyclinic_id = -1
                        if (polyclinic_id == "не выбрано"): polyclinic_id = -1
                        val = (id, last_name, name, patronymic, birthday, phone, address, policy_number, polyclinic_id)
                        
                        mycursor.callproc("update_patient_in_polyclinic", val)
                        mydb.commit()

                        messagebox.showinfo(
                            "Success", "Пациент обновлен")
                    
                    last_name_entry.delete(0, 'end')
                    name_entry.delete(0, 'end')
                    patronymic_entry.delete(0, 'end')
                    birthday_entry.delete(0, 'end')
                    phone_entry.delete(0, 'end')
                    address_entry.delete(0, 'end')
                    policy_number_entry.delete(0, 'end')
                    polyclinic_id_entry.delete(0, 'end')
                    polyclinic_id_entry.insert(0, "не выбрано")

                    show_patients(list_patients)
            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Ошибка обновления пациента: {err}")


    # Создаем поля для ввода данных
    def update_medical_organisation_entry(medical_organisation_id):
        polyclinic_id_entry.delete(0, 'end')
        if (medical_organisation_id == ""):
            polyclinic_id_entry.insert(0, "не выбрано")
        else:
            polyclinic_id_entry.insert(0, medical_organisation_id)


    help_label = tk.Label(patients_window, text="Для добавления нового пациента введите его данные и нажмите 'Сохранить'. Поля Фамилия, Имя, Дата рождения, Адрес, Поликлиника обязательны для заполнения.")
    help_label.grid(row=0, columnspan=3)
    help_label.configure(highlightcolor='blue')
    help_label = tk.Label(patients_window, text="Для обновления данных пациента выделите запись для изменения, заполните необходимые поля и нажмите 'Обновить'.")
    help_label.grid(row=1, columnspan=3)
    help_label = tk.Label(patients_window, text="Для удаления данных пациента выделите запись и нажмите 'Удалить'.")
    help_label.grid(row=2, columnspan=3)

    last_name_label = tk.Label(patients_window, text="Фамилия:")
    last_name_label.grid(row=3, column=1)
    last_name_entry = tk.Entry(patients_window)
    last_name_entry.grid(row=3, column=2)

    name_label = tk.Label(patients_window, text="Имя:")
    name_label.grid(row=4, column=1)
    name_entry = tk.Entry(patients_window)
    name_entry.grid(row=4, column=2)

    patronymic_label = tk.Label(patients_window, text="Отчество:")
    patronymic_label.grid(row=5, column=1)
    patronymic_entry = tk.Entry(patients_window)
    patronymic_entry.grid(row=5, column=2)

    birthday_label = tk.Label(patients_window, text="Дата рождения (YYYY-MM-DD):")
    birthday_label.grid(row=6, column=1)
    birthday_entry = tk.Entry(patients_window)
    birthday_entry.grid(row=6, column=2)

    phone_label = tk.Label(patients_window, text="Номер телефона:")
    phone_label.grid(row=7, column=1)
    phone_entry = tk.Entry(patients_window)
    phone_entry.grid(row=7, column=2)

    address_label = tk.Label(patients_window, text="Адрес:")
    address_label.grid(row=8, column=1)
    address_entry = tk.Entry(patients_window)
    address_entry.grid(row=8, column=2)

    policy_number_label = tk.Label(
        patients_window, text="Номер медицинского полиса:")
    policy_number_label.grid(row=9, column=1)
    policy_number_entry = tk.Entry(patients_window)
    policy_number_entry.grid(row=9, column=2)

    polyclinic_id_label = tk.Label(patients_window, text="Поликлиника:")
    polyclinic_id_label.grid(row=10, column=1)
    polyclinic_select_button = tk.Button(patients_window, text="Выбрать", bg='lightblue', command=lambda: open_polyclinic_selection_window(update_medical_organisation_entry))
    polyclinic_select_button.grid(row=10, column=3)
    polyclinic_id_entry = tk.Entry(patients_window)
    polyclinic_id_entry.grid(row=10, column=2)
    polyclinic_id_entry.insert(0, "не выбрано")

    add_doctor_button = tk.Button(
        patients_window, text="Сохранить", bg='lightblue', command=add_patient)
    add_doctor_button.grid(row=3, column=3)

    update_doctor_button = tk.Button(
        patients_window, text="Обновить", bg='lightblue', command=update_patient)
    update_doctor_button.grid(row=4, column=3)

    delete_doctor_button = tk.Button(
        patients_window, text="Удалить", bg='lightblue', command=delete_patient)
    delete_doctor_button.grid(row=5, column=3)


open_settings_window()