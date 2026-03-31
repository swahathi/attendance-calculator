import pdfplumber
from datetime import datetime, timedelta
from config import SEMESTER_START, SEMESTER_END, WEEKEND_DAYS


class CalendarExtractor:

    def __init__(self, calendar_file=None):

        self.start = datetime.strptime(SEMESTER_START, "%Y-%m-%d")
        self.end = datetime.strptime(SEMESTER_END, "%Y-%m-%d")
        self.calendar_file = calendar_file
        self.holidays = self.extract_holidays()

    def extract_holidays(self):

        holidays = []

        if not self.calendar_file:
            return holidays

        try:

            with pdfplumber.open(self.calendar_file) as pdf:

                text = ""

                for page in pdf.pages:
                    text += page.extract_text()

                lines = text.split("\n")

                for line in lines:

                    if "Holiday" in line or "Christmas" in line or "holiday" in line.lower():

                        holidays.append(line)

        except Exception as e:

            print("PDF reading warning:", e)

        return holidays

    def get_working_days(self):

        current = self.start

        working_days = []

        while current <= self.end:

            weekday = current.strftime("%a")

            if weekday not in WEEKEND_DAYS:

                working_days.append(current)

            current += timedelta(days=1)

        return working_days

    def get_working_days_until_today(self):

        today = datetime.today()

        current = self.start

        working_days = []

        while current <= today and current <= self.end:

            weekday = current.strftime("%a")

            if weekday not in WEEKEND_DAYS:

                working_days.append(current)

            current += timedelta(days=1)

        return working_days
