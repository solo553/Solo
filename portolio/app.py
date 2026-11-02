from pathlib import Path
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, g

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-random-secret-before-deployment"
app.config["DATABASE"] = str(DATABASE)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_no TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            course TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()
    db.close()


@app.route("/")
def dashboard():
    db = get_db()
    total_students = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    recent_students = db.execute(
        "SELECT * FROM students ORDER BY created_at DESC, id DESC LIMIT 5"
    ).fetchall()
    return render_template(
        "dashboard.html",
        total_students=total_students,
        recent_students=recent_students
    )


@app.route("/students")
def students():
    query = request.args.get("q", "").strip()
    db = get_db()
    if query:
        like = f"%{query}%"
        records = db.execute("""
            SELECT * FROM students
            WHERE admission_no LIKE ? OR full_name LIKE ?
               OR email LIKE ? OR phone LIKE ? OR course LIKE ?
            ORDER BY full_name COLLATE NOCASE
        """, (like, like, like, like, like)).fetchall()
    else:
        records = db.execute(
            "SELECT * FROM students ORDER BY full_name COLLATE NOCASE"
        ).fetchall()
    return render_template("students.html", students=records, query=query)


@app.route("/students/new", methods=("GET", "POST"))
def new_student():
    if request.method == "POST":
        values = {
            "admission_no": request.form.get("admission_no", "").strip(),
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "course": request.form.get("course", "").strip(),
        }
        if not values["admission_no"] or not values["full_name"]:
            flash("Admission number and full name are required.", "error")
            return render_template("student_form.html", student=values, mode="Add")

        try:
            db = get_db()
            db.execute("""
                INSERT INTO students (admission_no, full_name, email, phone, course)
                VALUES (:admission_no, :full_name, :email, :phone, :course)
            """, values)
            db.commit()
            flash("Student added successfully.", "success")
            return redirect(url_for("students"))
        except sqlite3.IntegrityError:
            flash("That admission number already exists. Use a unique one.", "error")
            return render_template("student_form.html", student=values, mode="Add")

    return render_template("student_form.html", student={}, mode="Add")


@app.route("/students/<int:student_id>/edit", methods=("GET", "POST"))
def edit_student(student_id):
    db = get_db()
    existing = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if existing is None:
        flash("Student record not found.", "error")
        return redirect(url_for("students"))

    if request.method == "POST":
        values = {
            "admission_no": request.form.get("admission_no", "").strip(),
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "course": request.form.get("course", "").strip(),
        }
        if not values["admission_no"] or not values["full_name"]:
            flash("Admission number and full name are required.", "error")
            return render_template("student_form.html", student=values, mode="Edit")

        try:
            db.execute("""
                UPDATE students
                SET admission_no = :admission_no, full_name = :full_name,
                    email = :email, phone = :phone, course = :course
                WHERE id = :id
            """, {**values, "id": student_id})
            db.commit()
            flash("Student record updated.", "success")
            return redirect(url_for("students"))
        except sqlite3.IntegrityError:
            flash("That admission number already exists. Use a unique one.", "error")
            return render_template("student_form.html", student=values, mode="Edit")

    return render_template("student_form.html", student=dict(existing), mode="Edit")


@app.route("/students/<int:student_id>/delete", methods=("POST",))
def delete_student(student_id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    flash("Student record deleted.", "success")
    return redirect(url_for("students"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
