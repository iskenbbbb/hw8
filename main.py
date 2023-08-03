import sqlite3

# Шаг 1
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        area REAL DEFAULT 0,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
''')

cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        city_id INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
''')

conn.commit()

# Шаг 2
cursor.executemany('INSERT INTO countries (title) VALUES (?)', [('Kyrgyzstan',), ('Germany',), ('China',)])
conn.commit()

# Шаг 3
cursor.executemany('INSERT INTO cities (title, country_id) VALUES (?, ?)', [('Bishkek', 1), ('Osh', 1), ('Berlin', 2), ('Beijing', 3), ('Moscow', 3), ('New York', 0), ('Tokyo', 0)])
conn.commit()

# Шаг 4 (города добавлены в шаге 3)

# Шаг 5
cursor.executemany('INSERT INTO employees (first_name, last_name, city_id) VALUES (?, ?, ?)', [
    ('John', 'Doe', 1),
    ('Jane', 'Smith', 1),
    ('Michael', 'Johnson', 2),
    ('Emma', 'Lee', 3),
    ('Robert', 'Kim', 4),
    ('Olivia', 'Chen', 5),
    ('William', 'Wang', 4),
    ('Sophia', 'Li', 5),
    ('Alexander', 'Garcia', 6),
    ('Ava', 'Martinez', 0),
    ('Ethan', 'Nguyen', 0),
    ('Mia', 'Rodriguez', 3),
    ('James', 'Brown', 4),
    ('Amelia', 'Miller', 1),
    ('Charlotte', 'Davis', 2),
])
conn.commit()

conn.close()



def print_cities():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()

    print(
        "Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
    for city in cities:
        print(f"{city[0]}. {city[1]}")

    conn.close()


def print_employees_by_city(city_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT e.first_name, e.last_name, co.title, ci.title, ci.area
        FROM employees e
        JOIN cities ci ON e.city_id = ci.id
        JOIN countries co ON ci.country_id = co.id
        WHERE e.city_id = ?
    ''', (city_id,))

    employees = cursor.fetchall()

    if not employees:
        print("Нет сотрудников для данного города.")
    else:
        print("Имя\t\tФамилия\t\tСтрана\t\tГород\t\tПлощадь города")
        for employee in employees:
            print(f"{employee[0]}\t\t{employee[1]}\t\t{employee[2]}\t\t{employee[3]}\t\t{employee[4]}")

    conn.close()


if __name__ == "__main__":
    while True:
        print_cities()
        city_id = int(input("Введите id города: "))

        if city_id == 0:
            print("Программа завершена.")
            break

        print_employees_by_city(city_id)
