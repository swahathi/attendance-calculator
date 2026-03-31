import os
from pathlib import Path

# --- 1. Academic Constants ---
# Used for attendance calculations (75%)
ATTENDANCE_LIMIT = 0.75

# Default Semester Dates (Matching your Spring 2026 Schema)
SEMESTER_START = "2026-01-15"
SEMESTER_END = "2026-05-30"

# Default Working Day counts if not found in Database
S4_WORKINGDAYS = 71
S6_WORKINGDAYS = 74
S8_WORKINGDAYS = 74
WEEKEND_DAYS = ["Sun"]

# --- 2. Paths Configuration ---
# BASE_DIR is the root of your project
BASE_DIR = Path(__file__).resolve().parent

# Ensure the upload folders exist automatically
UPLOAD_FOLDER = BASE_DIR / "uploads"
CALENDAR_UPLOAD_FOLDER = UPLOAD_FOLDER / "calendars"

# Create directories if they don't exist to prevent 'File Not Found' errors
UPLOAD_FOLDER.mkdir(exist_ok=True)
CALENDAR_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# --- 3. Flask Security ---
# REQUIRED for session['user_id'] and flash() messages to work
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key_12345')

# --- 4. MySQL Database Configuration ---
# When running in Docker, 'host' must be 'db' (the service name in docker-compose)
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'rootpassword'), # Match your Docker password
    'database': os.getenv('MYSQL_DATABASE', 'attendance_system')
}

# --- 5. File Constraints ---
# Limit file uploads to 16MB for security and performance
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
