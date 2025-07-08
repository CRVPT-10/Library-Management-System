import tkinter as tk
from tkinter import messagebox, ttk
import cx_Oracle

# 🔹 Global database connection
db1 = None

def connect():
    global db1
    db1 = cx_Oracle.connect(user="crvpt", password="sys", dsn="localhost:1521/XE")

connect()

# 🔹 Colors for better UI
theme_bg = "#2C3E50"
theme_fg = "#ECF0F1"
button_bg = "#3498DB"
button_fg = "#FFFFFF"
frame_bg = "#34495E"
title_color = "#E74C3C"
entry_bg = "#ECF0F1"
entry_fg = "#2C3E50"

# 🔹 Login Function
def login():
    un = username_entry.get()
    pw = password_entry.get()
    
    if db1 is None:
        messagebox.showerror("Connection Error", "Database connection not established.")
        return
    
    try:
        cursor = db1.cursor()
        cursor.execute("SELECT * FROM users WHERE username = :un AND passw = :pw", {"un": un, "pw": pw})
        res = cursor.fetchall()
        
        if len(res) == 0:
            messagebox.showerror("Login Failed", "Invalid Username or Password")
        else:
            messagebox.showinfo("Login Success", "Access Granted")
            login_frame.pack_forget()
            operations_frame.pack(side="left", fill="y", padx=10, pady=10)
            right_panel_frame.pack(side="right", fill="both", expand=True)
            show_operations()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# 🔹 Apply UI Styles
def style_widget(widget, bg=theme_bg, fg=theme_fg, font=("Arial", 12)):
    widget.configure(bg=bg, fg=fg, font=font)

# 🔹 Show Operations Panel
def show_operations():
    for widget in operations_frame.winfo_children():
        widget.destroy()

    tk.Label(operations_frame, text="Library Management System", font=("Arial", 16, "bold"), fg=title_color, bg=frame_bg).pack(pady=10)
    
    sections = {
        "Student Management": ["Add Student", "Delete Student", "Show Students"],
        "Faculty Management": ["Add Faculty", "Delete Faculty", "Show Faculty"],
        "Book Management": ["Add Book", "Delete Book", "Show Books"],
        "Issue & Return Books": ["Issue Book", "Return Book"],
        "Issued & Returned Books": ["Show Issued Books", "Show Returned Books"]
    }
    
    for section, buttons in sections.items():
        tk.Label(operations_frame, text=section, font=("Arial", 12, "bold"), bg=frame_bg, fg=theme_fg).pack()
        for btn_text in buttons:
            tk.Button(operations_frame, text=btn_text, command=lambda t=btn_text: update_right_panel(t.lower().replace(" ", "_")),
                      bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat").pack(fill="x", padx=10, pady=5)
    
    tk.Button(operations_frame, text="Logout", command=logout, bg="red", fg="white", font=("Arial", 10, "bold"), relief="flat").pack(fill="x", padx=10, pady=10)

# 🔹 Logout Function
def logout():
    operations_frame.pack_forget()
    right_panel_frame.pack_forget()
    login_frame.pack(side="top", padx=10, pady=10)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# 🔹 Create main application window
root = tk.Tk()
root.title("Library Management System")
root.configure(bg=theme_bg)

# 🔹 Frames
main_frame = tk.Frame(root, bg=theme_bg)
main_frame.pack(fill="both", expand=True)

operations_frame = tk.Frame(main_frame, width=250, bg=frame_bg)
right_panel_frame = tk.Frame(main_frame, bg=theme_bg)
login_frame = tk.Frame(root, bg=theme_bg)

title_label = tk.Label(login_frame, text="Library Management System", font=("Arial", 16, "bold"), fg=title_color, bg=theme_bg)
title_label.grid(row=0, column=0, columnspan=2, pady=20)

username_label = tk.Label(login_frame, text="Username:", bg=theme_bg, fg=theme_fg)
username_label.grid(row=1, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_frame, bg=entry_bg, fg=entry_fg)
username_entry.grid(row=1, column=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password:", bg=theme_bg, fg=theme_fg)
password_label.grid(row=2, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_frame, show="*", bg=entry_bg, fg=entry_fg)
password_entry.grid(row=2, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=login, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat")
login_button.grid(row=3, column=0, columnspan=2, pady=20)



# 🔹 STUDENT MANAGEMENT
def addStudent():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Add New Student", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Student ID", "Name", "Phone", "Email", "Father's Name", "Department"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(right_panel_frame, text=label, bg=theme_bg, fg=theme_fg).grid(row=idx+1, column=0, padx=10, pady=5)
        entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
        entry.grid(row=idx+1, column=1, padx=10, pady=5)
        entries[label] = entry

    def submit_student():
        sid = entries["Student ID"].get()
        name = entries["Name"].get()
        phone = entries["Phone"].get()
        email = entries["Email"].get()
        father_name = entries["Father's Name"].get()
        dept_name = entries["Department"].get()

        if not all([sid, name, phone, email, father_name, dept_name]):
            messagebox.showerror("Validation Error", "All fields must be filled!")
            return

        cursor1 = db1.cursor()
        cursor1.execute("SELECT COUNT(*) FROM students WHERE htno = :sid", {"sid": sid})
        exists = cursor1.fetchone()[0]

        if exists > 0:
            messagebox.showerror("Error", f"Student ID {sid} already exists.")
        else:
            query = """INSERT INTO students (htno, name, phone, email, father_name, dept_name) 
                    VALUES (:sid, :name, :phone, :email, :father_name, :dept_name)"""
            cursor1.execute(query, {"sid": sid, "name": name, "phone": phone, "email": email, "father_name": father_name, "dept_name": dept_name})
            db1.commit()
            messagebox.showinfo("Success", "Student Added Successfully")

    tk.Button(right_panel_frame, text="Submit", command=submit_student, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

def deleteStudent():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Delete Student", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(right_panel_frame, text="Enter Student ID:", bg=theme_bg, fg=theme_fg).grid(row=1, column=0, padx=10, pady=5)
    student_id_entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
    student_id_entry.grid(row=1, column=1, padx=10, pady=5)

    def confirm_delete():
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID.")
            return

        cursor1 = db1.cursor()
        cursor1.execute("""
            SELECT COUNT(*) FROM ISSUETOSTUDENT WHERE htno = :sid AND dateofreturn IS NULL
        """, {"sid": student_id})
        
        if cursor1.fetchone()[0] > 0:
            messagebox.showerror("Error", "Student has active books and cannot be deleted.")
            return

        cursor1.execute("DELETE FROM students WHERE htno = :sid", {"sid": student_id})
        db1.commit()
        messagebox.showinfo("Success", "Student Deleted Successfully")

    tk.Button(right_panel_frame, text="Delete", command=confirm_delete, bg="red", fg="white", font=("Arial", 10, "bold"), relief="flat").grid(row=2, column=0, columnspan=2, pady=10)

def showStudents():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Students List", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).pack(pady=10)

    tree = ttk.Treeview(right_panel_frame, columns=("ID", "Name", "Department", "Email", "Phone", "Father's Name"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in ("ID", "Name", "Department", "Email", "Phone", "Father's Name"):
        tree.heading(col, text=col)

    cursor = db1.cursor()
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# 🔹 FACULTY MANAGEMENT
def addFaculty():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Add Faculty", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Faculty ID", "Name", "Phone", "Email", "Date of Joining (YYYY-MM-DD)", "Department"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(right_panel_frame, text=label, bg=theme_bg, fg=theme_fg).grid(row=idx+1, column=0, padx=10, pady=5)
        entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
        entry.grid(row=idx+1, column=1, padx=10, pady=5)
        entries[label] = entry

    def submit_faculty():
        fid = entries["Faculty ID"].get()
        name = entries["Name"].get()
        phone = entries["Phone"].get()
        email = entries["Email"].get()
        doj = entries["Date of Joining (YYYY-MM-DD)"].get()
        dept_name = entries["Department"].get()

        if not all([fid, name, phone, email, doj, dept_name]):
            messagebox.showerror("Validation Error", "All fields must be filled!")
            return

        cursor1 = db1.cursor()
        cursor1.execute("SELECT COUNT(*) FROM faculty WHERE faculty_id = :fid", {"fid": fid})
        exists = cursor1.fetchone()[0]

        if exists > 0:
            messagebox.showerror("Error", f"Faculty ID {fid} already exists.")
        else:
            query = """INSERT INTO faculty (faculty_id, name, phone, email, dateofjoin, dept_name) 
                    VALUES (:fid, :name, :phone, :email, TO_DATE(:doj, 'YYYY-MM-DD'), :dept_name)"""
            cursor1.execute(query, {"fid": fid, "name": name, "phone": phone, "email": email, "doj": doj, "dept_name": dept_name})
            db1.commit()
            messagebox.showinfo("Success", "Faculty Added Successfully")

    tk.Button(right_panel_frame, text="Submit", command=submit_faculty, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

def deleteFaculty():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Delete Faculty", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(right_panel_frame, text="Enter Faculty ID:", bg=theme_bg, fg=theme_fg).grid(row=1, column=0, padx=10, pady=5)
    faculty_id_entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
    faculty_id_entry.grid(row=1, column=1, padx=10, pady=5)

    def confirm_delete():
        faculty_id = faculty_id_entry.get()
        if not faculty_id:
            messagebox.showerror("Error", "Please enter a Faculty ID.")
            return

        cursor1 = db1.cursor()
        cursor1.execute("""SELECT COUNT(*) FROM ISSUETOFACULTY WHERE faculty_id = :fid AND dateofreturn IS NULL""", {"fid": faculty_id})
        
        if cursor1.fetchone()[0] > 0:
            messagebox.showerror("Error", "Faculty has active books and cannot be deleted.")
            return

        cursor1.execute("DELETE FROM faculty WHERE faculty_id = :fid", {"fid": faculty_id})
        db1.commit()
        messagebox.showinfo("Success", "Faculty Deleted Successfully")

    tk.Button(right_panel_frame, text="Delete", command=confirm_delete, bg="red", fg="white", font=("Arial", 10, "bold"), relief="flat").grid(row=2, column=0, columnspan=2, pady=10)

def showFaculty():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Faculty List", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).pack(pady=10)

    tree = ttk.Treeview(right_panel_frame, columns=("Faculty ID", "Name", "Department", "Email", "Phone", "Date of Join"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in ("Faculty ID", "Name", "Department", "Email", "Phone", "Date of Join"):
        tree.heading(col, text=col)

    cursor = db1.cursor()
    cursor.execute("SELECT * FROM faculty")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# 🔹 BOOK MANAGEMENT
def addBook():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Add New Book", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Book ID", "Title", "Author", "Publisher", "Cost"]
    entries = {}
    for idx, label in enumerate(labels):
        tk.Label(right_panel_frame, text=label, bg=theme_bg, fg=theme_fg).grid(row=idx+1, column=0, padx=10, pady=5)
        entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
        entry.grid(row=idx+1, column=1, padx=10, pady=5)
        entries[label] = entry

    def submit_book():
        bookid = entries["Book ID"].get()
        title = entries["Title"].get()
        author = entries["Author"].get()
        publisher = entries["Publisher"].get()
        cost = entries["Cost"].get()

        if not all([bookid, title, author, publisher, cost]):
            messagebox.showerror("Validation Error", "All fields must be filled!")
            return

        cursor1 = db1.cursor()
        cursor1.execute("SELECT COUNT(*) FROM book WHERE bookid = :bookid", {"bookid": bookid})
        exists = cursor1.fetchone()[0]

        if exists > 0:
            messagebox.showerror("Error", f"Book ID {bookid} already exists.")
        else:
            query = """INSERT INTO book (bookid, title, author, publisher, cost) 
                    VALUES (:bookid, :title, :author, :publisher, :cost)"""
            cursor1.execute(query, {"bookid": bookid, "title": title, "author": author, "publisher": publisher, "cost": cost})
            db1.commit()
            messagebox.showinfo("Success", "Book Added Successfully")

    tk.Button(right_panel_frame, text="Submit", command=submit_book, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

def deleteBook():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Delete Book", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(right_panel_frame, text="Enter Book ID:", bg=theme_bg, fg=theme_fg).grid(row=1, column=0, padx=10, pady=5)
    book_id_entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
    book_id_entry.grid(row=1, column=1, padx=10, pady=5)

    def confirm_delete():
        book_id = book_id_entry.get()
        if not book_id:
            messagebox.showerror("Error", "Please enter a Book ID.")
            return

        cursor1 = db1.cursor()
        cursor1.execute("SELECT COUNT(*) FROM ISSUE WHERE bookid = :bookid AND dateofreturn IS NULL", {"bookid": book_id})
        if cursor1.fetchone()[0] > 0:
            messagebox.showerror("Error", "Book is currently issued and cannot be deleted.")
            return

        cursor1.execute("DELETE FROM book WHERE bookid = :bookid", {"bookid": book_id})
        db1.commit()
        messagebox.showinfo("Success", "Book Deleted Successfully")

    tk.Button(right_panel_frame, text="Delete", command=confirm_delete, bg="red", fg="white", font=("Arial", 10, "bold"), relief="flat").grid(row=2, column=0, columnspan=2, pady=10)

def showBooks():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Book List", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).pack(pady=10)

    tree = ttk.Treeview(right_panel_frame, columns=("Book ID", "Title", "Author", "Publisher", "Cost", "Status"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in ("Book ID", "Title", "Author", "Publisher", "Cost", "Status"):
        tree.heading(col, text=col)

    cursor1 = db1.cursor()
    cursor1.execute("""
        SELECT b.bookid, b.title, b.author, b.publisher, b.cost,
               CASE 
                   WHEN EXISTS (SELECT 1 FROM ISSUE WHERE bookid = b.bookid AND dateofreturn IS NULL) 
                   THEN 'ISSUED'
                   ELSE 'AVAILABLE'
               END AS status
        FROM BOOK b
    """)
    for row in cursor1.fetchall():
        tree.insert("", "end", values=row)

def displayIssuedBooks():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Issued Books", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).pack(pady=10)

    tree = ttk.Treeview(right_panel_frame, columns=("Book ID", "ID", "Role", "Date of Issue", "Date of Return"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in ("Book ID", "ID", "Role", "Date of Issue", "Date of Return"):
        tree.heading(col, text=col)

    cursor = db1.cursor()
    cursor.execute("""
    SELECT bookid, htno, 
           CASE 
               WHEN htno IN (SELECT htno FROM students) THEN 'Student'
               WHEN htno IN (SELECT faculty_id FROM faculty) THEN 'Faculty'
               ELSE NULL
           END AS role,
           dateofissue, dateofreturn 
    FROM ISSUE 
    WHERE dateofreturn IS NULL 
    AND htno IN (SELECT htno FROM students UNION SELECT faculty_id FROM faculty)
""")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def displayReturnedBooks():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Returned Books", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).pack(pady=10)

    tree = ttk.Treeview(right_panel_frame, columns=("Book ID", "ID", "Role", "Date of Issue", "Date of Return"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in ("Book ID", "ID", "Role", "Date of Issue", "Date of Return"):
        tree.heading(col, text=col)

    cursor = db1.cursor()
    cursor.execute("""
        SELECT bookid, htno, 
               CASE 
                   WHEN htno IN (SELECT htno FROM students) THEN 'Student'
                   WHEN htno IN (SELECT faculty_id FROM faculty) THEN 'Faculty'
                   ELSE 'Unknown'
               END AS role,
               dateofissue, dateofreturn 
        FROM ISSUE 
        WHERE dateofreturn IS NOT NULL
    """)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# 🔹 ISSUE & RETURN BOOK
def issueBook():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Issue Book", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Book ID", "Student ID (or Faculty ID)"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(right_panel_frame, text=label, bg=theme_bg, fg=theme_fg).grid(row=idx+1, column=0, padx=10, pady=5)
        entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
        entry.grid(row=idx+1, column=1, padx=10, pady=5)
        entries[label] = entry

    def submit_issue():
        book_id = entries["Book ID"].get()
        user_id = entries["Student ID (or Faculty ID)"].get()

        if not all([book_id, user_id]):
            messagebox.showerror("Validation Error", "All fields must be filled!")
            return

        cursor = db1.cursor()
        cursor.execute("SELECT COUNT(*) FROM ISSUE WHERE bookid = :book_id AND dateofreturn IS NULL", {"book_id": book_id})
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", f"Book ID {book_id} is already issued!")
            return

        query = """INSERT INTO ISSUE (bookid, htno, dateofissue) VALUES (:book_id, :user_id, SYSDATE)"""
        cursor.execute(query, {"book_id": book_id, "user_id": user_id})
        db1.commit()

        messagebox.showinfo("Success", f"Book ID {book_id} issued successfully!")

    tk.Button(right_panel_frame, text="Issue", command=submit_issue, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

def returnBook():
    for widget in right_panel_frame.winfo_children():
        widget.destroy()

    tk.Label(right_panel_frame, text="Return Book", font=("Arial", 14, "bold"), fg=title_color, bg=theme_bg).grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Book ID", "Student ID (or Faculty ID)"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(right_panel_frame, text=label, bg=theme_bg, fg=theme_fg).grid(row=idx+1, column=0, padx=10, pady=5)
        entry = tk.Entry(right_panel_frame, bg=entry_bg, fg=entry_fg)
        entry.grid(row=idx+1, column=1, padx=10, pady=5)
        entries[label] = entry

    def submit_return():
        book_id = entries["Book ID"].get()
        user_id = entries["Student ID (or Faculty ID)"].get()

        if not all([book_id, user_id]):
            messagebox.showerror("Validation Error", "All fields must be filled!")
            return

        cursor = db1.cursor()
        cursor.execute("SELECT COUNT(*) FROM ISSUE WHERE bookid = :book_id AND htno = :user_id AND dateofreturn IS NULL", 
                       {"book_id": book_id, "user_id": user_id})
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Error", f"Book ID {book_id} was not issued to this user!")
            return

        query = "UPDATE ISSUE SET dateofreturn = SYSDATE WHERE bookid = :book_id AND htno = :user_id"
        cursor.execute(query, {"book_id": book_id, "user_id": user_id})
        db1.commit()

        messagebox.showinfo("Success", f"Book ID {book_id} returned successfully!")

    tk.Button(right_panel_frame, text="Return", command=submit_return, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

# 🔹 Function to update the right panel with the selected operation's content
def update_right_panel(operation):
    for widget in right_panel_frame.winfo_children():
        widget.destroy()  # Clear previous content

    if operation == "add_student":
        addStudent()
    elif operation == "delete_student":
        deleteStudent()
    elif operation == "show_students":
        showStudents()
    elif operation == "add_faculty":
        addFaculty()
    elif operation == "delete_faculty":
        deleteFaculty()
    elif operation == "show_faculty":
        showFaculty()
    elif operation == "add_book":
        addBook()
    elif operation == "delete_book":
        deleteBook()
    elif operation == "show_books":
        showBooks()
    elif operation == "issue_book":
        issueBook()
    elif operation == "return_book":
        returnBook()
    elif operation == "show_issued_books":
        displayIssuedBooks()
    elif operation == "show_returned_books":
        displayReturnedBooks()

# 🔹 Create main application window
root = tk.Tk()
root.title("Library Management System")
root.configure(bg=theme_bg)

# 🔹 Frames
main_frame = tk.Frame(root, bg=theme_bg)
main_frame.pack(fill="both", expand=True)

operations_frame = tk.Frame(main_frame, width=250, bg=frame_bg)
right_panel_frame = tk.Frame(main_frame, bg=theme_bg)
login_frame = tk.Frame(root, bg=theme_bg)

title_label = tk.Label(login_frame, text="Library Management System", font=("Arial", 16, "bold"), fg=title_color, bg=theme_bg)
title_label.grid(row=0, column=0, columnspan=2, pady=20)

username_label = tk.Label(login_frame, text="Username:", bg=theme_bg, fg=theme_fg)
username_label.grid(row=1, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_frame, bg=entry_bg, fg=entry_fg)
username_entry.grid(row=1, column=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password:", bg=theme_bg, fg=theme_fg)
password_label.grid(row=2, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_frame, show="*", bg=entry_bg, fg=entry_fg)
password_entry.grid(row=2, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=login, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="flat")
login_button.grid(row=3, column=0, columnspan=2, pady=20)

# 🔹 Pack the login frame initially
login_frame.pack(side="top", padx=25, pady=25)

root.mainloop()