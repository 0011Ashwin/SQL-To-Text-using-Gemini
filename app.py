# Importing libraries from python
from dotenv import load_dotenv

# Load .env
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configuration of Google API 

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
                    The SQL database has the name AMITY and has the following Tables - Semester, Student, 
                    Subject , Enrollments , Subject_Marks and SGPA_CGPA. For example, 
                    Example 1 - How many entries of records are present?, 
                        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
                    Example 2 - Tell me all the students studying in Semester?, 
                        the SQL command will be something like this SELECT Students.First_name, Students.Last_name, Semester.Semester_name
                        FROM Students
                        JOIN Semester ON Students.Semester_id = Semester.semester_id
                        WHERE Semester.Semester_name = 'Sem1 2023'; 
                        
                    Example 1 - Count Total Students ?, the SQL command will be something like this
                    SELECT COUNT(*) AS Total_Students FROM Student;
                    
                    Example 2 - Count Total Subjects ?, the SQL command will be somthing like this
                    SELECT COUNT(*) AS Total_Subjects FROM Subject;
                    
                    Example 3 - Count Total Enrollments ?, the SQL command will be somthing like this
                    SELECT COUNT(*) AS Total_Enrollments FROM Enrollments;
                    
                    Example 4 - Count Total Semesters ?, the SQL command will be somthings like this 
                    SELECT COUNT(*) AS Total_Semesters FROM Semester;
                    
                    Example 5 - Get all Student and their Semester ?, the SQL command will be somthings like this
                    SELECT Student.Student_id, Student.First_name, Student.Last_name, Semester.Semester_name 
                    FROM Student 
                    JOIN Semester ON Student.Semester_id = Semester.Semester_id;
                    
                    Example 7 - Get all Students in a specific Semester 
                    SELECT First_name, Last_name 
                    FROM Student 
                    WHERE Semester_id = 1;

                    Example 8 - Find a Student by ID ? , the  SQL command will be somthings like this
                    SELECT * FROM Student WHERE Student_id = 'A01';
                    
                    Example 9 - List Student sorted by First Name
                    SELECT * FROM Student ORDER BY First_name ASC;
                    
                    Example 10 - Get the number of students per semester
                    SELECT Semester.Semester_name, COUNT(Student.Student_id) AS Total_Students 
                    FROM Student 
                    JOIN Semester ON Student.Semester_id = Semester.Semester_id 
                    GROUP BY Semester.Semester_name;
                    
                    Example 11 - Get all subjects
                    SELECT * FROM Subject;

                    Example 12 - List All Subjects a Specific Student is Enrolled In
                    SELECT Subject.Subject_name 
                    FROM Subject 
                    JOIN Enrollments ON Subject.Subject_id = Enrollments.Subject_id 
                    JOIN Student ON Student.Student_id = Enrollments.Student_id 
                    WHERE Student.Student_id = 'A01';

                    Example 13 - Get Total Number of Enrollments per Subject
                    SELECT Subject.Subject_name, COUNT(Enrollments.Student_id) AS Total_Enrollments 
                    FROM Subject 
                    JOIN Enrollments ON Subject.Subject_id = Enrollments.Subject_id 
                    GROUP BY Subject.Subject_name;

                    Example 14 -  Get All Students' Marks and Grades
                    SELECT Student.First_name, Student.Last_name, Subject.Subject_name, Subject_Marks.Marks, Subject_Marks.Grade 
                    FROM Student 
                    JOIN Subject_Marks ON Student.Student_id = Subject_Marks.Student_id 
                    JOIN Subject ON Subject_Marks.Subject_id = Subject.Subject_id;

                    Example 15 - Get Marks of a Specific Student (Example: 'A01')
                    SELECT Subject.Subject_name, Subject_Marks.Marks, Subject_Marks.Grade 
                    FROM Subject_Marks 
                    JOIN Subject ON Subject_Marks.Subject_id = Subject.Subject_id 
                    WHERE Subject_Marks.Student_id = 'A01';

                    Example 16 - Get Students Who Scored More Than 80 Marks in Any Subject
                    SELECT Student.First_name, Student.Last_name, Subject.Subject_name, Subject_Marks.Marks 
                    FROM Student 
                    JOIN Subject_Marks ON Student.Student_id = Subject_Marks.Student_id 
                    JOIN Subject ON Subject_Marks.Subject_id = Subject.Subject_id 
                    WHERE Subject_Marks.Marks > 80;
                                        
                    also the sql code should not have ``` in beginning or end and sql word in output.
                    Now convert the following question in English to a valid SQL Query: {user_query}. 
                    No preamble, only valid SQL please

                    
    """


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"Amity.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)
        
        
# Tell me students name
# tell subjects detials 
# Find total number of student in each semester 