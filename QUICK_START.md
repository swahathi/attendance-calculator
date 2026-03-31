# Quick Start Guide - 5 Minutes Setup

## ⚡ Quick Setup (Follow in Order)

### Step 1: Install MySQL Package (1 minute)
```bash
pip install mysql-connector-python
```

### Step 2: Set Up MySQL Database (2 minutes)

**Option A: Using MySQL Command Line**
```bash
mysql -u root -p < database\schema.sql
```

**Option B: Manual Setup**
1. Open MySQL client: `mysql -u root -p`
2. Copy-paste contents of `database/schema.sql`
3. Press Enter

### Step 3: Update Database Credentials (1 minute)

Edit `config.py`:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Change if different
    'password': 'your_password', # Add your password
    'database': 'attendance_system'
}
```

### Step 4: Start Application (1 minute)
```bash
python webapp.py
```

Open browser: `http://localhost:5000`

---

## 🎯 First-Time Usage (5 minutes)

### 1. Register Your College
- Click **Admin Panel → Register College**
- Enter:
  - College Name: "My Engineering College"
  - College Code: "MEC-2025" (must be unique)
- Click Register

### 2. Upload Calendar
- Click **Admin Panel → Upload Calendar**
- Fill in:
  - Semester Name: "Sem 4"
  - Start Date: 2025-12-01
  - End Date: 2026-04-30
  - Weekend Days: Sun
- Select your calendar PDF
- Click Upload

### 3. View Statistics
- Go to **Calendars** section
- See:
  - ✓ Working Days: XX
  - ✓ Holidays Found: XX
  - ✓ Total Semester Days: XX

### 4. Check Attendance
- Click **Check Attendance**
- Enter student name/ID
- Enter present days
- View attendance percentage

---

## 📚 What Happens Automatically

When you upload a calendar PDF:
1. ✅ System reads the PDF
2. ✅ Finds holiday mentions
3. ✅ Calculates working days
4. ✅ Stores in database
5. ✅ Shows you the summary

---

## 🆘 If Something Doesn't Work

### "MySQL Connection Error"
→ Check your password in config.py is correct

### "Table Already Exists Error"
→ Database already set up, just update config credentials

### "Calendar Upload Fails"
→ Make sure PDF file is readable text (not scanned image)

### "No Holidays Found"
→ Normal if PDF doesn't mention holidays explicitly

---

## ✨ Key Features Ready to Use

| Feature | Location |
|---------|----------|
| Check Attendance | Home → Check Attendance |
| View Calendar | Home → View Calendar |
| Admin Panel | Home → Admin Panel |
| Upload Calendar | Admin → Upload Calendar |
| Add College | Admin → Register College |

---

## 📞 Need Help?

Read these files:
- **SETUP_GUIDE.md** - Detailed setup instructions
- **IMPLEMENTATION_SUMMARY.md** - What was built
- Database logs - Check for errors

---

**That's it! You're ready to go!** 🚀
