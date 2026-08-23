"""
Student Enrollment Management System
A Streamlit + SQLite CRUD application.

Run locally with:
    python init_db.py
    streamlit run app.py
"""

import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "enrollment.db"

st.set_page_config(page_title="Student Enrollment System", page_icon="🎓", layout="wide")


# ---------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def run_query(query, params=()):
    conn = get_conn()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def run_action(query, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()


def next_id(table, id_col):
    df = run_query(f"SELECT MAX({id_col}) as m FROM {table}")
    m = df["m"].iloc[0]
    return int(m) + 1 if m is not None else 1


# ---------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------
st.sidebar.title("🎓 Enrollment System")
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Students", "Courses", "Instructors", "Enrollments", "Grades", "Reports"],
)

st.sidebar.markdown("---")
st.sidebar.caption("SQLite + Streamlit CRUD app for managing students, courses and enrollments.")


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------
if page == "Dashboard":
    st.title("Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Students", int(run_query("SELECT COUNT(*) c FROM STUDENT")["c"][0]))
    col2.metric("Courses", int(run_query("SELECT COUNT(*) c FROM COURSE")["c"][0]))
    col3.metric("Instructors", int(run_query("SELECT COUNT(*) c FROM INSTRUCTOR")["c"][0]))
    col4.metric("Enrollments", int(run_query("SELECT COUNT(*) c FROM ENROLL")["c"][0]))

    st.subheader("Course-wise student count")
    df = run_query("""
        SELECT c.course_name, COUNT(e.student_id) AS total_students
        FROM COURSE c
        LEFT JOIN ENROLL e ON c.course_id = e.course_id
        GROUP BY c.course_name
    """)
    st.bar_chart(df.set_index("course_name"))


# ---------------------------------------------------------------------
# Students CRUD
# ---------------------------------------------------------------------
elif page == "Students":
    st.title("Students")

    st.dataframe(run_query("SELECT * FROM STUDENT ORDER BY student_id"), use_container_width=True)

    with st.expander("➕ Add student"):
        with st.form("add_student"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=1, max_value=99, value=20)
            email = st.text_input("Email")
            submitted = st.form_submit_button("Add")
            if submitted:
                if not name:
                    st.error("Name is required.")
                else:
                    sid = next_id("STUDENT", "student_id")
                    run_action(
                        "INSERT INTO STUDENT (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                        (sid, name, age, email or None),
                    )
                    st.success(f"Added student '{name}' (ID {sid}).")
                    st.rerun()

    with st.expander("🗑️ Delete student"):
        ids = run_query("SELECT student_id, name FROM STUDENT")["student_id"].tolist()
        if ids:
            del_id = st.selectbox("Student ID to delete", ids)
            if st.button("Delete student"):
                run_action("DELETE FROM STUDENT WHERE student_id = ?", (del_id,))
                st.success(f"Deleted student {del_id}.")
                st.rerun()


# ---------------------------------------------------------------------
# Courses CRUD
# ---------------------------------------------------------------------
elif page == "Courses":
    st.title("Courses")

    df = run_query("""
        SELECT c.course_id, c.course_name, c.credits, i.name AS instructor
        FROM COURSE c
        LEFT JOIN INSTRUCTOR i ON c.instructor_id = i.instructor_id
        ORDER BY c.course_id
    """)
    st.dataframe(df, use_container_width=True)

    with st.expander("➕ Add course"):
        instructors = run_query("SELECT instructor_id, name FROM INSTRUCTOR")
        with st.form("add_course"):
            cname = st.text_input("Course name")
            credits = st.number_input("Credits", min_value=1, max_value=10, value=3)
            instr = st.selectbox(
                "Instructor",
                options=[None] + instructors["instructor_id"].tolist(),
                format_func=lambda x: "—" if x is None else instructors.set_index("instructor_id").loc[x, "name"],
            )
            submitted = st.form_submit_button("Add")
            if submitted:
                if not cname:
                    st.error("Course name is required.")
                else:
                    cid = next_id("COURSE", "course_id")
                    run_action(
                        "INSERT INTO COURSE (course_id, course_name, instructor_id, credits) VALUES (?, ?, ?, ?)",
                        (cid, cname, instr, credits),
                    )
                    st.success(f"Added course '{cname}' (ID {cid}).")
                    st.rerun()

    with st.expander("🗑️ Delete course"):
        ids = run_query("SELECT course_id FROM COURSE")["course_id"].tolist()
        if ids:
            del_id = st.selectbox("Course ID to delete", ids)
            if st.button("Delete course"):
                run_action("DELETE FROM COURSE WHERE course_id = ?", (del_id,))
                st.success(f"Deleted course {del_id}.")
                st.rerun()


# ---------------------------------------------------------------------
# Instructors CRUD
# ---------------------------------------------------------------------
elif page == "Instructors":
    st.title("Instructors")

    st.dataframe(run_query("SELECT * FROM INSTRUCTOR ORDER BY instructor_id"), use_container_width=True)

    with st.expander("➕ Add instructor"):
        with st.form("add_instructor"):
            name = st.text_input("Name")
            dept = st.text_input("Department")
            submitted = st.form_submit_button("Add")
            if submitted:
                if not name:
                    st.error("Name is required.")
                else:
                    iid = next_id("INSTRUCTOR", "instructor_id")
                    run_action(
                        "INSERT INTO INSTRUCTOR (instructor_id, name, department) VALUES (?, ?, ?)",
                        (iid, name, dept or None),
                    )
                    st.success(f"Added instructor '{name}' (ID {iid}).")
                    st.rerun()


# ---------------------------------------------------------------------
# Enrollments CRUD
# ---------------------------------------------------------------------
elif page == "Enrollments":
    st.title("Enrollments")

    df = run_query("""
        SELECT e.enroll_id, s.name AS student, c.course_name AS course, e.enroll_date
        FROM ENROLL e
        JOIN STUDENT s ON e.student_id = s.student_id
        JOIN COURSE c ON e.course_id = c.course_id
        ORDER BY e.enroll_id
    """)
    st.dataframe(df, use_container_width=True)

    with st.expander("➕ Add enrollment"):
        students = run_query("SELECT student_id, name FROM STUDENT")
        courses = run_query("SELECT course_id, course_name FROM COURSE")
        with st.form("add_enroll"):
            sid = st.selectbox(
                "Student", options=students["student_id"].tolist(),
                format_func=lambda x: students.set_index("student_id").loc[x, "name"],
            )
            cid = st.selectbox(
                "Course", options=courses["course_id"].tolist(),
                format_func=lambda x: courses.set_index("course_id").loc[x, "course_name"],
            )
            submitted = st.form_submit_button("Enroll")
            if submitted:
                try:
                    eid = next_id("ENROLL", "enroll_id")
                    run_action(
                        "INSERT INTO ENROLL (enroll_id, student_id, course_id) VALUES (?, ?, ?)",
                        (eid, sid, cid),
                    )
                    st.success("Enrollment added.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("This student is already enrolled in that course.")

    with st.expander("🗑️ Delete enrollment"):
        ids = run_query("SELECT enroll_id FROM ENROLL")["enroll_id"].tolist()
        if ids:
            del_id = st.selectbox("Enrollment ID to delete", ids)
            if st.button("Delete enrollment"):
                run_action("DELETE FROM ENROLL WHERE enroll_id = ?", (del_id,))
                st.success(f"Deleted enrollment {del_id}.")
                st.rerun()


# ---------------------------------------------------------------------
# Grades CRUD
# ---------------------------------------------------------------------
elif page == "Grades":
    st.title("Grades")

    df = run_query("""
        SELECT g.grade_id, s.name AS student, c.course_name AS course, g.grade
        FROM GRADE g
        JOIN ENROLL e ON g.enroll_id = e.enroll_id
        JOIN STUDENT s ON e.student_id = s.student_id
        JOIN COURSE c ON e.course_id = c.course_id
        ORDER BY g.grade_id
    """)
    st.dataframe(df, use_container_width=True)

    with st.expander("➕ Assign grade"):
        ungraded = run_query("""
            SELECT e.enroll_id, s.name AS student, c.course_name AS course
            FROM ENROLL e
            JOIN STUDENT s ON e.student_id = s.student_id
            JOIN COURSE c ON e.course_id = c.course_id
            WHERE e.enroll_id NOT IN (SELECT enroll_id FROM GRADE)
        """)
        if ungraded.empty:
            st.info("All enrollments already have a grade.")
        else:
            with st.form("add_grade"):
                ungraded_indexed = ungraded.set_index("enroll_id")
                eid = st.selectbox(
                    "Enrollment", options=ungraded_indexed.index.tolist(),
                    format_func=lambda x: f"{ungraded_indexed.loc[x, 'student']} — {ungraded_indexed.loc[x, 'course']}",
                )
                grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])
                submitted = st.form_submit_button("Assign")
                if submitted:
                    gid = next_id("GRADE", "grade_id")
                    run_action(
                        "INSERT INTO GRADE (grade_id, enroll_id, grade) VALUES (?, ?, ?)",
                        (gid, eid, grade),
                    )
                    st.success("Grade assigned.")
                    st.rerun()


# ---------------------------------------------------------------------
# Reports (from the original assignment queries)
# ---------------------------------------------------------------------
elif page == "Reports":
    st.title("Reports")

    st.subheader("Students enrolled in courses")
    st.dataframe(run_query("""
        SELECT s.name, c.course_name
        FROM STUDENT s
        JOIN ENROLL e ON s.student_id = e.student_id
        JOIN COURSE c ON e.course_id = c.course_id
    """), use_container_width=True)

    st.subheader("Students not enrolled in any course")
    st.dataframe(run_query("""
        SELECT name FROM STUDENT s
        WHERE NOT EXISTS (
            SELECT * FROM ENROLL e WHERE s.student_id = e.student_id
        )
    """), use_container_width=True)

    st.subheader("Course-wise student count")
    st.dataframe(run_query("""
        SELECT c.course_name, COUNT(e.student_id) AS total_students
        FROM COURSE c
        LEFT JOIN ENROLL e ON c.course_id = e.course_id
        GROUP BY c.course_name
    """), use_container_width=True)

    st.subheader("Average grade points per course")
    grade_points = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
    df = run_query("""
        SELECT c.course_name, g.grade
        FROM GRADE g
        JOIN ENROLL e ON g.enroll_id = e.enroll_id
        JOIN COURSE c ON e.course_id = c.course_id
    """)
    if not df.empty:
        df["points"] = df["grade"].map(grade_points)
        st.dataframe(df.groupby("course_name")["points"].mean().reset_index().rename(
            columns={"points": "avg_grade_points"}), use_container_width=True)
    else:
        st.info("No grades recorded yet.")
