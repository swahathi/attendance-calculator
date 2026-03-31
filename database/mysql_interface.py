import mysql.connector
from mysql.connector import Error
import json
import time #delay for retry
import sys #exit program if db fails
from datetime import datetime

class MySQLDBInterface:
    """Interface for MySQL database operations tailored for Attendance System 2026"""

    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None 
        self.connect_with_retry()#object creation 

    def connect_with_retry(self):
        """Establish connection with retry logic—crucial for Docker startup."""
        retries = 10
        while retries > 0:
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    consume_results=True,
                    auth_plugin='mysql_native_password'
                )
                if self.connection.is_connected():
                    print(f"Successfully connected to MySQL database: {self.database}")
                    return
            except Error as e:
                print(f"Database connection waiting... {retries} attempts left. Error: {e}")
                time.sleep(5)
                retries -= 1
        
        print("CRITICAL: Database connection failed after multiple retries.")
        sys.exit(1)

    def ensure_connection(self):
        """Checks if connection is alive, reconnects if not."""
        if not self.connection or not self.connection.is_connected():
            self.connect_with_retry()

    # --- College Operations ---

    def create_college(self, name, code=None):
        """
        Creates a college. Generates a code if none provided to satisfy 
        the NOT NULL constraint in your schema.sql.
        """
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Auto-generate a code if not provided (e.g., 'Google' -> 'GOO-2026')
        if not code:
            code = f"{name[:3].upper()}-{datetime.now().year}"
            
        query = """INSERT INTO colleges (college_name, college_code) 
                   VALUES (%s, %s)"""
        try:
            cursor.execute(query, (name, code))
            self.connection.commit()
            print(f"College created: {name} with code {code}")
            return cursor.lastrowid
        except Error as e:
            print(f"Error creating college: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_college_by_name(self, college_name):
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM colleges WHERE college_name = %s"
            cursor.execute(query, (college_name,))
            return cursor.fetchone()
        finally:
            cursor.close()

    # --- User / Auth Operations ---

    def create_user(self, name, college_name, student_id, hashed_password):
        """
        Registers a student. Matches the users table in schema.sql.
        Note: college_name must exist in colleges table first due to FK constraint.
        """
        self.ensure_connection()
        cursor = self.connection.cursor()
        try:
            query = """INSERT INTO users (name, college_name, student_id, password) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (name, college_name, student_id, hashed_password))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error creating user: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_user_by_student_id(self, student_id):
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    # --- Calendar Operations ---

    def upload_and_store_calendar(self, college_id, sem_name, start, end, file_path, working_days=0, weekends="", holidays=None):
        """
        Matches semester_calendars table. 
        Converts holidays list to JSON string for the TEXT column.
        """
        self.ensure_connection()
        cursor = self.connection.cursor()
        try:
            holidays_json = json.dumps(holidays) if holidays else None
            query = """INSERT INTO semester_calendars 
                       (college_id, semester_name, semester_start, semester_end, file_path, working_days, weekend_days, holidays) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (college_id, sem_name, start, end, file_path, working_days, weekends, holidays_json))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error storing calendar: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_college_calendars(self, college_id):
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM semester_calendars WHERE college_id = %s ORDER BY created_at DESC"
            cursor.execute(query, (college_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    # --- Attendance Operations ---

    def add_attendance_record(self, student_id_int, calendar_id, present_days, percentage, status):
        """Matches attendance_records table."""
        self.ensure_connection()
        cursor = self.connection.cursor()
        try:
            query = """INSERT INTO attendance_records 
                       (student_id, calendar_id, present_days, attendance_percentage, status) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (student_id_int, calendar_id, present_days, percentage, status))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding attendance: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    def add_calendar(self, college_id, semester_name, semester_start, semester_end, file_path, working_days=0, weekend_days="", holidays=None):
        """Exactly matches the keys sent by webapp.py"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        try:
            h_json = json.dumps(holidays) if holidays else None
            query = """INSERT INTO semester_calendars 
                   (college_id, semester_name, semester_start, semester_end, file_path, working_days, weekend_days, holidays) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # All variables here now match the arguments above
            cursor.execute(query, (
                college_id, 
                semester_name, 
                semester_start, 
                semester_end, 
                file_path, 
                working_days, 
                weekend_days, 
                h_json
            ))
        
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"SQL Error: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_college_calendars(self, college_id):
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM semester_calendars WHERE college_id = %s ORDER BY calendar_id DESC", (college_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
