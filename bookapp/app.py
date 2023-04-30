import os
from flask import Flask, redirect, render_template, request
import sqlite3


app = Flask(__name__)

db_path = "students.db"
# Create a connection to the database file
conn = sqlite3.connect('students.db')

# Create a cursor object
cur = conn.cursor()

# Define a schema for a new table
# if not os.path.exists(db_path):
cur.execute('''CREATE TABLE Students
               (id INTEGER PRIMARY KEY, name TEXT, email TEXT, status TEXT)''')

# Insert some data into the table
cur.execute("INSERT INTO Students (name, email, status) VALUES (?, ?, ?)",
            ('Roland', 'Roland@leadwaymission.com', 'Active'))
cur.execute("INSERT INTO Students (name, email, status) VALUES (?, ?, ?)",
            ('Mike', 'Mike@leadwaymission.com', 'Active'))
cur.execute("INSERT INTO Students (name, email, status) VALUES (?, ?, ?)",
            ('John', 'John@leadwaymission.com', 'Active'))

# Save the changes to the database
conn.commit()

# Close the connection
conn.close()

# Routes


@app.route('/')
def index():
    name = 'Alice'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students")
    students = cur.fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/student/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('addStudent.html')
    if request.method == 'POST':

        # Get data from request form
        name = request.form["name"]
        student_id = request.form["id"]
        status = request.form["status"]

    # Insert data into database
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Students (name, email, status) VALUES (?, ?, ?)",
                    (name, student_id, status))
        conn.commit()

    # Return success message
    # return jsonify({"message": "Student added successfully"}), 201
        return redirect('/')


@app.route('/student/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('deleteStudent.html')
    if request.method == 'POST':

        # Get data from request form
        name = request.form["name"]
        student_id = request.form["id"]
        status = request.form["status"]

    # Insert data into database
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        # cur.execute("DELETE FROM Students WHERE id=?", (id,))
        cur.execute("DELETE FROM Students where id=?",
                    (student_id))
        conn.commit()

    # Return success message
    # return jsonify({"message": "Student added successfully"}), 201
        return redirect('/')


@app.route('/students')
def view():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students")
    students = cur.fetchall()
    conn.close()
    return render_template('viewStudent.html', students=students)


if __name__ == '__main__':
    app.run()
