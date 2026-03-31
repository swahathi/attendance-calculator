from pathlib import Path
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from datetime import datetime, timedelta
import os

class CalendarManagementService:
    """Service for managing calendar uploads and storage"""

    def __init__(self, mysql_db, upload_folder):
        self.db = mysql_db
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(parents=True, exist_ok=True)

    def upload_and_store_calendar(self, file, college_id, semester_name, 
                                  semester_start, semester_end, weekend_days=None):
        try:
            # 1. Create college-specific folder
            college_folder = self.upload_folder / f"college_{college_id}"
            college_folder.mkdir(exist_ok=True)

            # 2. Save uploaded file (Using timestamp for unique files)
            filename = f"{semester_name.replace(' ', '_')}_{int(datetime.now().timestamp())}.pdf"
            file_path = college_folder / filename
            file.save(str(file_path))

            # 3. Extract calendar data (Fixed to handle OCR fallback)
            extracted_data = self.extract_calendar_data(file_path, semester_start, semester_end, weekend_days)
            if not extracted_data:
                return None

            # 4. Store in database (Synced with your MySQLDBInterface)
            calendar_id = self.db.add_calendar(
                college_id=college_id,
                semester_name=semester_name,
                semester_start=semester_start,
                semester_end=semester_end,
                file_path=str(file_path),
                holidays=extracted_data.get('holidays'),
                working_days=extracted_data.get('working_days_count'),
                weekend_days=','.join(weekend_days) if weekend_days else 'Sun'
            )

            if calendar_id:
                return {
                    'calendar_id': calendar_id,
                    'file_path': str(file_path),
                    'holidays': extracted_data.get('holidays'),
                    'working_days_count': extracted_data.get('working_days_count'),
                    'total_days': extracted_data.get('total_days')
                }
            else:
                if file_path.exists(): file_path.unlink()
                return None

        except Exception as e:
            print(f"Error uploading calendar: {e}")
            return None

    def extract_calendar_data(self, pdf_path, semester_start, semester_end, weekend_days=None):
        if weekend_days is None:
            weekend_days = ['Sun']

        try:
            holidays = []
            text_content = ""
            
            # A. Try extracting text directly
            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content += text + "\n"

            # B. If file is a scanned image, use OCR (Prevents empty results)
            if len(text_content.strip()) < 50:
                images = convert_from_path(str(pdf_path))
                for img in images:
                    text_content += pytesseract.image_to_string(img) + "\n"

            # Extract holidays
            lines = text_content.split("\n")
            keywords = ['holiday', 'break', 'vacation', 'closed', 'recess', 'christmas', 'festival', 'diwali']
            for line in lines:
                if any(k in line.lower() for k in keywords) and len(line.strip()) > 5:
                    holidays.append(line.strip())

            # Calculate working days
            # Fixed: handle both string and datetime object inputs
            start = datetime.strptime(semester_start, "%Y-%m-%d") if isinstance(semester_start, str) else semester_start
            end = datetime.strptime(semester_end, "%Y-%m-%d") if isinstance(semester_end, str) else semester_end
            
            working_days = 0
            current = start
            while current <= end:
                if current.strftime("%a") not in weekend_days:
                    working_days += 1
                current += timedelta(days=1)

            return {
                'holidays': holidays,
                'working_days_count': working_days,
                'total_days': (end - start).days + 1
            }

        except Exception as e:
            print(f"Error extracting calendar data: {e}")
            return None

    def get_calendar_summary(self, calendar_id):
        calendar = self.db.get_calendar(calendar_id)
        if not calendar: return None
        return {
            'calendar_id': calendar['calendar_id'],
            'semester_name': calendar['semester_name'],
            'working_days': calendar['working_days'],
            'holidays': calendar.get('holidays', [])
        }

    def delete_calendar(self, calendar_id):
        calendar = self.db.get_calendar(calendar_id)
        if calendar:
            file_path = Path(calendar['file_path'])
            if file_path.exists():
                file_path.unlink()
            return True # Assuming DB deletion handled elsewhere or added to DB interface
        return False
