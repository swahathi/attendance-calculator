# Attendance Management System - Setup Guide

## 🎯 Overview
This is an attendance management system that allows different colleges to upload their own semester calendars and calculate student attendance based on college-specific working days and holidays.

## 📋 Features
- **College Registration**: Register colleges with unique codes
- **Calendar Upload**: Upload semester calendars (PDF format)
- **Automatic Extraction**: System automatically extracts holidays and calculates working days
- **Attendance Calculation**: Calculate student attendance percentage
- **Timetable Analysis**: Upload timetable images to calculate period weights
- **Multi-College Support**: Different colleges can have different calendars

## 🔧 Prerequisites
- Python 3.8+
- MySQL Server 5.7+
- pip (Python package manager)

## 📦 Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up MySQL Database

#### Step 1: Create Database and Tables
**Windows:**
```bash
mysql -u root -p < database\schema.sql
```

**Linux/Mac:**
```bash
mysql -u root -p < database/schema.sql
```

### 3. Configure Database Connection

Edit `config.py` and update MySQL credentials:
```python
MYSQL_CONFIG = {
    'host': 'localhost',           # Your MySQL host
    'user': 'root',                # Your MySQL username
    'password': 'your_password',   # Your MySQL password
    'database': 'attendance_system'
}
```

## 🚀 Running the Application

### Start the Flask Application
```bash
python webapp.py
```

### Access the Web Application
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### For College Administrators

#### 1. Register College
1. Go to **Admin Panel** → **Register College**
2. Enter College Name, Code, Email, and Contact Person.
3. Click "Register College".

#### 2. Upload Semester Calendar
1. Go to **Admin Panel** → **Upload Calendar**
2. Provide Semester Name, Start Date, End Date, Weekend Days, and PDF file.
3. Click "Upload Calendar".

### For Students

#### Check Attendance
1. Go to **Check Attendance**
2. Enter Student ID/Name and Present Days.
3. View calculated attendance percentage.

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running.
- Check username and password in `config.py`.

### Calendar Upload Fails
- Ensure PDF file is valid and contains readable text.
- Check file permissions in `uploads/` folder.

### Holidays Not Extracted
- System looks for keywords: "Holiday", "break", "vacation", "closed", etc.
- Manually add holidays if not auto-detected.

## 📝 File Structure
```
attendance_system/
├── webapp.py                 # Main Flask application
├── config.py                # Configuration file
├── requirements.txt         # Python dependencies
├── database/
│   ├── schema.sql          # Database schema
│   └── mysql_interface.py  # MySQL database interface
├── extractors/
│   └── calendar_pdf_extractor.py  # PDF extraction logic
├── services/
│   ├── attendance_service.py       # Attendance calculation
│   ├── calendar_management_service.py  # Calendar management
│   └── period_weight_service.py    # Timetable weight calculation
├── templates/
│   └── ...                 # HTML templates
├── uploads/
│   └── calendars/          # Uploaded calendar storage
```
