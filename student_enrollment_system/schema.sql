-- ============================================================
-- Student Enrollment Management System - Schema
-- ============================================================

DROP TABLE IF EXISTS GRADE;
DROP TABLE IF EXISTS ENROLL;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS INSTRUCTOR;
DROP TABLE IF EXISTS STUDENT;

CREATE TABLE STUDENT (
    student_id  INTEGER PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    age         INTEGER CHECK (age > 0 AND age < 100),
    email       VARCHAR(100) UNIQUE
);

CREATE TABLE INSTRUCTOR (
    instructor_id  INTEGER PRIMARY KEY,
    name           VARCHAR(50) NOT NULL,
    department     VARCHAR(50)
);

CREATE TABLE COURSE (
    course_id      INTEGER PRIMARY KEY,
    course_name    VARCHAR(50) NOT NULL,
    instructor_id  INTEGER,
    credits        INTEGER DEFAULT 3,
    FOREIGN KEY (instructor_id) REFERENCES INSTRUCTOR(instructor_id)
);

CREATE TABLE ENROLL (
    enroll_id    INTEGER PRIMARY KEY,
    student_id   INTEGER NOT NULL,
    course_id    INTEGER NOT NULL,
    enroll_date  DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id),
    UNIQUE (student_id, course_id)
);

CREATE TABLE GRADE (
    grade_id    INTEGER PRIMARY KEY,
    enroll_id   INTEGER NOT NULL UNIQUE,
    grade       VARCHAR(2) CHECK (grade IN ('A','B','C','D','F')),
    FOREIGN KEY (enroll_id) REFERENCES ENROLL(enroll_id)
);
