# COMP 3005 – Student Management 

This project implements the required PostgreSQL `students` table and four database operations using Python and `psycopg2`.

## Requirements
- PostgreSQL running locally, with pgAdmin 4 available
- Python 3.11 (or a compatible Python 3 version)
- The `psycopg2-binary` package

## Project files

COMP3005-Student-Management/
├── student_management.py   # Python application and interactive menu
├── database/
│   └── setup.sql           # Creates the students table and insert starter data
├── requirements.txt        # Python database connector dependency
├── .gitignore              # Files to exclude from Git
└── README.md               # Documentation and setup instructions

## Database setup (pgAdmin 4)
1. Start PostgreSQL and open pgAdmin 4.
2. Connect to your local PostgreSQL server.
3. Create a database named `student_management_db`.
4. Select that database
5. Execute the SQL script once on the new empty database.
6. lastly verify that John Doe, Jane Smith, and Jim Beam appear in the query result.

## Installing and running the python application.
Open a terminal in the project folder and install the dependency:
- python -m pip install -r requirements.txt

Run the application:
- python student_management.py

- When prompted, enter your PostgreSQL password for the `postgres` user. The password input is hidden so, do not put the password in your source code or public GitHub repository. The application assumes PostgreSQL is at `localhost:5432`, and uses the database `student_management_db`. If your configuration is different, change the connection settings in `connectDatabase()`.

- Python is interpreted and so there is no separate compilation step. If you wish to check the syntax, run:python -m py_compile student_management.py

## Application functions
- `getAllStudents()`: executes `SELECT * FROM students ORDER BY student_id;` and prints the results.
- `addStudent(first_name, last_name, email, enrollment_date)`: uses a parameterized `INSERT` and commits the new record.
- `updateStudentEmail(student_id, new_email)`: uses a parameterized `UPDATE ... WHERE student_id = %s` and commits to it when a student is found.
- `deleteStudent(student_id)`: uses a parameterized `DELETE ... WHERE student_id = %s` and commits when a student is found.

- `connectDatabase()` this establishes and reuses a connection during the program session. `closeDatabase()`then closes it. SQL errors are handled using the `try`/`except`, transactions are rolled back if necessary, and cursors are closed.

- The interactive menu is an optional interface for accessing the four required functions. so, Enter `1`, `2`, `3`, `4`, or `5` to choose an operation or exit.

## Testing and demonstration
1. Choose '1' to show the original three students.
2. Choose '2' to add a test student, example `Sarah Johnson`, `sarah.johnson@example.com`, `2026-11-13`.
3. In pgAdmin, run `SELECT * FROM students ORDER BY student_id;` to verify the insert and note the actual generated ID of Sarah.
4. Choose '3' to update Sarah's email using that ID, then refresh the pgAdmin query to show the changed email.
5. Choose '4' to delete Sarah using the same ID, then refresh the pgAdmin query to verify the deletion.
6. Choose '5' to close the application.

Another thing is do not assume the new student will have ID `4` this is because PostgreSQL identity values are not necessarily reused after deletion or failed inserts.

## Video demonstration 
link: https://youtu.be/NsRtvjq2N9o
