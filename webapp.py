from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import calendar as pycalendar
import time
import os

# Internal Project Imports
from database.mysql_interface import MySQLDBInterface
from services.calendar_management_service import CalendarManagementService
from services.period_weight_service import calculate_weights
from config import MYSQL_CONFIG, UPLOAD_FOLDER, CALENDAR_UPLOAD_FOLDER, ATTENDANCE_LIMIT

# --- 1. Configuration ---
BASE_DIR = Path(__file__).resolve().parent
# Ensure directories exist immediately on startup
UPLOAD_FOLDER.mkdir(exist_ok=True)
CALENDAR_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Secret key is essential for session['user_id'] to work
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key_2026_secure")

# --- 2. Service Initialization ---
mysql_db = None
calendar_service = None

def initialize_services():
    """Retries connection to MySQL to allow the DB container time to start"""
    for i in range(10):
        try:
            db = MySQLDBInterface(**MYSQL_CONFIG)
            service = CalendarManagementService(db, CALENDAR_UPLOAD_FOLDER)
            print(">>> SUCCESS: MySQL and Services initialized!")
            return db, service
        except Exception as e:
            print(f">>> Waiting for MySQL... attempt {i+1}/10. Error: {e}")
            time.sleep(5)
    return None, None

mysql_db, calendar_service = initialize_services()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 3. Authentication Middleware ---

@app.before_request
def require_login():
    """Restricts access to all pages except login and signup if not logged in"""
    allowed_routes = ['login', 'signup', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

# --- 4. Navigation & Auth Routes ---

@app.route("/")
def index():
    return render_template(
        "index.html", 
        user_name=session.get('user_name'),
        college=session.get('user_college')
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        college_name = request.form.get("college") # Text from user
        student_id = request.form.get("student_id")
        password = request.form.get("password")

        # 1. Check if the college already exists
        college = mysql_db.get_college_by_name(college_name)
        
        # 2. If it doesn't exist, create it on the fly!
        if not college:
            mysql_db.create_college(college_name)
            college = mysql_db.get_college_by_name(college_name)
        
        # 3. Now proceed with user creation using the college_id
        hashed_pw = generate_password_hash(password)
        user_created = mysql_db.create_user(name, college_name, student_id, hashed_pw)
        
        if user_created:
            flash("Account created successfully!")
            return redirect(url_for("login"))
            
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        password = request.form.get("password")
        user = mysql_db.get_user_by_student_id(student_id)
        
        if user and check_password_hash(user['password'], password):
            session.permanent = True 
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_college'] = user['college_name']
            return redirect(url_for("index"))
        else:
            flash("Invalid Student ID or Password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out.")
    return redirect(url_for("login"))

# --- 5. Core Features ---

@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    user_college_name = session.get("user_college")
    college_data = mysql_db.get_college_by_name(user_college_name)
    
    if not college_data:
        flash(f"College configuration missing.")
        return redirect(url_for("index"))
    
    result = None
    if request.method == "POST":
        try:
            present_days = int(request.form.get("present") or 0)
            calendars = mysql_db.get_college_calendars(college_data['college_id'])
            
            if not calendars:
                flash("No academic calendar found.")
            else:
                cal = calendars[0] 
                # Linked to your original service's 'working_days_count'
                working = cal['working_days']
                
                if working > 0:
                    perc = (present_days / working) * 100
                    # Logic: (Min required % * total) - present
                    needed = (ATTENDANCE_LIMIT * working) - present_days
                    # Logic: (present / Min %) - total
                    bunks = (present_days / ATTENDANCE_LIMIT) - working

                    result = {
                        "college_name": college_data['college_name'],
                        "working_days_count": working,
                        "present_days": present_days,
                        "percentage": round(perc, 2),
                        "required_days": max(0, int(needed)),
                        "bunk_allowed": max(0, int(bunks)),
                        "status": "Safe" if perc >= (ATTENDANCE_LIMIT * 100) else "Shortage"
                    }
        except ValueError:
            flash("Please enter a valid number.")

    return render_template("attendance.html", result=result)

@app.route("/calendar", methods=["GET", "POST"])
def show_calendar():
    month_text = None
    if request.method == "POST":
        try:
            y = int(request.form.get("year"))
            m = int(request.form.get("month"))
            month_text = pycalendar.month(y, m)
        except (ValueError, TypeError):
            flash("Invalid year or month.")
    return render_template("calendar.html", month_text=month_text)
@app.route("/weights", methods=["GET", "POST"])
def weights():
    data = None
    if request.method == "POST":
        file = request.files.get("timetable") # Matches 'name="timetable"' in HTML
        if file:
            filepath = UPLOAD_FOLDER / secure_filename(file.filename)
            file.save(str(filepath))
            data = calculate_weights(filepath) # and 'total_periods'
    return render_template("weights.html", data=data)
@app.route("/upload-calendar", methods=["GET", "POST"])
def upload_calendar():
    if request.method == "POST":
        # 1. Extract data from the form
        file = request.files.get("file")
        sem_name = request.form.get("semester_name")
        start = request.form.get("semester_start")
        end = request.form.get("semester_end")
        
        # Handle weekends safely (default to Sun if empty)
        raw_weekends = request.form.get("weekend_days", "Sun")
        weekends = [d.strip() for d in raw_weekends.split(",") if d.strip()]

        # 2. DYNAMIC LOGIC: Look up the college ID based on the logged-in user
        user_college_name = session.get("user_college")
        college_record = mysql_db.get_college_by_name(user_college_name)

        if not college_record:
            flash(f"Error: Your college '{user_college_name}' is not registered in our system.")
            return redirect(url_for("index"))

        target_college_id = college_record['college_id']

        # 3. Validation Check
        if not file or file.filename == '':
            flash("No file selected.")
            return redirect(request.url)

        # 4. Process using your original CalendarManagementService
        result = calendar_service.upload_and_store_calendar(
            file=file,
            college_id=target_college_id,
            semester_name=sem_name,
            semester_start=start,
            semester_end=end,
            weekend_days=weekends
        )
        
        if result:
            # result contains the 'working_days_count' returned by your service
            flash(f"Success! Calendar processed for {sem_name}. Found {result['working_days_count']} working days.")
            return redirect(url_for('index'))
        else:
            flash("Failed to process calendar. Please ensure the PDF is readable.")
            
    return render_template("upload_calendar.html")

if __name__ == "__main__":
    # host='0.0.0.0' is required for Docker
    app.run(debug=True, host='0.0.0.0', port=5000)
