import sqlite3

# Connect to SQLite
connection = sqlite3.connect("Amity.db")
cursor = connection.cursor()

# Creating tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Semester (
    Semester_id INT PRIMARY KEY,
    Semester_name VARCHAR(50) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    Student_id VARCHAR(20) PRIMARY KEY,
    First_name VARCHAR(50),
    Last_name VARCHAR(50),
    Semester_id INT,
    FOREIGN KEY (Semester_id) REFERENCES Semester(Semester_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Subject (
    Subject_id INT PRIMARY KEY,
    Subject_name VARCHAR(100)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments (
    Enrollment_id VARCHAR(20) PRIMARY KEY,
    Student_id VARCHAR(20),
    Subject_id INT,
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id),
    FOREIGN KEY (Subject_id) REFERENCES Subject(Subject_id)
);
""")

# Inserting data into Semester
sql_query1 = """INSERT INTO Semester (Semester_id, Semester_name) VALUES (?, ?)"""
values_1 = [
    (1, 'Sem1'),
    (2, 'Sem2'),
    (3, 'Sem3')
]

# Inserting data into Student
sql_query2 = """INSERT INTO Student (Student_id, First_name, Last_name, Semester_id) VALUES (?, ?, ?, ?)"""
values_2 = [
    ('A01', 'Sameer', 'Jamuar', 1),
    ('A02', 'Hariom', 'Sharnam', 1),
    ('A03', 'Arjun', 'Kumar', 1),
    ('A04', 'Sahdev', 'Kumar', 1),
    ('A05', 'Rajnish', 'Raj', 1),
    ('A06', 'Abjijeet', 'Kumar', 1),
    ('A07', 'Ashwin', 'Mehta', 1)
]

# Inserting data into Subject
sql_query3 = """INSERT INTO Subject (Subject_id, Subject_name) VALUES (?, ?)"""
values_3 = [
    (109, 'Communication skills-1'),
    (113, 'Computer and Information Technology'),
    (122, 'Software'),
    (140, 'Programming C'),
    (103, 'Environmental Studies'),
    (145, 'French'),
    (111, 'Basic Mathematics'),
    (206, 'Communication Skills-2'),
    (202, 'Operating System'),
    (124, 'Data Structures Using C'),
    (144, 'Digital Circuit Design'),
    (334, 'Fundamental of e-commerce'),
    (104, 'French-Grammar-1'),
    (105, 'Individual Excellence & Social Dynamics'),
    (221, 'Elementary Algorithms'),
    (246, 'Fundamental Database Management System'),
    (314, 'Entrepreneurship Development Programme'),
    (203, 'Object Oriented Programming Using C++'),
    (147, 'Written Expression & Comprehension in French-3')
]

# Inserting data into Enrollments
sql_query4 = """INSERT INTO Enrollments (Enrollment_id) VALUES (?)"""
values_4 = [
    ("A45349523001",),
    ("A45349523002",),
    ("A45349523003",),
    ("A45349523004",),
    ("A45349523005",),
    ("A45349523006",),
    ("A45349523007",)
]

cursor.executemany(sql_query1, values_1)
cursor.executemany(sql_query2, values_2)
cursor.executemany(sql_query3, values_3)
cursor.executemany(sql_query4, values_4)

connection.commit()

# Display records from Student
data = cursor.execute("SELECT * FROM Student")

for row in data:
    print(row)

if connection:
    connection.close()
    print("Database connection closed")
