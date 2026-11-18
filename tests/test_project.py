"""
tests/test_project.py - Unit Test Suite
Project: Placement Readiness and Student Progress Management System
Batch: DA-VSP-006

Demonstrates:
- Built-in unittest module
- Isolated tests using tempfile.TemporaryDirectory
- Data integrity, validation, calculations, OOP, and persistence verification
"""

import os
import unittest
import tempfile
import json

from models import Person, Student, Batch
from manager import PlacementManager
from utils import (
    calculate_average,
    format_details_card,
    format_table_row,
    calculate_percentage,
    validate_score,
    validate_date,
    validate_email,
    validate_phone,
)


class TestProjectSuite(unittest.TestCase):
    """
    Comprehensive test suite running in an isolated temporary directory.
    Never modifies real data files.
    """

    def setUp(self):
        # Create temporary directories for data and reports
        self.test_dir = tempfile.TemporaryDirectory()
        self.data_dir = os.path.join(self.test_dir.name, "data")
        self.reports_dir = os.path.join(self.test_dir.name, "reports")

        # Initialize manager with temporary folders
        self.manager = PlacementManager(data_dir=self.data_dir, reports_dir=self.reports_dir)

        # Seed a test batch
        self.batch = self.manager.create_batch(
            batch_id="TEST-001",
            batch_name="Test Batch Name",
            course_name="Python Testing"
        )

    def tearDown(self):
        # Clean up temporary directory
        self.test_dir.cleanup()

    # ==========================================
    # 1. OOP CONCEPTS & ENCAPSULATION / POLYMORPHISM
    # ==========================================

    def test_person_encapsulation(self):
        """Test private __email attribute and validation in getter/setter."""
        p = Person("Rahul Sharma", "rahul@example.com", "9876543210")
        self.assertEqual(p.name, "Rahul Sharma")
        self.assertEqual(p.email, "rahul@example.com")
        self.assertEqual(p.get_email(), "rahul@example.com")

        # Update via setter
        p.email = "new.email@example.com"
        self.assertEqual(p.email, "new.email@example.com")

        # Reject invalid email format
        with self.assertRaises(ValueError):
            p.email = "invalid-email"

    def test_student_inheritance_and_polymorphism(self):
        """Test Student inheriting Person and overriding display_details."""
        s = Student("ST100", "Pooja Patel", "pooja@example.com", "9123456789", "TEST-001")
        self.assertIsInstance(s, Person)
        self.assertEqual(s.student_id, "ST100")
        self.assertEqual(s.batch_id, "TEST-001")

        # Test polymorphic output
        details = s.display_details()
        self.assertIn("ST100", details)
        self.assertIn("Pooja Patel", details)
        self.assertIn("TEST-001", details)

    # ==========================================
    # 2. UTILITY & *ARGS / **KWARGS DEMONSTRATIONS
    # ==========================================

    def test_args_calculate_average(self):
        """Test *args helper with varying number of arguments."""
        self.assertEqual(calculate_average(10, 20, 30), 20.0)
        self.assertEqual(calculate_average(85.5, 90.5), 88.0)
        self.assertEqual(calculate_average(), 0.0)
        # Ignores None
        self.assertEqual(calculate_average(100, None, 50), 75.0)

    def test_kwargs_format_details_card(self):
        """Test **kwargs helper formatting arbitrary key-values."""
        card = format_details_card("Student Info", name="Kiran", score=95, status=None)
        self.assertIn("STUDENT INFO", card)
        self.assertIn("Name", card)
        self.assertIn("Kiran", card)
        self.assertIn("Not Entered", card)

    def test_format_table_row(self):
        """Test *args table formatter."""
        row = format_table_row("Col1", "Col2", 100, width=10)
        self.assertIn("Col1", row)
        self.assertIn("100", row)

    # ==========================================
    # 3. STUDENT REGISTRATION & VALIDATION
    # ==========================================

    def test_student_registration_success(self):
        """Test registering a valid student."""
        student = self.manager.register_student(
            name="Amit Kumar",
            email="amit@example.com",
            phone="9876543210",
            batch_id="TEST-001"
        )
        self.assertEqual(student.name, "Amit Kumar")
        self.assertEqual(student.email, "amit@example.com")
        self.assertEqual(student.batch_id, "TEST-001")
        self.assertTrue(student.student_id.startswith("ST"))

    def test_duplicate_student_id_prevention(self):
        """Test that registering a duplicate student ID is rejected."""
        self.manager.register_student(
            name="Student 1",
            email="s1@example.com",
            phone="9876543210",
            batch_id="TEST-001",
            student_id="ST999"
        )
        with self.assertRaises(ValueError) as ctx:
            self.manager.register_student(
                name="Student 2",
                email="s2@example.com",
                phone="9876543211",
                batch_id="TEST-001",
                student_id="ST999"
            )
        self.assertIn("already registered", str(ctx.exception))

    def test_duplicate_email_prevention(self):
        """Test that registering a duplicate email address is rejected."""
        self.manager.register_student(
            name="Student A",
            email="common@example.com",
            phone="9876543210",
            batch_id="TEST-001"
        )
        with self.assertRaises(ValueError) as ctx:
            self.manager.register_student(
                name="Student B",
                email="COMMON@example.com",  # Case-insensitive
                phone="9876543211",
                batch_id="TEST-001"
            )
        self.assertIn("already registered", str(ctx.exception))

    def test_invalid_batch_rejection(self):
        """Test assigning a student to a non-existent batch."""
        with self.assertRaises(ValueError) as ctx:
            self.manager.register_student(
                name="Student C",
                email="c@example.com",
                phone="9876543210",
                batch_id="NON-EXISTENT"
            )
        self.assertIn("does not exist", str(ctx.exception))

    def test_invalid_phone_and_name_rejection(self):
        """Test invalid phone numbers and empty names."""
        with self.assertRaises(ValueError):
            self.manager.register_student(
                name="   ",  # Blank name
                email="blank@example.com",
                phone="9876543210",
                batch_id="TEST-001"
            )
        with self.assertRaises(ValueError):
            self.manager.register_student(
                name="Valid Name",
                email="valid@example.com",
                phone="12345",  # Less than 10 digits
                batch_id="TEST-001"
            )

    def test_update_student_details(self):
        """Test updating student details without modifying student ID."""
        s = self.manager.register_student("Initial Name", "initial@example.com", "9876543210", "TEST-001")
        original_id = s.student_id

        updated = self.manager.update_student(original_id, name="Updated Name", phone="9998887776")
        self.assertEqual(updated.student_id, original_id)
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.phone, "9998887776")

    # ==========================================
    # 4. BATCH CREATION & RETRIEVAL
    # ==========================================

    def test_duplicate_batch_rejection(self):
        """Test creating a duplicate batch ID."""
        with self.assertRaises(ValueError) as ctx:
            self.manager.create_batch("TEST-001", "Another Name", "Course")
        self.assertIn("already exists", str(ctx.exception))

    # ==========================================
    # 5. ATTENDANCE TRACKING & CALCULATION
    # ==========================================

    def test_attendance_tracking_and_percentage(self):
        """Test recording attendance and formula: (Present / Total) * 100."""
        s = self.manager.register_student("Att Student", "att@example.com", "9876543210", "TEST-001")

        self.manager.record_attendance(s.student_id, "2026-11-01", "Present")
        self.manager.record_attendance(s.student_id, "2026-11-02", "Present")
        self.manager.record_attendance(s.student_id, "2026-11-03", "Present")
        self.manager.record_attendance(s.student_id, "2026-11-04", "Absent")

        summary = self.manager.get_attendance_summary(s.student_id)
        self.assertEqual(summary["total_days"], 4)
        self.assertEqual(summary["present_days"], 3)
        self.assertEqual(summary["absent_days"], 1)
        self.assertEqual(summary["percentage"], 75.0)

    def test_attendance_zero_days(self):
        """Test attendance percentage returns 0.0 when no days are recorded."""
        s = self.manager.register_student("Zero Days", "zero@example.com", "9876543210", "TEST-001")
        summary = self.manager.get_attendance_summary(s.student_id)
        self.assertEqual(summary["percentage"], 0.0)
        self.assertFalse(summary["has_records"])

    def test_duplicate_attendance_date_rejection(self):
        """Test duplicate attendance entry on the same date for the same student."""
        s = self.manager.register_student("Dup Att", "dup@example.com", "9876543210", "TEST-001")
        self.manager.record_attendance(s.student_id, "2026-11-01", "Present")
        with self.assertRaises(ValueError) as ctx:
            self.manager.record_attendance(s.student_id, "2026-11-01", "Absent")
        self.assertIn("already recorded", str(ctx.exception))

    def test_invalid_attendance_date_format(self):
        """Test invalid date formats."""
        s = self.manager.register_student("Inv Date", "invdate@example.com", "9876543210", "TEST-001")
        with self.assertRaises(ValueError):
            self.manager.record_attendance(s.student_id, "01-11-2026", "Present")

    # ==========================================
    # 6. ASSESSMENTS & SCORE VALIDATION
    # ==========================================

    def test_python_assessment_average(self):
        """Test Python assessment average calculation."""
        s = self.manager.register_student("Py Student", "py@example.com", "9876543210", "TEST-001")
        self.manager.add_python_assessment(s.student_id, "A1", 80)
        self.manager.add_python_assessment(s.student_id, "A2", 90)

        summary = self.manager.get_python_assessment_summary(s.student_id)
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["average"], 85.0)

    def test_duplicate_assessment_id_rejection(self):
        """Test preventing duplicate assessment ID for the same student."""
        s = self.manager.register_student("Dup Assess", "dupass@example.com", "9876543210", "TEST-001")
        self.manager.add_python_assessment(s.student_id, "A1", 80)
        with self.assertRaises(ValueError):
            self.manager.add_python_assessment(s.student_id, "A1", 90)

    def test_invalid_score_rejection(self):
        """Test scores outside 0-100 or non-numeric."""
        s = self.manager.register_student("Score Val", "score@example.com", "9876543210", "TEST-001")
        with self.assertRaises(ValueError):
            self.manager.add_python_assessment(s.student_id, "A1", 105)
        with self.assertRaises(ValueError):
            self.manager.add_python_assessment(s.student_id, "A2", -5)
        with self.assertRaises(ValueError):
            self.manager.add_python_assessment(s.student_id, "A3", "abc")

    def test_technical_scores_missing_vs_zero(self):
        """Test that missing scores remain None and are distinct from 0."""
        s = self.manager.register_student("Tech Student", "tech@example.com", "9876543210", "TEST-001")
        # Update only SQL
        self.manager.update_technical_scores(s.student_id, sql_score=0.0)

        details = self.manager.get_assessment_details(s.student_id)
        self.assertEqual(details["sql_score"], 0.0)
        self.assertIsNone(details["excel_score"])
        self.assertIsNone(details["powerbi_score"])

    # ==========================================
    # 7. PRACTICE SESSIONS TRACKING
    # ==========================================

    def test_practice_sessions_calculation(self):
        """Test practice participation calculation."""
        s = self.manager.register_student("Prac Student", "prac@example.com", "9876543210", "TEST-001")
        self.manager.update_practice_sessions(s.student_id, conducted=20, attended=15)

        summary = self.manager.get_practice_summary(s.student_id)
        self.assertEqual(summary["conducted"], 20)
        self.assertEqual(summary["attended"], 15)
        self.assertEqual(summary["percentage"], 75.0)

    def test_practice_invalid_inputs(self):
        """Test rejection of negative numbers or attended > conducted."""
        s = self.manager.register_student("Prac Inv", "pracinv@example.com", "9876543210", "TEST-001")
        with self.assertRaises(ValueError):
            self.manager.update_practice_sessions(s.student_id, conducted=-10, attended=5)
        with self.assertRaises(ValueError):
            self.manager.update_practice_sessions(s.student_id, conducted=10, attended=15)

    # ==========================================
    # 8. OVERALL PROGRESS & PLACEMENT ELIGIBILITY
    # ==========================================

    def test_overall_progress_calculation(self):
        """
        Verify exact weighted overall progress calculation:
        Attendance (20%) + Python (20%) + SQL (10%) + Excel (10%) +
        Power BI (10%) + Project (10%) + Practice (10%) + Mock (10%)
        """
        s = self.manager.register_student("Prog Student", "prog@example.com", "9876543210", "TEST-001")

        # 1. Attendance: 100% -> Contrib: 20.0
        self.manager.record_attendance(s.student_id, "2026-11-01", "Present")
        # 2. Python: 80% -> Contrib: 16.0
        self.manager.add_python_assessment(s.student_id, "P1", 80.0)
        # 3, 4, 5. SQL: 80 (8.0), Excel: 80 (8.0), Power BI: 80 (8.0)
        self.manager.update_technical_scores(s.student_id, sql_score=80.0, excel_score=80.0, powerbi_score=80.0)
        # 6. Project: Completed (100) -> Contrib: 10.0
        self.manager.update_project_status(s.student_id, "Completed")
        # 7. Practice: 80% -> Contrib: 8.0
        self.manager.update_practice_sessions(s.student_id, conducted=10, attended=8)
        # 8. Mock: Passed (100) -> Contrib: 10.0
        self.manager.update_mock_interview_status(s.student_id, "Passed")

        res = self.manager.calculate_overall_progress(s.student_id)
        # Expected: 20 + 16 + 8 + 8 + 8 + 10 + 8 + 10 = 88.00%
        self.assertEqual(res["overall_progress"], 88.0)
        self.assertEqual(res["category"], "Excellent")

    def test_placement_eligibility_passed(self):
        """Test a student who meets all 8 placement conditions."""
        s = self.manager.register_student("Eligible Student", "el@example.com", "9876543210", "TEST-001")

        self.manager.record_attendance(s.student_id, "2026-11-01", "Present")  # 100%
        self.manager.add_python_assessment(s.student_id, "P1", 75.0)  # 75%
        self.manager.update_technical_scores(s.student_id, sql_score=70.0, excel_score=70.0, powerbi_score=70.0)
        self.manager.update_project_status(s.student_id, "Completed")
        self.manager.update_practice_sessions(s.student_id, conducted=10, attended=8)  # 80%
        self.manager.update_mock_interview_status(s.student_id, "Passed")

        is_eligible, reasons = self.manager.check_placement_eligibility(s.student_id)
        self.assertTrue(is_eligible)
        self.assertEqual(len(reasons), 0)

    def test_placement_ineligible_reasons(self):
        """Test an ineligible student and verify that specific reasons are returned."""
        s = self.manager.register_student("Ineligible Student", "inel@example.com", "9876543210", "TEST-001")

        # Attendance: 50% (< 75%)
        self.manager.record_attendance(s.student_id, "2026-11-01", "Present")
        self.manager.record_attendance(s.student_id, "2026-11-02", "Absent")

        # Python: 50% (< 60%)
        self.manager.add_python_assessment(s.student_id, "P1", 50.0)

        # SQL: 55 (< 60), Excel missing, Power BI missing
        self.manager.update_technical_scores(s.student_id, sql_score=55.0)

        # Project: In Progress
        self.manager.update_project_status(s.student_id, "In Progress")

        # Practice: 50% (< 70%)
        self.manager.update_practice_sessions(s.student_id, conducted=10, attended=5)

        # Mock: Attended (!= Passed)
        self.manager.update_mock_interview_status(s.student_id, "Attended")

        is_eligible, reasons = self.manager.check_placement_eligibility(s.student_id)
        self.assertFalse(is_eligible)

        reasons_text = " ".join(reasons)
        self.assertIn("Attendance is 50.0%", reasons_text)
        self.assertIn("Python assessment average is 50.0%", reasons_text)
        self.assertIn("SQL score is 55.0", reasons_text)
        self.assertIn("Excel score has not been entered", reasons_text)
        self.assertIn("Power BI score has not been entered", reasons_text)
        self.assertIn("Project status is 'In Progress'", reasons_text)
        self.assertIn("Practice participation is 50.0%", reasons_text)
        self.assertIn("Mock interview status is 'Attended'", reasons_text)

    # ==========================================
    # 9. SEARCH, RANKINGS, & REPORTS
    # ==========================================

    def test_student_search(self):
        """Test case-insensitive search by name, id, and batch."""
        s = self.manager.register_student("Ramesh Kumar", "ramesh@example.com", "9876543210", "TEST-001")

        # By Name
        res_name = self.manager.search_students("ramesh", search_type="name")
        self.assertEqual(len(res_name), 1)
        self.assertEqual(res_name[0].student_id, s.student_id)

        # By ID
        res_id = self.manager.search_students(s.student_id.lower(), search_type="id")
        self.assertEqual(len(res_id), 1)

        # By Batch
        res_batch = self.manager.search_students("test-001", search_type="batch")
        self.assertEqual(len(res_batch), 1)

    def test_top_performers_ranking(self):
        """Test sorting of top performers by overall progress descending."""
        s1 = self.manager.register_student("Student Low", "low@example.com", "9876543210", "TEST-001")
        s2 = self.manager.register_student("Student High", "high@example.com", "9876543211", "TEST-001")

        # High student gets 100% on everything
        self.manager.record_attendance(s2.student_id, "2026-11-01", "Present")
        self.manager.add_python_assessment(s2.student_id, "P1", 100.0)
        self.manager.update_technical_scores(s2.student_id, sql_score=100.0, excel_score=100.0, powerbi_score=100.0)
        self.manager.update_project_status(s2.student_id, "Completed")
        self.manager.update_practice_sessions(s2.student_id, conducted=10, attended=10)
        self.manager.update_mock_interview_status(s2.student_id, "Passed")

        top = self.manager.get_top_performers(limit=5)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]["student_id"], s2.student_id)
        self.assertEqual(top[0]["overall_progress"], 100.0)
        self.assertEqual(top[1]["student_id"], s1.student_id)

    def test_report_generation(self):
        """Test generating student report and overall report."""
        s = self.manager.register_student("Report User", "rep@example.com", "9876543210", "TEST-001")

        # Generate individual report
        student_rep_path, content = self.manager.generate_student_report(s.student_id)
        self.assertTrue(os.path.exists(student_rep_path))
        self.assertIn("STUDENT PROGRESS AND PLACEMENT READINESS REPORT", content)
        self.assertIn(s.student_id, content)

        # Generate overall report
        overall_path, overall_content = self.manager.generate_overall_report()
        self.assertTrue(os.path.exists(overall_path))
        self.assertIn("INSTITUTE PLACEMENT READINESS SUMMARY REPORT", overall_content)

    # ==========================================
    # 10. PERSISTENCE & CORRUPTED DATA PROTECTION
    # ==========================================

    def test_txt_persistence_after_restart(self):
        """Test that data written by one manager instance is loaded by a new instance."""
        s = self.manager.register_student("Persist Student", "persist@example.com", "9876543210", "TEST-001")
        self.manager.record_attendance(s.student_id, "2026-11-01", "Present")

        # Create a brand new manager instance pointing to the same data directory
        new_manager = PlacementManager(data_dir=self.data_dir, reports_dir=self.reports_dir)
        loaded_student = new_manager.get_student_by_id(s.student_id)

        self.assertIsNotNone(loaded_student)
        self.assertEqual(loaded_student.name, "Persist Student")
        self.assertEqual(loaded_student.email, "persist@example.com")

        att = new_manager.get_attendance_summary(s.student_id)
        self.assertEqual(att["total_days"], 1)
        self.assertEqual(att["percentage"], 100.0)

    def test_corrupted_data_handling(self):
        """Test that corrupted JSON in a TXT file raises ValueError and is not silently overwritten."""
        corrupted_file = os.path.join(self.data_dir, "students.txt")
        with open(corrupted_file, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON TEXT ::::")

        with self.assertRaises(ValueError) as ctx:
            self.manager.get_all_students()
        self.assertIn("corrupted JSON", str(ctx.exception))

        # Verify corrupted content was not overwritten
        with open(corrupted_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("INVALID JSON", content)


if __name__ == "__main__":
    unittest.main()
