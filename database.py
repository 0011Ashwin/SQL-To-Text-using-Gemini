import sqlite3

# Connect to SQLite
connection = sqlite3.connect("Amity.db")
cursor = connection.cursor()

# Enable Foreign Key Support
cursor.execute("PRAGMA foreign_keys = ON;")

# Creating Semester Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Semester (
    Semester_id INT PRIMARY KEY,
    Semester_name VARCHAR(50) NOT NULL
);
""")

# Creating Student Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    Student_id VARCHAR(20) PRIMARY KEY,
    First_name VARCHAR(50),
    Last_name VARCHAR(50),
    Semester_id INT,
    FOREIGN KEY (Semester_id) REFERENCES Semester(Semester_id) ON DELETE CASCADE
);
""")

# Creating Subject Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Subject (
    Subject_id INT PRIMARY KEY,
    Subject_name VARCHAR(100)
);
""")

# Creating Enrollments Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments (
    Enrollment_id VARCHAR(20) PRIMARY KEY,
    Student_id VARCHAR(20),
    Subject_id INT,
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE,
    FOREIGN KEY (Subject_id) REFERENCES Subject(Subject_id) ON DELETE CASCADE
);
""")

# Creating Subject Marks Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Subject_Marks (
    Student_id VARCHAR(20),
    Subject_id INT,
    Marks INT CHECK (Marks BETWEEN 0 AND 100),
    Grade VARCHAR(2),
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE,
    FOREIGN KEY (Subject_id) REFERENCES Subject(Subject_id) ON DELETE CASCADE,
    PRIMARY KEY (Student_id, Subject_id)
);
""")

# Creating SGPA & CGPA Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS SGPA_CGPA (
    Student_id VARCHAR(20) PRIMARY KEY,
    SGPA FLOAT,
    CGPA FLOAT,
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE
);
""")

# Inserting Data into Semester
sql_query1 = """INSERT OR IGNORE INTO Semester (Semester_id, Semester_name) VALUES (?, ?)"""
values_1 = [(1, 'Sem1'), (2, 'Sem2'), (3, 'Sem3')]

# Inserting Data into Student
sql_query2 = """INSERT OR IGNORE INTO Student (Student_id, First_name, Last_name, Semester_id) VALUES (?, ?, ?, ?)"""
values_2 = [
    ('A01', 'Sameer', 'Jamuar', 1),
    ('A02', 'Hariom', 'Sharnam', 1),
    ('A03', 'Arjun', 'Kumar', 1),
    ('A04', 'Sahdev', 'Kumar', 1),
    ('A05', 'Rajnish', 'Raj', 1),
    ('A06', 'Abjijeet', 'Kumar', 1),
    ('A07', 'Ashwin', 'Mehta', 1)
]

# Inserting Data into Subject
sql_query3 = """INSERT OR IGNORE INTO Subject (Subject_id, Subject_name) VALUES (?, ?)"""
values_3 = [
    (109, 'Communication Skills-1'),
    (113, 'Computer and Information Technology'),
    (122, 'Software Engineering'),
    (140, 'Programming in C'),
    (103, 'Environmental Studies'),
    (145, 'French'),
    (111, 'Basic Mathematics')
]

# Inserting Data into Enrollments
sql_query4 = """INSERT OR IGNORE INTO Enrollments (Enrollment_id, Student_id, Subject_id) VALUES (?, ?, ?)"""
values_4 = [
    ("A45349523001", "A01", 109),
    ("A45349523002", "A02", 113),
    ("A45349523003", "A03", 122),
    ("A45349523004", "A04", 140),
    ("A45349523005", "A05", 103),
    ("A45349523006", "A06", 145),
    ("A45349523007", "A07", 111)
]

# Inserting Data into Subject_Marks
sql_query5 = """INSERT OR IGNORE INTO Subject_Marks (Student_id, Subject_id, Marks, Grade) VALUES (?, ?, ?, ?)"""
values_5 = [
    ("A01", 109, 85, "A"),
    ("A02", 113, 78, "B"),
    ("A03", 122, 92, "A"),
    ("A04", 140, 67, "C"),
    ("A05", 103, 88, "A"),
    ("A06", 145, 74, "B"),
    ("A07", 111, 59, "D")
]

# Calculate SGPA & CGPA (Example Calculation)
cursor.execute("""
INSERT OR IGNORE INTO SGPA_CGPA (Student_id, SGPA, CGPA)
SELECT Student_id,
       ROUND(AVG(CASE WHEN Marks >= 90 THEN 10
                      WHEN Marks >= 80 THEN 9
                      WHEN Marks >= 70 THEN 8
                      WHEN Marks >= 60 THEN 7
                      WHEN Marks >= 50 THEN 6
                      WHEN Marks >= 40 THEN 5
                      ELSE 0 END), 2) AS SGPA,
       ROUND(AVG(CASE WHEN Marks >= 90 THEN 10
                      WHEN Marks >= 80 THEN 9
                      WHEN Marks >= 70 THEN 8
                      WHEN Marks >= 60 THEN 7
                      WHEN Marks >= 50 THEN 6
                      WHEN Marks >= 40 THEN 5
                      ELSE 0 END), 2) AS CGPA
FROM Subject_Marks
GROUP BY Student_id;
""")

cursor.executemany(sql_query1, values_1)
cursor.executemany(sql_query2, values_2)
cursor.executemany(sql_query3, values_3)
cursor.executemany(sql_query4, values_4)
cursor.executemany(sql_query5, values_5)

connection.commit()

# Display Student Records
data = cursor.execute("SELECT * FROM Student")
print("Student Records:")
for row in data:
    print(row)

# Display Subject Marks
marks_data = cursor.execute("SELECT * FROM Subject_Marks")
print("\nSubject Marks:")
for row in marks_data:
    print(row)

# Display SGPA & CGPA
sgpa_data = cursor.execute("SELECT * FROM SGPA_CGPA")
print("\nSGPA & CGPA:")
for row in sgpa_data:
    print(row)

# Close Connection
if connection:
    connection.close()
    print("\nDatabase connection closed.")
print("Database connection closed.")
    
# You are an expert in converting English questions to SQL queries for the AMITY database. The database has the following tables:

# • Semester (Semester_id, Semester_name)
# • Student (Student_id, First_name, Last_name, Semester_id)
# • Subject (Subject_id, Subject_name)
# • Enrollments (Enrollment_id, Student_id, Subject_id)

# Examples:
# Example 1 - How many entries of records are present?
# SELECT COUNT(*) FROM Student;

# Example 2 - Tell me all the students studying in a specific semester.
# SELECT Student.First_name, Student.Last_name, Semester.Semester_name FROM Student JOIN Semester ON Student.Semester_id = Semester.Semester_id WHERE Semester.Semester_name = 'Sem1 2023';

# Example 3 - List all subjects a given student is enrolled in.
# SELECT Subject.Subject_name FROM Subject JOIN Enrollments ON Subject.Subject_id = Enrollments.Subject_id JOIN Student ON Student.Student_id = Enrollments.Student_id WHERE Student.Student_id = 'A01';

# Example 4 - Get the total number of enrollments per subject.
# SELECT Subject.Subject_name, COUNT(Enrollments.Student_id) AS Total_Enrollments FROM Subject JOIN Enrollments ON Subject.Subject_id = Enrollments.Subject_id GROUP BY Subject.Subject_name;

# Now convert the following English question into a valid SQL query for the AMITY database: {user_query}.
# No preamble, only the valid SQL query.



# Query for all-student and sub-query
# get the marks of student of sem_id=1