import sqlite3


def connect_db():
    """Create a database connection and return the connection object."""
    connection = sqlite3.connect("School.db")
    return connection


def create_table():
    """Create the students and marks tables if they do not already exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            admission_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
        """
    )
    
    # Create marks table with columns for Physics, Chemistry, Maths, Total, and Percentage
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS marks (
            admission_number TEXT PRIMARY KEY,
            physics REAL NOT NULL,
            chemistry REAL NOT NULL,
            maths REAL NOT NULL,
            total REAL NOT NULL,
            percentage REAL NOT NULL,
            FOREIGN KEY (admission_number) REFERENCES students(admission_number)
        )
        """
    )
    
    conn.commit()
    conn.close()


def add_student():
    """Take student details from input and insert a new record into the students table."""
    print("\nEnter student details to add a new student:")
    admission_number = input("Admission Number: ").strip()
    name = input("Name: ").strip()
    student_class = input("Class: ").strip()
    phone_number = input("Phone Number: ").strip()

    if not admission_number or not name or not student_class or not phone_number:
        print("Error: All fields are required. Please try again.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (admission_number, name, student_class, phone_number) VALUES (?, ?, ?, ?)",
            (admission_number, name, student_class, phone_number),
        )
        conn.commit()
        print("Student added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: A student with admission number '{admission_number}' already exists.")
    finally:
        conn.close()


def view_students():
    """Select all student records and print them in a neatly aligned table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT admission_number, name, student_class, phone_number FROM students")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nNo students found in the database.")
        return

    # Determine column widths for neat formatting.
    headers = ["Admission No.", "Name", "Class", "Phone No."]
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    format_string = " | ".join(f"{{:<{width}}}" for width in widths)
    separator = "-+-".join("-" * width for width in widths)

    print("\nStudent Records:")
    print(format_string.format(*headers))
    print(separator)
    for row in rows:
        print(format_string.format(*row))


def add_marks():
    """Take student marks, calculate total and percentage, and insert into marks table."""
    print("\nEnter student marks:")
    admission_number = input("Admission Number: ").strip()
    
    # Verify if student exists
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE admission_number = ?", (admission_number,))
    student = cursor.fetchone()
    
    if not student:
        print(f"Error: No student found with admission number '{admission_number}'.")
        conn.close()
        return
    
    print(f"Adding marks for: {student[0]}")
    
    # Take marks input for Physics, Chemistry, and Maths
    try:
        physics = float(input("Physics Marks (out of 100): ").strip())
        chemistry = float(input("Chemistry Marks (out of 100): ").strip())
        maths = float(input("Maths Marks (out of 100): ").strip())
        
        # Validate marks range
        if physics < 0 or physics > 100 or chemistry < 0 or chemistry > 100 or maths < 0 or maths > 100:
            print("Error: Marks should be between 0 and 100.")
            conn.close()
            return
        
        # Calculate total and percentage
        total = physics + chemistry + maths
        percentage = (total / 300) * 100
        
        # Insert marks into the marks table
        cursor.execute(
            "INSERT INTO marks (admission_number, physics, chemistry, maths, total, percentage) VALUES (?, ?, ?, ?, ?, ?)",
            (admission_number, physics, chemistry, maths, total, percentage),
        )
        conn.commit()
        print(f"Marks added successfully. Total: {total}, Percentage: {percentage:.2f}%")
    
    except ValueError:
        print("Error: Please enter valid numeric values for marks.")
    except sqlite3.IntegrityError:
        print(f"Error: Marks for admission number '{admission_number}' already exist.")
    finally:
        conn.close()


def view_marks():
    """Select all marks records and print them in a neatly aligned table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT admission_number, physics, chemistry, maths, total, percentage FROM marks")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nNo marks records found in the database.")
        return

    # Determine column widths for neat formatting.
    headers = ["Admission No.", "Physics", "Chemistry", "Maths", "Total", "Percentage"]
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            if index == 5:  # Percentage column
                value_str = f"{value:.2f}%"
            else:
                value_str = str(value)
            widths[index] = max(widths[index], len(value_str))

    format_string = " | ".join(f"{{:<{width}}}" for width in widths)
    separator = "-+-".join("-" * width for width in widths)

    print("\nStudent Marks:")
    print(format_string.format(*headers))
    print(separator)
    for row in rows:
        # Format percentage with 2 decimal places
        formatted_row = list(row)
        formatted_row[5] = f"{formatted_row[5]:.2f}%"
        print(format_string.format(*formatted_row))


def main_menu():
    """Display the main menu and handle user choices."""
    create_table()
    while True:
        print("\n" + "="*50)
        print("      SCHOOL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Marks")
        print("4. View Marks")
        print("5. Exit")
        print("="*50)
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            add_marks()
        elif choice == "4":
            view_marks()
        elif choice == "5":
            print("\nExiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main_menu()
