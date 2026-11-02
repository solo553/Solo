# StudentDesk — Student Management System

A beginner-friendly portfolio project built with **HTML, CSS, Python (Flask), and SQLite**.

## Current milestone: Student records

Features:
- Dashboard with total student count and recently added records
- Add student records
- View and search students
- Edit student records
- Delete student records with confirmation
- SQLite storage that persists between runs
- Validation for required fields and duplicate admission numbers

## Requirements

- Python 3.10 or newer
- Internet connection for the first installation of Flask (Google Fonts are optional; the app still works without them)

## Run on Windows

1. Extract the ZIP file into a folder, for example `C:\Projects\student_management_system`.
2. Open that folder in File Explorer.
3. Click the address bar, type `cmd`, and press Enter.
4. Create a virtual environment:

   ```bat
   py -m venv .venv
   ```

5. Activate it:

   ```bat
   .venv\Scripts\activate
   ```

6. Install Flask:

   ```bat
   py -m pip install -r requirements.txt
   ```

7. Start the application:

   ```bat
   py app.py
   ```

8. Open the local address shown in the terminal, normally `http://127.0.0.1:5000`.

Keep the terminal window open while using the app. Press `Ctrl+C` in the terminal to stop it.

## First test

1. Choose **Add a student**.
2. Enter an admission number such as `STU-2026-001` and a full name.
3. Save the record.
4. Search for the student, edit the record, and test deleting a disposable test record.

Use fictional data while testing. Do not enter real student personal information into a demo app.

## Project structure

```text
student_management_system/
├── app.py
├── requirements.txt
├── README.md
├── students.db              # created automatically when the app starts
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── students.html
│   ├── student_form.html
│   └── 404.html
└── static/
    └── style.css
```

## Database

SQLite creates `students.db` automatically. The `students` table stores:
- Admission number (unique)
- Full name
- Email
- Phone
- Course / program
- Created timestamp

## Important notes

- This is a local learning project, not a production student information system.
- The built-in Flask development server is for development only.
- Before public deployment, set a strong secret key, add authentication and authorization, CSRF protection, backups, privacy safeguards, and production hosting.
- This milestone does not yet implement course management or results recording. Those can be added in the next milestone.

## Portfolio description (use after you have run and tested it)

**StudentDesk — Student Management System (Milestone 1)**  
Built a local web application using HTML, CSS, JavaScript-ready frontend structure, Python Flask, and SQLite to create, view, search, update, and delete student records. Implemented form validation, unique admission numbers, and a dashboard with student counts.

Only claim features you have personally tested and understood.
