-- ============================================================
-- Seed Data
-- ============================================================

INSERT INTO STUDENT VALUES (1, 'Rahul Sharma', 20, 'rahul@example.com');
INSERT INTO STUDENT VALUES (2, 'Sneha', 21, 'sneha@example.com');
INSERT INTO STUDENT VALUES (3, 'Amit', 22, 'amit@example.com');
INSERT INTO STUDENT VALUES (4, 'Priya', 20, 'priya@example.com');
INSERT INTO STUDENT VALUES (5, 'Kiran', 23, 'kiran@example.com');
INSERT INTO STUDENT VALUES (6, 'Anjali', 21, 'anjali@example.com');
INSERT INTO STUDENT VALUES (7, 'Vikram', 22, 'vikram@example.com');
INSERT INTO STUDENT VALUES (8, 'Pooja', 20, 'pooja@example.com');
INSERT INTO STUDENT VALUES (9, 'Arjun', 21, 'arjun@example.com');
INSERT INTO STUDENT VALUES (10, 'Meena', 22, 'meena@example.com');

INSERT INTO INSTRUCTOR VALUES (201, 'Dr. Rao', 'Computer Science');
INSERT INTO INSTRUCTOR VALUES (202, 'Dr. Verma', 'Computer Science');
INSERT INTO INSTRUCTOR VALUES (203, 'Dr. Iyer', 'Data Science');

INSERT INTO COURSE VALUES (101, 'DBMS', 201, 4);
INSERT INTO COURSE VALUES (102, 'EAD', 202, 3);
INSERT INTO COURSE VALUES (103, 'FML', 203, 3);

INSERT INTO ENROLL (enroll_id, student_id, course_id) VALUES (1, 1, 101);
INSERT INTO ENROLL (enroll_id, student_id, course_id) VALUES (2, 2, 102);
INSERT INTO ENROLL (enroll_id, student_id, course_id) VALUES (3, 3, 103);
INSERT INTO ENROLL (enroll_id, student_id, course_id) VALUES (4, 1, 102);
INSERT INTO ENROLL (enroll_id, student_id, course_id) VALUES (5, 5, 101);

INSERT INTO GRADE VALUES (1, 1, 'A');
INSERT INTO GRADE VALUES (2, 2, 'B');
INSERT INTO GRADE VALUES (3, 3, 'A');
INSERT INTO GRADE VALUES (4, 4, 'C');
