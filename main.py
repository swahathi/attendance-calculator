from database.mysql_interface import MySQLDBInterface
from config import MYSQL_CONFIG
from services.calendar_visualizer import CalendarVisualizer


def display(result):
    print("\n----- Attendance Report -----")
    print("Working Days :", result["working_days"])
    print("Present Days :", result["present_days"])
    print("Attendance % :", round(result["percentage"], 2))
    if result["percentage"] < 75:
        print("Below 75%")
        print("Days needed :", result["required_days"])
    else:
        print("You can bunk :", result["bunk_allowed"], "days")
    print("-----------------------------")


def main():
    # Initialize MySQL interface
    try:
        db = MySQLDBInterface(**MYSQL_CONFIG)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    visualizer = CalendarVisualizer()

    while True:
        print("\n====== Attendance System ======")
        print("1 Check by Student Name/ID")
        print("2 Show Calendar")
        print("3 Launch Web UI")
        print("4 Exit")

        choice = input("Choice: ")

        if choice == "1":
            college_id = int(input("Enter College ID: "))
            identifier = input("Enter student ID or name: ")
            
            student = db.get_student(college_id, identifier)
            if not student:
                print("Student not found")
                continue

            present = int(input("Days present: "))
            
            # Get first calendar for calculation
            calendars = db.get_college_calendars(college_id)
            if not calendars:
                print("No calendar found for this college.")
                continue
            
            calendar = calendars[0]
            working_days = calendar['working_days']
            
            percentage = (present / working_days) * 100
            required_total = 0.75 * working_days
            required_days = max(0, int(required_total - present))
            max_bunk = max(0, int(working_days - required_total))
            
            display({
                "working_days": working_days,
                "present_days": present,
                "percentage": percentage,
                "required_days": required_days,
                "bunk_allowed": max_bunk
            })

        elif choice == "2":
            year = int(input("Year: "))
            month = int(input("Month: "))
            visualizer.show_month(year, month)

        elif choice == "3":
            # launch the Flask web application
            try:
                from webapp import app
                print("Starting web interface on http://127.0.0.1:5000 ...")
                app.run(host='0.0.0.0', port=5000, debug=True)
            except Exception as e:
                print(f"Unable to start web UI: {e}")

        elif choice == "4":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
