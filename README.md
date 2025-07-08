# Library-Management-System
A fully functional Library Management System using Python (Tkinter GUI) and Oracle SQL. Handles student/faculty/book records, issuing, returning, and reporting — with a modern UI and secure backend.

# 📚 Library Management System (LMS)

This project is a **Library Database Management System** built using **Python (Tkinter)** for the GUI and **Oracle SQL** for the backend database. It is designed to automate library operations such as managing books, students, faculty, issuing/returning books, and generating reports — minimizing paperwork and improving efficiency.



## 🧠 Project Overview

The LMS is a desktop-based application that connects to an Oracle database (`LIB_DB`) and provides a graphical interface (`LIB_GUI`) for smooth interaction. The system supports multiple user roles (student, faculty, admin) and includes essential operations such as:

- User Authentication
- Book Management (Add/Delete/View)
- Student & Faculty Management
- Book Issuing & Returning
- Viewing Issued/Returned Logs

---

## 💡 Features

✅ Role-based login (admin, student, faculty)  
✅ Add/Delete/View Students and Faculty  
✅ Add/Delete/View Book Inventory  
✅ Book Issuing/Returning with date tracking  
✅ View logs for issued and returned books  
✅ Fine tracking and validations for constraints  
✅ GUI designed using `Tkinter` for usability  
✅ Real-time database integration with Oracle SQL  

---

## 🧱 Technologies Used

| Component        | Technology         |
|------------------|--------------------|
| Programming Lang | Python             |
| GUI Library      | Tkinter            |
| Database         | Oracle SQL         |
| DB Connector     | cx_Oracle          |

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.x installed
- Oracle Database (e.g., Oracle XE)
- Python library: `cx_Oracle`
```bash
pip install cx_Oracle
