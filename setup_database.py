import getpass

import mysql.connector


# Ask for the MySQL root password only during database setup.
root_password = getpass.getpass("Enter MySQL root password: ")


# Connect without selecting a database because it may not exist yet.
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=root_password
)

cursor = connection.cursor()


# Create the database and the application user.
cursor.execute(
    "CREATE DATABASE IF NOT EXISTS leave_tracker_db"
)

cursor.execute(
    "CREATE USER IF NOT EXISTS "
    "'leave_user'@'localhost' "
    "IDENTIFIED BY 'leave_password'"
)

cursor.execute(
    "CREATE USER IF NOT EXISTS "
    "'leave_user'@'127.0.0.1' "
    "IDENTIFIED BY 'leave_password'"
)

cursor.execute(
    "GRANT ALL PRIVILEGES ON leave_tracker_db.* "
    "TO 'leave_user'@'localhost'"
)

cursor.execute(
    "GRANT ALL PRIVILEGES ON leave_tracker_db.* "
    "TO 'leave_user'@'127.0.0.1'"
)

cursor.execute("FLUSH PRIVILEGES")

cursor.execute("USE leave_tracker_db")


# Module 1: Employees.
# Three main fields: name, email, department.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS employees (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        department VARCHAR(100) NOT NULL
    )
    """
)


# Module 2: Leave types.
# Three main fields: name, days_allowed, description.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS leave_types (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL UNIQUE,
        days_allowed INT NOT NULL,
        description VARCHAR(255) NOT NULL
    )
    """
)


# Module 3: Leave requests.
# Three main fields: employee_id, leave_type_id, leave_date.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INT PRIMARY KEY AUTO_INCREMENT,
        employee_id INT NOT NULL,
        leave_type_id INT NOT NULL,
        leave_date DATE NOT NULL,
        FOREIGN KEY (employee_id)
            REFERENCES employees(id)
            ON DELETE CASCADE,
        FOREIGN KEY (leave_type_id)
            REFERENCES leave_types(id)
            ON DELETE CASCADE
    )
    """
)


# Insert starter rows so the project can be tested immediately.
cursor.execute(
    """
    INSERT IGNORE INTO employees
    (name, email, department)
    VALUES
    ('Demo Employee', 'demo@example.com', 'IT')
    """
)

cursor.execute(
    """
    INSERT IGNORE INTO leave_types
    (name, days_allowed, description)
    VALUES
    ('Annual Leave', 20, 'Regular paid leave')
    """
)


# Save all changes.
connection.commit()

cursor.close()
connection.close()


print("Database setup completed successfully.")
print("Database: leave_tracker_db")
print("User: leave_user")