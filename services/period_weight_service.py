import cv2
import pytesseract
import re

# configure tesseract; assuming it is in the system PATH on Linux
pytesseract.pytesseract.tesseract_cmd = "tesseract"

# subjects we actually care about
VALID_SUBJECTS = [
    "DBMS", "OS", "COA", "MIS", "EEASD", "SE", "ADS",
    "DBMS LAB", "OSL", "OS LAB", "COAA"
]


def calculate_weights(image_path):
    """Extract subjects from a timetable image and calculate period weights.

    Returns a dictionary with subject counts, total periods, and computed weights.
    """

    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)

    table = cv2.add(horizontal, vertical)
    contours, _ = cv2.findContours(table, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    subjects = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 80 or h < 40:
            continue
        cell = img[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cell)
        text = text.upper().replace("\n", " ")

        # remove time patterns
        text = re.sub(r"\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}", "", text)
        # remove standalone numbers
        text = re.sub(r"\d+", "", text)
        text = text.strip()

        if text:
            subjects.append(text)

    subject_count = {}
    for text in subjects:
        for subject in VALID_SUBJECTS:
            if subject in text:
                subject_count[subject] = subject_count.get(subject, 0) + 1

    total_periods = sum(subject_count.values())
    weights = {}

    for subject, period_count in subject_count.items():
        weight = period_count / total_periods if total_periods else 0
        percentage = weight * 100
        weights[subject] = {
            "periods": period_count,
            "weight": weight,
            "percentage": percentage,
            "formula": f"{period_count}/{total_periods} = {weight:.4f}" if total_periods else ""
        }

    return {
        "subject_count": subject_count,
        "total_periods": total_periods,
        "weights": weights,
    }
