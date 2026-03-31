CREATE DATABASE IF NOT EXISTS attendance_system;

USE attendance_system;


-- 1. Table for colleges/institutions

CREATE TABLE IF NOT EXISTS colleges (

    college_id INT PRIMARY KEY AUTO_INCREMENT,

    college_name VARCHAR(255) NOT NULL UNIQUE,

    college_code VARCHAR(50) NOT NULL UNIQUE,

    email VARCHAR(255),

    contact_person VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

);


-- 2. Table for semester calendars

CREATE TABLE IF NOT EXISTS semester_calendars (

    calendar_id INT PRIMARY KEY AUTO_INCREMENT,

    college_id INT NOT NULL,

    semester_name VARCHAR(100) NOT NULL,

    semester_start DATE NOT NULL,

    semester_end DATE NOT NULL,

    file_path VARCHAR(500) NOT NULL,

    holidays TEXT,

    working_days INT DEFAULT 0,

    weekend_days VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (college_id) REFERENCES colleges(college_id) ON DELETE CASCADE,

    UNIQUE KEY unique_semester (college_id, semester_name)

);


-- 3. Table for login users (Students)

CREATE TABLE IF NOT EXISTS users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    college_name VARCHAR(255) NOT NULL, 

    student_id VARCHAR(50) UNIQUE NOT NULL, -- The Roll No used for login

    password VARCHAR(255) NOT NULL,         -- Length for Werkzeug password hashes

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (college_name) REFERENCES colleges(college_name) ON UPDATE CASCADE

);


-- 4. Table for students (Detailed Profiles)

CREATE TABLE IF NOT EXISTS students (

    student_id INT PRIMARY KEY AUTO_INCREMENT,

    college_id INT NOT NULL,

    student_roll_id VARCHAR(50) NOT NULL,

    student_name VARCHAR(255) NOT NULL,

    email VARCHAR(255),

    phone VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (college_id) REFERENCES colleges(college_id) ON DELETE CASCADE,

    UNIQUE KEY unique_student (college_id, student_roll_id)

);


-- 5. Table for attendance records

CREATE TABLE IF NOT EXISTS attendance_records (

    attendance_id INT PRIMARY KEY AUTO_INCREMENT,

    student_id INT NOT NULL,

    calendar_id INT NOT NULL,

    present_days INT,

    attendance_percentage DECIMAL(5, 2),

    status VARCHAR(20),

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,

    FOREIGN KEY (calendar_id) REFERENCES semester_calendars(calendar_id) ON DELETE CASCADE

);


-- Create indexes for performance

CREATE INDEX idx_college_name ON colleges(college_name);

CREATE INDEX idx_calendar_college ON semester_calendars(college_id);

CREATE INDEX idx_student_roll ON students(student_roll_id);
-- 1. Insert College
INSERT INTO colleges (college_name, college_code, email, contact_person)
VALUES ('Institute of Technology', 'IOT-2026', 'admin@iot.edu', 'Dr. Smith');
-- 2. Insert Semester Calendar (Linked to College ID 1)
INSERT INTO semester_calendars (college_id, semester_name, semester_start, semester_end, file_path, working_days, weekend_days)

VALUES (1, 'Spring 2026', '2026-01-15', '2026-05-30', '/uploads/calendars/college_1/semester_calendar.pdf', 90, 'Saturday, Sunday');
-- 3. Insert Sample Students (Linked to College ID 1)
INSERT INTO students (college_id, student_roll_id, student_name, email, phone) VALUES
(1, 'S101', 'Aarav Sharma', 'aarav@example.com', '9876543210'),

(1, 'S102', 'Vihaan Gupta', 'vihaan@example.com', '9876543211'),

(1, 'S103', 'Aditi Rao', 'aditi@example.com', '9876543212'),

(1, 'S104', 'Diya Mistry', 'diya@example.com', '9876543213'),

(1, 'S105', 'Sai Kumar', 'sai@example.com', '9876543214'),

(1, 'S106', 'Ananya Iyer', 'ananya@example.com', '9876543215'),

(1, 'S107', 'Arjun Varma', 'arjun@example.com', '9876543216'),

(1, 'S108', 'Kavya Nair', 'kavya@example.com', '9876543217'),

(1, 'S109', 'Rohan Das', 'rohan@example.com', '9876543218'),

(1, 'S110', 'Saanvi Reddy', 'saanvi@example.com', '9876543219'); 
