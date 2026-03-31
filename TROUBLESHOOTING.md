# Troubleshooting Guide

## 🔴 Common Issues & Solutions

### 1. MySQL Connection Errors

#### Error: "Access denied for user 'root'@'localhost'"
**Cause**: Wrong password in config.py

**Solution**:
1. Open `config.py`
2. Update password:
```python
MYSQL_CONFIG = {
    'password': 'your_actual_password'  # ← Add correct password
}
```
3. Restart Flask app

#### Error: "Unknown database 'attendance_system'"
**Cause**: Database not created

**Solution**:
```bash
mysql -u root -p < database\schema.sql
```

#### Error: "Can't connect to MySQL server"
**Cause**: MySQL not running

**Solution**:
- Windows: Start MySQL from Services
- Mac: `brew services start mysql`
- Linux: `sudo systemctl start mysql`

---

### 2. Calendar Upload Issues

#### Error: "No file part" when uploading
**Cause**: File input field is empty

**Solution**:
- Select a PDF file before clicking Upload
- Ensure file exists and is readable

#### Error: "Only PDF files are allowed"
**Cause**: File extension is not .pdf

**Solution**:
- Ensure you're selecting a PDF file
- Rename file to end with `.pdf` if needed

#### Warning: "No holidays found in PDF"
**Cause**: PDF doesn't contain holiday keywords

**Solution**:
- This is normal if calendar doesn't explicitly mention holidays
- You can add holidays manually later
- Keywords searched: "holiday", "break", "vacation", "closed", "recess"

#### Error: "Error processing PDF"
**Cause**: PDF might be corrupted or not readable

**Solution**:
- Ensure PDF is not encrypted
- Try opening PDF in Adobe Reader first
- Ensure PDF contains selectable text (not just image)
- If PDF is scanned image, use OCR tool first: tesseract, ABBYY, etc.

---

### 3. Database Issues

#### Error: "Table 'colleges' doesn't exist"
**Cause**: Schema not properly created

**Solution**:
```bash
# Drop old database if exists
mysql -u root -p -e "DROP DATABASE attendance_system;"

# Create fresh database
mysql -u root -p < database\schema.sql

# Verify
mysql -u root -p -e "USE attendance_system; SHOW TABLES;"
```

#### Error: "Duplicate entry for college_code"
**Cause**: College code already exists

**Solution**:
- Use a different college code
- Example: Change "ABC-2025" to "ABC-2026"

#### Error: "Foreign key constraint fails"
**Cause**: Trying to reference non-existent parent record

**Solution**:
- Register college before uploading calendar
- Ensure college_id is valid in session

---

### 4. Flask Application Issues

#### Error: "ModuleNotFoundError: No module named 'mysql'"
**Cause**: mysql-connector-python not installed

**Solution**:
```bash
pip install mysql-connector-python
```

#### Error: "ImportError: cannot import name 'CalendarManagementService'"
**Cause**: File not created or in wrong location

**Solution**:
- Ensure `services/calendar_management_service.py` exists
- Check file path is correct
- Restart Flask app

#### Error: "Port 5000 is already in use"
**Cause**: Another app using port 5000

**Solution**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # Mac/Linux

# Kill process by PID
taskkill /PID <PID>           # Windows
```

Or use different port:
```python
# In webapp.py
app.run(debug=True, port=5001)
```

---

### 5. Session/Login Issues

#### Error: "Please register college first"
**Cause**: College not registered or session expired

**Solution**:
- Register college again
- Clear browser cookies
- Open in incognito/private mode

#### Error: Session shows wrong college
**Cause**: Multiple colleges registered

**Solution**:
- Session stores one college at a time
- If switching colleges, register the other one
- For multiple users, use incognito mode or different browsers

---

### 6. File Upload Issues

#### Error: "No space left on device"
**Cause**: Disk full

**Solution**:
- Delete old calendar PDFs from `uploads/calendars/`
- Clear browser cache
- Check disk space: `df -h` (Linux/Mac) or `dir D:\` (Windows)

#### Error: "Permission denied" when saving file
**Cause**: Folder permissions issue

**Solution**:
```bash
# Windows
# Right-click uploads folder → Properties → Security → Full Control

# Linux/Mac
chmod 755 uploads/
chmod 755 uploads/calendars/
```

---

### 7. Display/View Issues

#### Holidays not showing in calendar details
**Cause**: PDF parsing didn't find holiday text

**Solution**:
- Check PDF contains readable text
- Ensure holiday keywords are present
- Try re-uploading calendar

#### Calendar statistics showing 0 working days
**Cause**: Incorrect date format

**Solution**:
- Use format: YYYY-MM-DD (example: 2025-12-01)
- Ensure start date < end date

---

### 8. API Issues

#### Error: "College not found" in API
**Cause**: Wrong college code or not registered

**Solution**:
```bash
# Check registered colleges
GET http://localhost:5000/api/college/<code>

# Example:
GET http://localhost:5000/api/college/ABC-2025
```

#### Error: "404 Not Found" for calendars API
**Cause**: College has no calendars

**Solution**:
- Upload a calendar first
- Verify college_id is correct

---

## 🛠️ Diagnostic Commands

### Check MySQL Connection
```python
# In Python terminal
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="attendance_system"
)
print("Connection successful!")
conn.close()
```

### Check Database Content
```bash
mysql -u root -p
USE attendance_system;
SELECT * FROM colleges;
SELECT * FROM semester_calendars;
```

### Check Flask Routes
```bash
# Browse to
http://localhost:5000/
http://localhost:5000/admin/college/register
http://localhost:5000/admin/calendar/upload
```

### Check Upload Folder
```bash
ls -la uploads/calendars/      # Linux/Mac
dir uploads\calendars\         # Windows
```

---

## 🔍 Debug Mode

Enable detailed error messages:

In `webapp.py`:
```python
app.run(debug=True)  # Already enabled
```

In browser Console:
```javascript
// Check if JavaScript errors
Press F12 → Console tab
```

---

## 📊 Verify Setup

Run this checklist:

- [ ] MySQL is running
- [ ] Database created (`mysql -p -e "SHOW DATABASES;"`)
- [ ] config.py has correct password
- [ ] requirements.txt packages installed
- [ ] Flask starts without errors
- [ ] Can register college
- [ ] Can upload calendar PDF
- [ ] Calendar statistics show correctly

---

## 📞 Still Not Working?

1. Check Flask console output for specific error
2. Check browser Console (F12)
3. Check MySQL error log
4. Read SETUP_GUIDE.md completely
5. Verify all file paths are correct

### Debug Output to Watch For

**Successful startup**:
```
* Running on http://127.0.0.1:5000
* Debugger PIN: XXXXXXX
```

**Connection successful**:
```
MySQL Database connection successful!
```

**Calendar upload successful**:
```
Calendar 'Sem 4' uploaded successfully!
Working Days: 71, Holidays: 5
```

---

**Version**: 1.0  
**Last Updated**: March 11, 2026
