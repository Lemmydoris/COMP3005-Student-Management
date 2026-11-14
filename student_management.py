import psycopg2
from getpass import getpass

# Keep one database connection for the duration of the application.
# The leading underscore shows that this variable is for internal use.
_connection = None

def connectDatabase():
    """Connect to PostgreSQL, reusing an existing open connection."""
    global _connection

    # Avoids asking for the password again for each menu operation.
    if _connection is not None and not _connection.closed:
        return _connection
    
    try:
        _connection = psycopg2.connect(
            host="localhost",
            database="student_management_db",
            user="postgres",
            password=getpass("Enter PostgreSQL password: "),
            port="5432"
        )
        print("Connected to PostgreSQL successfully!")
        return _connection

    except psycopg2.Error as error:
        _connection = None
        print("Database connection failed:", error)
        return None

def getAllStudents():
    """Retrieve and display every record from the students table."""
    connection = connectDatabase()
    if connection is None:
        return
    cursor = None
    try:
        cursor = connection.cursor()

        # SELECT retrieves all records, that are sorted by their student ID.
        cursor.execute("SELECT * FROM students ORDER BY student_id;")
        students = cursor.fetchall()
        connection.commit()

        print("\n--- All Students ---")
        if not students:
            print("No students found.")
        for student in students:
            print(student)

    except psycopg2.Error as error:
        connection.rollback()
        print("Error retrieving students:", error)

    finally:
        if cursor is not None:
            cursor.close()

def addStudent(first_name, last_name, email, enrollment_date):
    """Insert a new student with the supplied details."""
    if not first_name.strip() or not last_name.strip() or not email.strip():
        print("First name, last name, and email are required.")
        return

    connection = connectDatabase()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()

        # Parameter placeholders protect data values when executing SQL.
        insertSQL = """
            INSERT INTO students
            (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(
            insertSQL,
            (first_name.strip(), last_name.strip(), email.strip(), enrollment_date)
        )

        # Commit permanently saves the INSERT operation.
        connection.commit()
        print("Student added successfully!")

    except psycopg2.Error as error:
        connection.rollback()
        print("Error adding student:", error)

    finally:
        if cursor is not None:
            cursor.close()

def updateStudentEmail(student_id, new_email):
    """Update the email address for the student with the given ID."""
    if not new_email.strip():
        print("Email cannot be empty.")
        return
    connection = connectDatabase()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()

        # WHERE limits the UPDATE to the intended student ID.
        updateSQL = """
            UPDATE students
            SET email = %s
            WHERE student_id = %s;
        """
        cursor.execute(updateSQL, (new_email.strip(), student_id))

        if cursor.rowcount > 0:
            connection.commit()
            print("Student email updated successfully!")
        else:
            connection.rollback()
            print("No student found with that ID.")

    except psycopg2.Error as error:
        connection.rollback()
        print("Error updating student email:", error)

    finally:
        if cursor is not None:
            cursor.close()

def deleteStudent(student_id):
    """Delete the student record with the given ID."""
    connection = connectDatabase()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()

        # WHERE prevents accidentally deleting all students.
        deleteSQL = """
            DELETE FROM students
            WHERE student_id = %s;
        """
        cursor.execute(deleteSQL, (student_id,))

        if cursor.rowcount > 0:
            connection.commit()
            print("Student deleted successfully!")
        else:
            connection.rollback()
            print("No student found with that ID.")

    except psycopg2.Error as error:
        connection.rollback()
        print("Error deleting student:", error)

    finally:
        if cursor is not None:
            cursor.close()

def closeDatabase():
    """Close the shared connection when the program exits."""
    global _connection
    if _connection is not None and not _connection.closed:
        _connection.close()
        print("Database connection closed.")
    _connection = None

def main():
    """Display a menu that calls the four required CRUD functions."""
    if connectDatabase() is None:
        return

    try:
        while True:
            print("\n===== STUDENT MANAGEMENT SYSTEM =====")
            print("1. View all students")
            print("2. Add a student")
            print("3. Update student email")
            print("4. Delete a student")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                getAllStudents()

            elif choice == "2":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("Enter email: ")
                date_text = input("Enter enrollment date (YYYY-MM-DD, or blank): ").strip()

                # enrollment_date allows NULL, so blank input becomes None.
                addStudent(first_name, last_name, email, date_text or None)

            elif choice == "3":
                try:
                    student_id = int(input("Enter student ID: "))
                    new_email = input("Enter new email: ")
                    updateStudentEmail(student_id, new_email)
                except ValueError:
                    print("Invalid student ID. Enter a number.")

            elif choice == "4":
                try:
                    student_id = int(input("Enter student ID: "))
                    deleteStudent(student_id)
                except ValueError:
                    print("Invalid student ID. Enter a number.")

            elif choice == "5":
                print("Exiting Student Management System.")
                break

            else:
                print("Invalid choice. Please choose 1-5.")

    finally:
        closeDatabase()


# Start the application only when this file is run directly.
if __name__ == "__main__":
    main()
