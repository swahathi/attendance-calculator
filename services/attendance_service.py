from config import ATTENDANCE_LIMIT


class AttendanceService:

    def __init__(self, calendar):

        self.calendar = calendar

    def calculate(self, present_days):

        working_days = len(self.calendar.get_working_days_until_today())

        if working_days == 0:
            percentage = 0
        else:
            percentage = (present_days / working_days) * 100

        required_total = ATTENDANCE_LIMIT * working_days

        required_days = max(0, int(required_total - present_days))

        max_bunk = max(0, int(working_days - required_total))

        return {
            "working_days": working_days,
            "present_days": present_days,
            "percentage": percentage,
            "required_days": required_days,
            "bunk_allowed": max_bunk
        }
