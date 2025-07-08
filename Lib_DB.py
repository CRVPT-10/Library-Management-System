import cx_Oracle

# Initialize the database connection
db1 = None

def connect():
    global db1
    db1 = cx_Oracle.connect(user="crvpt", password="sys", dsn="localhost:1521/XE")

connect()

# Create a cursor to interact with the database
c1 = db1.cursor()

# Function to check if a table exists before dropping
def table_exists(cursor, table_name):
    cursor.execute("""
        SELECT COUNT(*) FROM all_tables WHERE table_name = :table_name
    """, {"table_name": table_name.upper()})  # Ensure the table name is in uppercase
    return cursor.fetchone()[0] > 0

# Function to drop tables if they exist
def drop_table_with_retry(cursor, table_name, retries=5):
    for attempt in range(1, retries + 1):
        try:
            if table_exists(cursor, table_name):  # Check if table exists
                cursor.execute(f"DROP TABLE {table_name} CASCADE CONSTRAINTS")
                print(f"Table {table_name} dropped successfully.")
            else:
                print(f"Table {table_name} does not exist, skipping.")
            break
        except cx_Oracle.DatabaseError as e:
            error_code, error_message = e.args
            if error_code == 942:  # Table does not exist
                print(f"Table {table_name} does not exist.")
                break
            elif error_code == 54:  # Resource is busy, retrying
                print(f"Table {table_name} is busy, retrying... ({attempt}/{retries})")
                if attempt == retries:
                    print(f"Failed to drop table {table_name} after {retries} retries.")
            else:
                print(f"Error occurred while dropping table {table_name}: {error_message}")
                break

# List of tables to drop
tables = ['ISSUELOG_STUDENT', 'ISSUELOG_FACULTY', 'ISSUETOSTUDENT', 'ISSUETOFACULTY', 'BOOK', 'STUDENTS', 'FACULTY', 'USERS']

# Drop each table if it exists
for table in tables:
    drop_table_with_retry(c1, table)

# Create USERS table
c1.execute("""
    CREATE TABLE USERS (
        username VARCHAR2(25),
        passw VARCHAR2(25),
        PRIMARY KEY (username)
    )
""")
c1.execute("INSERT INTO USERS (username, passw) VALUES ('admin', '123')")
c1.execute("INSERT INTO USERS (username, passw) VALUES ('crv', '123')")
c1.execute("INSERT INTO USERS (username, passw) VALUES ('crvpt', '123')")

# Create STUDENTS table
c1.execute("""
    CREATE TABLE STUDENTS (
        htno VARCHAR2(15) PRIMARY KEY,
        name VARCHAR2(25),
        dept_name VARCHAR2(10),
        email VARCHAR2(30),
        phone VARCHAR2(15),
        father_name VARCHAR2(25)
    )
""")

# Create FACULTY table
c1.execute("""
    CREATE TABLE FACULTY (
        faculty_id VARCHAR2(15) PRIMARY KEY,
        name VARCHAR2(25),
        dept_name VARCHAR2(10),
        email VARCHAR2(30),
        phone VARCHAR2(15),
        dateofjoin DATE
    )
""")

# Create BOOK table
c1.execute("""
    CREATE TABLE BOOK (
        bookid VARCHAR2(15) PRIMARY KEY,
        title VARCHAR2(25),
        author VARCHAR2(25),
        publisher VARCHAR2(25),
        cost NUMBER
    )
""")

# Create ISSUETOSTUDENT table (Issue books to students)
c1.execute("""
    CREATE TABLE ISSUETOSTUDENT (
        bookid VARCHAR2(50),
        htno VARCHAR2(50),
        dateofissue DATE NOT NULL,
        dateofreturn DATE DEFAULT NULL,
        PRIMARY KEY (bookid, htno),
        FOREIGN KEY (bookid) REFERENCES BOOK(bookid),
        FOREIGN KEY (htno) REFERENCES STUDENTS(htno)
    )
""")

# Create ISSUETOFACULTY table (Issue books to faculty)
c1.execute("""
    CREATE TABLE ISSUETOFACULTY (
        bookid VARCHAR2(50),
        faculty_id VARCHAR2(50),
        dateofissue DATE NOT NULL,
        dateofreturn DATE DEFAULT NULL,
        PRIMARY KEY (bookid, faculty_id),
        FOREIGN KEY (bookid) REFERENCES BOOK(bookid),
        FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id)
    )
""")

# Create ISSUELOG_STUDENT table (Return logs for students)
c1.execute("""
    CREATE TABLE ISSUELOG_STUDENT (
        bookid VARCHAR2(50),
        htno VARCHAR2(50),
        dateofissue DATE NOT NULL,
        dateofreturn DATE NOT NULL,
        fine NUMBER DEFAULT 0,
        PRIMARY KEY (bookid, htno),
        FOREIGN KEY (bookid, htno) REFERENCES ISSUETOSTUDENT(bookid, htno)
    )
""")

# Create ISSUELOG_FACULTY table (Return logs for faculty)
c1.execute("""
    CREATE TABLE ISSUELOG_FACULTY (
        bookid VARCHAR2(50),
        faculty_id VARCHAR2(50),
        dateofissue DATE NOT NULL,
        dateofreturn DATE NOT NULL,
        fine NUMBER DEFAULT 0,
        PRIMARY KEY (bookid, faculty_id),
        FOREIGN KEY (bookid, faculty_id) REFERENCES ISSUETOFACULTY(bookid, faculty_id)
    )
""")

# Commit all the changes
db1.commit()

# Close the cursor and connection
c1.close()
db1.close()

print("Database setup completed successfully.")
