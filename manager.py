"""
manager.py - Placement and Student Progress Business Logic
Project: Placement Readiness and Student Progress Management System
Batch: DA-VSP-006

Demonstrates:
- PlacementManager class coordinating all modules
- TXT file persistence integration
- Sets for duplicate prevention and uniqueness checks
- Lists and Dictionaries for record processing and rankings
- Conditional logic for validation, categorization, and eligibility
- Error handling with understandable messages
"""

from datetime import datetime
from models import Student, Batch
from file_handler import FileManager
from utils import (
    validate_string,
    validate_email,
    validate_phone,
    validate_date,
    validate_score,
    validate_choice,
    calculate_percentage,
    format_details_card,
    VALID_ATTENDANCE_STATUSES,
    VALID_PROJECT_STATUSES,
    VALID_INTERVIEW_STATUSES,
    PROGRESS_WEIGHTS,
)


class PlacementManager:
    """
    Core management class for batches, students, attendance,
    assessments, practice, mock interviews, progress, eligibility, and reports.
    """

    STUDENTS_FILE = "students.txt"
    BATCHES_FILE = "batches.txt"
    ATTENDANCE_FILE = "attendance.txt"
    ASSESSMENTS_FILE = "assessments.txt"
    PRACTICE_FILE = "practice.txt"
    INTERVIEWS_FILE = "interviews.txt"

    def __init__(self, data_dir="data", reports_dir="reports"):
        self.file_manager = FileManager(data_dir=data_dir, reports_dir=reports_dir)

    # ==========================================
    # MODULE 2: BATCH MANAGEMENT
    # ==========================================

    def create_batch(self, batch_id, batch_name, course_name):
        """
        Creates a new training batch.
        Prevents duplicate batch IDs (case-insensitive check).
        """
        batch = Batch(batch_id=batch_id, batch_name=batch_name, course_name=course_name)

        batches_data = self.file_manager.load_json_data(self.BATCHES_FILE)

        # Check duplicate batch ID using a Set
        existing_ids = {b["batch_id"].upper() for b in batches_data}
        if batch.batch_id in existing_ids:
            raise ValueError(f"Batch with ID '{batch.batch_id}' already exists.")

        batches_data.append(batch.to_dict())
        self.file_manager.save_json_data(self.BATCHES_FILE, batches_data)
        return batch

    def get_all_batches(self):
        """Returns a list of all Batch objects."""
        batches_data = self.file_manager.load_json_data(self.BATCHES_FILE)
        return [Batch.from_dict(b) for b in batches_data]

    def get_batch_by_id(self, batch_id):
        """Retrieves a Batch by ID, or None if not found."""
        cleaned_id = validate_string(batch_id, "Batch ID").upper()
        for batch in self.get_all_batches():
            if batch.batch_id == cleaned_id:
                return batch
        return None

    def batch_exists(self, batch_id):
        """Checks if a batch exists by ID."""
        return self.get_batch_by_id(batch_id) is not None

    # ==========================================
    # MODULE 1: STUDENT REGISTRATION
    # ==========================================

    def generate_next_student_id(self):
        """
        Generates the next unique Student ID in sequence (e.g., ST001, ST002).
        Uses a set of existing numeric suffixes.
        """
        students = self.get_all_students()
        existing_numbers = set()
        for student in students:
            id_str = student.student_id.upper()
            if id_str.startswith("ST"):
                digits = id_str[2:]
                if digits.isdigit():
                    existing_numbers.add(int(digits))

        next_number = 1
        while next_number in existing_numbers:
            next_number += 1

        return f"ST{next_number:03d}"

    def register_student(self, name, email, phone, batch_id, student_id=None):
        """
        Registers a new student after validating unique ID, unique email,
        and ensuring the assigned batch exists.
        """
        # Validate batch exists
        batch_id_clean = validate_string(batch_id, "Batch ID").upper()
        if not self.batch_exists(batch_id_clean):
            raise ValueError(f"Batch '{batch_id_clean}' does not exist. Please create the batch first.")

        # Determine student ID
        if not student_id:
            assigned_id = self.generate_next_student_id()
        else:
            assigned_id = validate_string(student_id, "Student ID").upper()

        students_data = self.file_manager.load_json_data(self.STUDENTS_FILE)

        # Check uniqueness using Sets (Demonstrating Sets)
        existing_ids = {s["student_id"].upper() for s in students_data}
        existing_emails = {s["email"].lower() for s in students_data}

        if assigned_id in existing_ids:
            raise ValueError(f"Student ID '{assigned_id}' is already registered.")

        # Validate email and check duplicate
        validated_email = validate_email(email)
        if validated_email in existing_emails:
            raise ValueError(f"Email '{validated_email}' is already registered with another student.")

        # Create Student instance (validates phone and name)
        new_student = Student(
            student_id=assigned_id,
            name=name,
            email=validated_email,
            phone=phone,
            batch_id=batch_id_clean,
        )

        students_data.append(new_student.to_dict())
        self.file_manager.save_json_data(self.STUDENTS_FILE, students_data)

        # Initialize assessment entry if missing
        self._ensure_student_records(assigned_id)

        return new_student

    def _ensure_student_records(self, student_id):
        """Initializes empty records for a student across tracking files if needed."""
        # 1. Assessment record
        assessments_data = self.file_manager.load_json_data(self.ASSESSMENTS_FILE)
        existing_assess_ids = {a["student_id"].upper() for a in assessments_data}
        if student_id.upper() not in existing_assess_ids:
            assessments_data.append({
                "student_id": student_id.upper(),
                "python_scores": {},
                "sql_score": None,
                "excel_score": None,
                "powerbi_score": None,
                "project_status": "Not Started",
            })
            self.file_manager.save_json_data(self.ASSESSMENTS_FILE, assessments_data)

        # 2. Practice record
        practice_data = self.file_manager.load_json_data(self.PRACTICE_FILE)
        existing_prac_ids = {p["student_id"].upper() for p in practice_data}
        if student_id.upper() not in existing_prac_ids:
            practice_data.append({
                "student_id": student_id.upper(),
                "conducted": 0,
                "attended": 0,
            })
            self.file_manager.save_json_data(self.PRACTICE_FILE, practice_data)

        # 3. Interview record
        interview_data = self.file_manager.load_json_data(self.INTERVIEWS_FILE)
        existing_int_ids = {i["student_id"].upper() for i in interview_data}
        if student_id.upper() not in existing_int_ids:
            interview_data.append({
                "student_id": student_id.upper(),
                "status": "Not Attended",
            })
            self.file_manager.save_json_data(self.INTERVIEWS_FILE, interview_data)

    def get_all_students(self):
        """Returns a list of all Student objects."""
        students_data = self.file_manager.load_json_data(self.STUDENTS_FILE)
        return [Student.from_dict(s) for s in students_data]

    def get_student_by_id(self, student_id):
        """Finds a student by Student ID (case-insensitive)."""
        cleaned_id = validate_string(student_id, "Student ID").upper()
        for student in self.get_all_students():
            if student.student_id == cleaned_id:
                return student
        return None

    def update_student(self, student_id, name=None, email=None, phone=None, batch_id=None):
        """
        Updates student details without changing the student ID.
        Ensures email uniqueness across other students and verifies new batch existence.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' does not exist.")

        students_data = self.file_manager.load_json_data(self.STUDENTS_FILE)

        # If email is being changed, ensure it is not taken by another student
        if email:
            new_email = validate_email(email)
            for rec in students_data:
                if rec["student_id"].upper() != student.student_id:
                    if rec["email"].lower() == new_email:
                        raise ValueError(f"Email '{new_email}' is already used by student {rec['student_id']}.")
            student.email = new_email

        if name:
            student.name = validate_string(name, "Name")

        if phone:
            student.phone = validate_phone(phone)

        if batch_id:
            new_batch_id = validate_string(batch_id, "Batch ID").upper()
            if not self.batch_exists(new_batch_id):
                raise ValueError(f"Batch '{new_batch_id}' does not exist.")
            student.batch_id = new_batch_id

        # Save updated list
        updated_list = []
        for rec in students_data:
            if rec["student_id"].upper() == student.student_id:
                updated_list.append(student.to_dict())
            else:
                updated_list.append(rec)

        self.file_manager.save_json_data(self.STUDENTS_FILE, updated_list)
        return student

    def get_students_by_batch(self, batch_id):
        """Returns list of Student objects assigned to a given batch ID."""
        cleaned_batch_id = validate_string(batch_id, "Batch ID").upper()
        if not self.batch_exists(cleaned_batch_id):
            raise ValueError(f"Batch '{cleaned_batch_id}' does not exist.")

        all_students = self.get_all_students()
        return [s for s in all_students if s.batch_id == cleaned_batch_id]

    # ==========================================
    # MODULE 3: ATTENDANCE TRACKING
    # ==========================================

    def record_attendance(self, student_id, date_str, status):
        """
        Records attendance for a student on a specific date.
        Validates date format (YYYY-MM-DD), status (Present/Absent),
        and prevents duplicate attendance entries for the same student and date.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        valid_date = validate_date(date_str)
        canonical_status = validate_choice(status, VALID_ATTENDANCE_STATUSES, "Attendance Status")

        attendance_data = self.file_manager.load_json_data(self.ATTENDANCE_FILE)

        # Check duplicate attendance date for this student
        for entry in attendance_data:
            if entry["student_id"].upper() == student.student_id and entry["date"] == valid_date:
                raise ValueError(
                    f"Attendance already recorded for student {student.student_id} on {valid_date}."
                )

        attendance_data.append({
            "student_id": student.student_id,
            "date": valid_date,
            "status": canonical_status,
        })
        self.file_manager.save_json_data(self.ATTENDANCE_FILE, attendance_data)
        return True

    def get_attendance_summary(self, student_id):
        """
        Calculates attendance percentage and day counts for a student.
        Formula: (Present Days / Total Days) * 100.
        Returns 0.0% if total recorded days is 0.
        """
        cleaned_id = validate_string(student_id, "Student ID").upper()
        attendance_data = self.file_manager.load_json_data(self.ATTENDANCE_FILE)

        student_records = [
            rec for rec in attendance_data
            if rec["student_id"].upper() == cleaned_id
        ]

        total_days = len(student_records)
        present_days = 0
        absent_days = 0

        for rec in student_records:
            if rec["status"].lower() == "present":
                present_days += 1
            else:
                absent_days += 1

        percentage = calculate_percentage(present_days, total_days)

        return {
            "present_days": present_days,
            "absent_days": absent_days,
            "total_days": total_days,
            "percentage": percentage,
            "has_records": total_days > 0,
        }

    # ==========================================
    # MODULE 4 & 5 & 6: ASSESSMENTS & PROJECT
    # ==========================================

    def _get_or_create_assessment_entry(self, student_id):
        """Internal helper to get student's record from assessments.txt."""
        cleaned_id = validate_string(student_id, "Student ID").upper()
        assessments_data = self.file_manager.load_json_data(self.ASSESSMENTS_FILE)

        for entry in assessments_data:
            if entry["student_id"].upper() == cleaned_id:
                return entry, assessments_data

        # If not present, create new entry
        new_entry = {
            "student_id": cleaned_id,
            "python_scores": {},
            "sql_score": None,
            "excel_score": None,
            "powerbi_score": None,
            "project_status": "Not Started",
        }
        assessments_data.append(new_entry)
        return new_entry, assessments_data

    def add_python_assessment(self, student_id, assessment_id, score):
        """
        Records a Python assessment score (0-100).
        Prevents duplicate assessment IDs for the same student.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        clean_assess_id = validate_string(assessment_id, "Assessment ID").upper()
        valid_score = validate_score(score, "Python Assessment Score")

        entry, all_data = self._get_or_create_assessment_entry(student.student_id)

        if "python_scores" not in entry:
            entry["python_scores"] = {}

        if clean_assess_id in entry["python_scores"]:
            raise ValueError(
                f"Assessment '{clean_assess_id}' already recorded for student {student.student_id}."
            )

        entry["python_scores"][clean_assess_id] = valid_score
        self.file_manager.save_json_data(self.ASSESSMENTS_FILE, all_data)
        return True

    def get_python_assessment_summary(self, student_id):
        """
        Calculates average Python assessment score.
        Formula: Sum of scores / Number of assessments.
        Returns 0.0 if no assessments recorded.
        """
        cleaned_id = validate_string(student_id, "Student ID").upper()
        entry, _ = self._get_or_create_assessment_entry(cleaned_id)
        scores_dict = entry.get("python_scores", {})

        scores_list = list(scores_dict.values())
        count = len(scores_list)

        if count == 0:
            return {
                "scores": {},
                "count": 0,
                "average": 0.0,
                "has_records": False,
            }

        avg = round(sum(scores_list) / count, 2)
        return {
            "scores": scores_dict,
            "count": count,
            "average": avg,
            "has_records": True,
        }

    def update_technical_scores(self, student_id, sql_score=None, excel_score=None, powerbi_score=None):
        """
        Updates SQL, Excel, and Power BI scores manually.
        Scores must be between 0 and 100.
        Missing scores remain None (clearly distinguished from 0).
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        entry, all_data = self._get_or_create_assessment_entry(student.student_id)

        if sql_score is not None:
            entry["sql_score"] = validate_score(sql_score, "SQL Score")

        if excel_score is not None:
            entry["excel_score"] = validate_score(excel_score, "Excel Score")

        if powerbi_score is not None:
            entry["powerbi_score"] = validate_score(powerbi_score, "Power BI Score")

        self.file_manager.save_json_data(self.ASSESSMENTS_FILE, all_data)
        return True

    def update_project_status(self, student_id, status):
        """
        Updates project completion status: Not Started, In Progress, Completed.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        canonical_status = validate_choice(status, VALID_PROJECT_STATUSES, "Project Status")
        entry, all_data = self._get_or_create_assessment_entry(student.student_id)
        entry["project_status"] = canonical_status
        self.file_manager.save_json_data(self.ASSESSMENTS_FILE, all_data)
        return canonical_status

    def get_assessment_details(self, student_id):
        """Returns the full assessment record for a student."""
        cleaned_id = validate_string(student_id, "Student ID").upper()
        entry, _ = self._get_or_create_assessment_entry(cleaned_id)
        return entry

    # ==========================================
    # MODULE 7: PRACTICE SESSION TRACKING
    # ==========================================

    def update_practice_sessions(self, student_id, conducted, attended):
        """
        Records practice sessions.
        Ensures conducted >= 0, attended >= 0, and attended <= conducted.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        try:
            cond_int = int(conducted)
            att_int = int(attended)
        except (ValueError, TypeError):
            raise ValueError("Practice sessions must be whole numbers (integers).")

        if cond_int < 0:
            raise ValueError("Conducted practice sessions cannot be negative.")
        if att_int < 0:
            raise ValueError("Attended practice sessions cannot be negative.")
        if att_int > cond_int:
            raise ValueError(
                f"Attended sessions ({att_int}) cannot exceed conducted sessions ({cond_int})."
            )

        practice_data = self.file_manager.load_json_data(self.PRACTICE_FILE)
        found = False
        for rec in practice_data:
            if rec["student_id"].upper() == student.student_id:
                rec["conducted"] = cond_int
                rec["attended"] = att_int
                found = True
                break

        if not found:
            practice_data.append({
                "student_id": student.student_id,
                "conducted": cond_int,
                "attended": att_int,
            })

        self.file_manager.save_json_data(self.PRACTICE_FILE, practice_data)
        return True

    def get_practice_summary(self, student_id):
        """
        Calculates practice participation percentage.
        Formula: (Attended / Conducted) * 100.
        Returns 0.0% if conducted is 0.
        """
        cleaned_id = validate_string(student_id, "Student ID").upper()
        practice_data = self.file_manager.load_json_data(self.PRACTICE_FILE)

        for rec in practice_data:
            if rec["student_id"].upper() == cleaned_id:
                conducted = rec.get("conducted", 0)
                attended = rec.get("attended", 0)
                pct = calculate_percentage(attended, conducted)
                return {
                    "conducted": conducted,
                    "attended": attended,
                    "percentage": pct,
                    "has_records": conducted > 0,
                }

        return {
            "conducted": 0,
            "attended": 0,
            "percentage": 0.0,
            "has_records": False,
        }

    # ==========================================
    # MODULE 8: MOCK INTERVIEW TRACKING
    # ==========================================

    def update_mock_interview_status(self, student_id, status):
        """
        Updates mock interview status: Not Attended, Attended, Passed.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        canonical_status = validate_choice(status, VALID_INTERVIEW_STATUSES, "Mock Interview Status")

        interview_data = self.file_manager.load_json_data(self.INTERVIEWS_FILE)
        found = False
        for rec in interview_data:
            if rec["student_id"].upper() == student.student_id:
                rec["status"] = canonical_status
                found = True
                break

        if not found:
            interview_data.append({
                "student_id": student.student_id,
                "status": canonical_status,
            })

        self.file_manager.save_json_data(self.INTERVIEWS_FILE, interview_data)
        return canonical_status

    def get_mock_interview_status(self, student_id):
        """Returns mock interview status (defaults to 'Not Attended')."""
        cleaned_id = validate_string(student_id, "Student ID").upper()
        interview_data = self.file_manager.load_json_data(self.INTERVIEWS_FILE)

        for rec in interview_data:
            if rec["student_id"].upper() == cleaned_id:
                return rec.get("status", "Not Attended")

        return "Not Attended"

    # ==========================================
    # MODULE 9: PERFORMANCE CATEGORY
    # ==========================================

    def get_performance_category(self, progress_percentage):
        """
        Classifies performance based on overall progress percentage:
        - Excellent: 85%–100%
        - Good: 70%–84.99%
        - Average: 50%–69.99%
        - Needs Improvement: Below 50%
        Uses simple if-elif-else statements.
        """
        score = float(progress_percentage)
        if score >= 85.0:
            return "Excellent"
        elif score >= 70.0:
            return "Good"
        elif score >= 50.0:
            return "Average"
        else:
            return "Needs Improvement"

    # ==========================================
    # MODULE 14: OVERALL PROGRESS CALCULATION
    # ==========================================

    def calculate_overall_progress(self, student_id):
        """
        Calculates overall progress using weights:
        Attendance: 20%
        Python Average: 20%
        SQL: 10%
        Excel: 10%
        Power BI: 10%
        Project Completion: 10% (Not Started=0, In Progress=50, Completed=100)
        Practice Participation: 10%
        Mock Interview: 10% (Not Attended=0, Attended=50, Passed=100)

        Missing components contribute zero until recorded.
        Returns a dictionary with complete details and rounded total.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        # 1. Attendance (20%)
        att_summary = self.get_attendance_summary(student.student_id)
        att_pct = att_summary["percentage"]
        att_contrib = att_pct * PROGRESS_WEIGHTS["attendance"]

        # 2. Python Average (20%)
        py_summary = self.get_python_assessment_summary(student.student_id)
        py_avg = py_summary["average"]
        py_contrib = py_avg * PROGRESS_WEIGHTS["python"]

        # 3, 4, 5. Technical Scores & Project
        assess_details = self.get_assessment_details(student.student_id)

        # SQL (10%)
        sql_val = assess_details.get("sql_score")
        sql_effective = sql_val if sql_val is not None else 0.0
        sql_contrib = sql_effective * PROGRESS_WEIGHTS["sql"]

        # Excel (10%)
        excel_val = assess_details.get("excel_score")
        excel_effective = excel_val if excel_val is not None else 0.0
        excel_contrib = excel_effective * PROGRESS_WEIGHTS["excel"]

        # Power BI (10%)
        powerbi_val = assess_details.get("powerbi_score")
        powerbi_effective = powerbi_val if powerbi_val is not None else 0.0
        powerbi_contrib = powerbi_effective * PROGRESS_WEIGHTS["powerbi"]

        # 6. Project Score (10%)
        proj_status = assess_details.get("project_status", "Not Started")
        if proj_status == "Completed":
            proj_score = 100.0
        elif proj_status == "In Progress":
            proj_score = 50.0
        else:
            proj_score = 0.0
        proj_contrib = proj_score * PROGRESS_WEIGHTS["project"]

        # 7. Practice Participation (10%)
        prac_summary = self.get_practice_summary(student.student_id)
        prac_pct = prac_summary["percentage"]
        prac_contrib = prac_pct * PROGRESS_WEIGHTS["practice"]

        # 8. Mock Interview (10%)
        mock_status = self.get_mock_interview_status(student.student_id)
        if mock_status == "Passed":
            mock_score = 100.0
        elif mock_status == "Attended":
            mock_score = 50.0
        else:
            mock_score = 0.0
        mock_contrib = mock_score * PROGRESS_WEIGHTS["interview"]

        # Total Progress
        total_progress = (
            att_contrib
            + py_contrib
            + sql_contrib
            + excel_contrib
            + powerbi_contrib
            + proj_contrib
            + prac_contrib
            + mock_contrib
        )
        total_progress = round(total_progress, 2)
        category = self.get_performance_category(total_progress)

        return {
            "student_id": student.student_id,
            "student_name": student.name,
            "batch_id": student.batch_id,
            "attendance_pct": att_pct,
            "attendance_contrib": round(att_contrib, 2),
            "attendance_recorded": att_summary["has_records"],
            "python_avg": py_avg,
            "python_contrib": round(py_contrib, 2),
            "python_recorded": py_summary["has_records"],
            "sql_score": sql_val,
            "sql_contrib": round(sql_contrib, 2),
            "excel_score": excel_val,
            "excel_contrib": round(excel_contrib, 2),
            "powerbi_score": powerbi_val,
            "powerbi_contrib": round(powerbi_contrib, 2),
            "project_status": proj_status,
            "project_score": proj_score,
            "project_contrib": round(proj_contrib, 2),
            "practice_pct": prac_pct,
            "practice_contrib": round(prac_contrib, 2),
            "practice_recorded": prac_summary["has_records"],
            "mock_status": mock_status,
            "mock_score": mock_score,
            "mock_contrib": round(mock_contrib, 2),
            "overall_progress": total_progress,
            "category": category,
        }

    # ==========================================
    # MODULE 10: PLACEMENT ELIGIBILITY CHECK
    # ==========================================

    def check_placement_eligibility(self, student_id):
        """
        Checks if a student satisfies ALL 8 placement eligibility rules:
        1. Attendance >= 75% (and at least 1 day recorded)
        2. Python Average >= 60% (and at least 1 assessment recorded)
        3. SQL Score >= 60 (must not be None)
        4. Excel Score >= 60 (must not be None)
        5. Power BI Score >= 60 (must not be None)
        6. Project Status == Completed
        7. Practice Participation >= 70% (and at least 1 session conducted)
        8. Mock Interview Status == Passed

        Returns: (is_eligible: bool, reasons: list of str)
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        reasons = []

        # 1. Attendance
        att = self.get_attendance_summary(student.student_id)
        if not att["has_records"]:
            reasons.append("Attendance records have not been entered (Minimum required: 75%).")
        elif att["percentage"] < 75.0:
            reasons.append(
                f"Attendance is {att['percentage']}% (Minimum required: 75.00%)."
            )

        # 2. Python Average
        py = self.get_python_assessment_summary(student.student_id)
        if not py["has_records"]:
            reasons.append("No Python assessments taken yet (Minimum average required: 60.00%).")
        elif py["average"] < 60.0:
            reasons.append(
                f"Python assessment average is {py['average']}% (Minimum required: 60.00%)."
            )

        # 3. SQL Score
        assess = self.get_assessment_details(student.student_id)
        sql_val = assess.get("sql_score")
        if sql_val is None:
            reasons.append("SQL score has not been entered (Minimum required: 60).")
        elif sql_val < 60.0:
            reasons.append(f"SQL score is {sql_val} (Minimum required: 60).")

        # 4. Excel Score
        excel_val = assess.get("excel_score")
        if excel_val is None:
            reasons.append("Excel score has not been entered (Minimum required: 60).")
        elif excel_val < 60.0:
            reasons.append(f"Excel score is {excel_val} (Minimum required: 60).")

        # 5. Power BI Score
        pbi_val = assess.get("powerbi_score")
        if pbi_val is None:
            reasons.append("Power BI score has not been entered (Minimum required: 60).")
        elif pbi_val < 60.0:
            reasons.append(f"Power BI score is {pbi_val} (Minimum required: 60).")

        # 6. Project Status
        proj_status = assess.get("project_status", "Not Started")
        if proj_status != "Completed":
            reasons.append(f"Project status is '{proj_status}' (Must be 'Completed').")

        # 7. Practice Participation
        prac = self.get_practice_summary(student.student_id)
        if not prac["has_records"]:
            reasons.append("Practice sessions have not been conducted/recorded (Minimum required: 70%).")
        elif prac["percentage"] < 70.0:
            reasons.append(
                f"Practice participation is {prac['percentage']}% (Minimum required: 70.00%)."
            )

        # 8. Mock Interview
        mock_status = self.get_mock_interview_status(student.student_id)
        if mock_status != "Passed":
            reasons.append(
                f"Mock interview status is '{mock_status}' (Must be 'Passed')."
            )

        is_eligible = len(reasons) == 0
        return is_eligible, reasons

    # ==========================================
    # MODULE 11: STUDENT SEARCH
    # ==========================================

    def search_students(self, query, search_type="name"):
        """
        Searches students by:
        - "id": Student ID (partial / exact)
        - "name": Full name (case-insensitive, partial matching)
        - "batch": Batch ID (case-insensitive)
        """
        cleaned_query = validate_string(query, "Search query").lower()
        all_students = self.get_all_students()
        results = []

        for student in all_students:
            if search_type == "id":
                if cleaned_query in student.student_id.lower():
                    results.append(student)
            elif search_type == "name":
                if cleaned_query in student.name.lower():
                    results.append(student)
            elif search_type == "batch":
                if cleaned_query == student.batch_id.lower():
                    results.append(student)
            else:
                raise ValueError(f"Invalid search type: '{search_type}'. Choose 'id', 'name', or 'batch'.")

        return results

    # ==========================================
    # MODULE 12: TOP PERFORMERS
    # ==========================================

    def get_top_performers(self, limit=5):
        """
        Ranks students by overall progress percentage in descending order.
        Uses student_id as consistent tie-breaker.
        Handles cases with fewer than 5 students.
        """
        all_students = self.get_all_students()
        if not all_students:
            return []

        ranked_list = []
        for student in all_students:
            prog = self.calculate_overall_progress(student.student_id)
            ranked_list.append(prog)

        # Sort by overall_progress desc, then student_id asc
        ranked_list.sort(key=lambda x: (-x["overall_progress"], x["student_id"]))

        return ranked_list[:limit]

    # ==========================================
    # MODULE 13: STUDENTS NEEDING IMPROVEMENT
    # ==========================================

    def get_students_needing_improvement(self):
        """
        Identifies students who satisfy at least one condition:
        - Overall progress < 50%
        - Attendance < 75%
        - Any recorded assessment score < 60 (Python avg, SQL, Excel, Power BI)
        - Missing assessment records (highlighted as incomplete information)

        Returns a list of dicts with student details and specific reasons.
        Avoids duplicate students using a Set.
        """
        all_students = self.get_all_students()
        results = []
        seen_ids = set()

        for student in all_students:
            prog = self.calculate_overall_progress(student.student_id)
            reasons = []

            # Check 1: Progress < 50%
            if prog["overall_progress"] < 50.0:
                reasons.append(f"Overall progress is {prog['overall_progress']}% (Below 50%).")

            # Check 2: Attendance < 75%
            if prog["attendance_pct"] < 75.0:
                if not prog["attendance_recorded"]:
                    reasons.append("No attendance records found.")
                else:
                    reasons.append(f"Attendance is {prog['attendance_pct']}% (Below 75%).")

            # Check 3: Python average < 60%
            if not prog["python_recorded"]:
                reasons.append("Incomplete data: Python assessments not taken.")
            elif prog["python_avg"] < 60.0:
                reasons.append(f"Python assessment average is {prog['python_avg']}% (Below 60%).")

            # Check 4: SQL Score
            if prog["sql_score"] is None:
                reasons.append("Incomplete data: SQL score not entered.")
            elif prog["sql_score"] < 60.0:
                reasons.append(f"SQL score is {prog['sql_score']} (Below 60).")

            # Check 5: Excel Score
            if prog["excel_score"] is None:
                reasons.append("Incomplete data: Excel score not entered.")
            elif prog["excel_score"] < 60.0:
                reasons.append(f"Excel score is {prog['excel_score']} (Below 60).")

            # Check 6: Power BI Score
            if prog["powerbi_score"] is None:
                reasons.append("Incomplete data: Power BI score not entered.")
            elif prog["powerbi_score"] < 60.0:
                reasons.append(f"Power BI score is {prog['powerbi_score']} (Below 60).")

            # If any trigger matched and student not already added
            if reasons and student.student_id not in seen_ids:
                seen_ids.add(student.student_id)
                results.append({
                    "student_id": student.student_id,
                    "student_name": student.name,
                    "batch_id": student.batch_id,
                    "overall_progress": prog["overall_progress"],
                    "category": prog["category"],
                    "reasons": reasons,
                })

        return results

    # ==========================================
    # MODULE 15: TXT-BASED REPORTS
    # ==========================================

    def generate_student_report(self, student_id):
        """
        Generates a comprehensive readable TXT report for an individual student.
        Saves report into reports/student_report_<student_id>.txt.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        batch = self.get_batch_by_id(student.batch_id)
        batch_name = batch.batch_name if batch else "Unknown Batch"
        course_name = batch.course_name if batch else "Unknown Course"

        progress = self.calculate_overall_progress(student.student_id)
        is_eligible, reasons = self.check_placement_eligibility(student.student_id)

        # Prepare formatted text
        lines = []
        lines.append("=" * 65)
        lines.append("    STUDENT PROGRESS AND PLACEMENT READINESS REPORT")
        lines.append("=" * 65)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        lines.append("1. BASIC INFORMATION")
        lines.append("-" * 40)
        lines.append(f"Student ID       : {student.student_id}")
        lines.append(f"Full Name        : {student.name}")
        lines.append(f"Email Address    : {student.email}")
        lines.append(f"Phone Number     : {student.phone}")
        lines.append(f"Batch ID         : {student.batch_id}")
        lines.append(f"Batch Name       : {batch_name}")
        lines.append(f"Course Name      : {course_name}")
        lines.append("")

        lines.append("2. ATTENDANCE METRICS (Weight: 20%)")
        lines.append("-" * 40)
        att = self.get_attendance_summary(student.student_id)
        lines.append(f"Recorded Days    : {att['total_days']}")
        lines.append(f"Present Days     : {att['present_days']}")
        lines.append(f"Absent Days      : {att['absent_days']}")
        lines.append(f"Attendance Rate  : {att['percentage']}%")
        lines.append(f"Contribution     : {progress['attendance_contrib']} / 20.00")
        lines.append("")

        lines.append("3. TECHNICAL ASSESSMENT SCORES")
        lines.append("-" * 40)
        py = self.get_python_assessment_summary(student.student_id)
        lines.append(f"Python Assessments: {py['count']} recorded")
        if py["scores"]:
            for a_id, sc in py["scores"].items():
                lines.append(f"  - {a_id}: {sc}")
        lines.append(f"Python Average   : {py['average']}% (Weight: 20%, Contrib: {progress['python_contrib']})")

        sql_display = f"{progress['sql_score']} / 100" if progress['sql_score'] is not None else "Not Entered (Missing)"
        lines.append(f"SQL Score        : {sql_display} (Weight: 10%, Contrib: {progress['sql_contrib']})")

        excel_display = f"{progress['excel_score']} / 100" if progress['excel_score'] is not None else "Not Entered (Missing)"
        lines.append(f"Excel Score      : {excel_display} (Weight: 10%, Contrib: {progress['excel_contrib']})")

        pbi_display = f"{progress['powerbi_score']} / 100" if progress['powerbi_score'] is not None else "Not Entered (Missing)"
        lines.append(f"Power BI Score   : {pbi_display} (Weight: 10%, Contrib: {progress['powerbi_contrib']})")
        lines.append("")

        lines.append("4. PROJECT & PRACTICAL ACTIVITIES")
        lines.append("-" * 40)
        lines.append(f"Project Status   : {progress['project_status']} (Weight: 10%, Contrib: {progress['project_contrib']})")

        prac = self.get_practice_summary(student.student_id)
        lines.append(f"Practice Conducted: {prac['conducted']} sessions")
        lines.append(f"Practice Attended : {prac['attended']} sessions")
        lines.append(f"Participation Rate: {prac['percentage']}% (Weight: 10%, Contrib: {progress['practice_contrib']})")

        lines.append(f"Mock Interview   : {progress['mock_status']} (Weight: 10%, Contrib: {progress['mock_contrib']})")
        lines.append("")

        lines.append("5. OVERALL PROGRESS & EVALUATION")
        lines.append("-" * 40)
        lines.append(f"Overall Progress : {progress['overall_progress']}%")
        lines.append(f"Performance Class: {progress['category']}")
        lines.append("")

        lines.append("6. PLACEMENT ELIGIBILITY STATUS")
        lines.append("-" * 40)
        if is_eligible:
            lines.append("STATUS: >>> ELIGIBLE FOR PLACEMENTS <<<")
            lines.append("Congratulations! All placement criteria have been met.")
        else:
            lines.append("STATUS: >>> NOT CURRENTLY ELIGIBLE <<<")
            lines.append("Reasons for Ineligibility:")
            for idx, reason in enumerate(reasons, start=1):
                lines.append(f"  {idx}. {reason}")
        lines.append("=" * 65)

        report_content = "\n".join(lines)
        filename = f"student_report_{student.student_id}.txt"
        saved_path = self.file_manager.write_report_file(filename, report_content)
        return saved_path, report_content

    def generate_overall_report(self):
        """
        Generates an institute-wide summary report.
        Saves report into reports/overall_placement_report.txt.
        """
        all_students = self.get_all_students()
        all_batches = self.get_all_batches()

        total_students = len(all_students)
        total_batches = len(all_batches)

        eligible_count = 0
        ineligible_count = 0
        categories_count = {
            "Excellent": 0,
            "Good": 0,
            "Average": 0,
            "Needs Improvement": 0,
        }

        total_progress_sum = 0.0
        student_summaries = []

        for student in all_students:
            prog = self.calculate_overall_progress(student.student_id)
            is_eligible, reasons = self.check_placement_eligibility(student.student_id)

            if is_eligible:
                eligible_count += 1
            else:
                ineligible_count += 1

            cat = prog["category"]
            categories_count[cat] = categories_count.get(cat, 0) + 1

            total_progress_sum += prog["overall_progress"]

            student_summaries.append({
                "student_id": student.student_id,
                "name": student.name,
                "batch": student.batch_id,
                "progress": prog["overall_progress"],
                "category": cat,
                "eligible": "Eligible" if is_eligible else "Not Eligible",
            })

        avg_progress = (
            round(total_progress_sum / total_students, 2)
            if total_students > 0
            else 0.0
        )

        # Top performers
        top_performers = self.get_top_performers(limit=5)

        # Format overall report
        lines = []
        lines.append("=" * 75)
        lines.append("         INSTITUTE PLACEMENT READINESS SUMMARY REPORT")
        lines.append("=" * 75)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        lines.append("1. EXECUTIVE SUMMARY")
        lines.append("-" * 45)
        lines.append(f"Total Registered Students     : {total_students}")
        lines.append(f"Total Batches                 : {total_batches}")
        lines.append(f"Placement Eligible Students   : {eligible_count} ({calculate_percentage(eligible_count, total_students)}%)")
        lines.append(f"Ineligible Students           : {ineligible_count} ({calculate_percentage(ineligible_count, total_students)}%)")
        lines.append(f"Institute Average Progress    : {avg_progress}%")
        lines.append("")

        lines.append("2. PERFORMANCE CATEGORY DISTRIBUTION")
        lines.append("-" * 45)
        for cat, count in categories_count.items():
            pct = calculate_percentage(count, total_students)
            lines.append(f"  {cat:<20}: {count:>3} students ({pct}%)")
        lines.append("")

        lines.append("3. TOP 5 PERFORMERS")
        lines.append("-" * 75)
        lines.append(f"{'Rank':<6}{'ID':<10}{'Name':<22}{'Batch':<14}{'Progress':<12}{'Category'}")
        lines.append("-" * 75)
        for idx, tp in enumerate(top_performers, start=1):
            lines.append(
                f"{idx:<6}{tp['student_id']:<10}{tp['student_name']:<22}{tp['batch_id']:<14}{tp['overall_progress']:<12}{tp['category']}"
            )
        lines.append("")

        lines.append("4. COMPLETE STUDENT ROSTER")
        lines.append("-" * 75)
        lines.append(f"{'ID':<10}{'Name':<22}{'Batch':<14}{'Progress':<12}{'Category':<18}{'Eligibility'}")
        lines.append("-" * 75)
        for s in student_summaries:
            lines.append(
                f"{s['student_id']:<10}{s['name']:<22}{s['batch']:<14}{s['progress']:<12}{s['category']:<18}{s['eligible']}"
            )
        lines.append("=" * 75)

        report_content = "\n".join(lines)
        filename = "overall_placement_report.txt"
        saved_path = self.file_manager.write_report_file(filename, report_content)
        return saved_path, report_content
