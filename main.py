"""
main.py - Console Menu Interface
Project: Placement Readiness and Student Progress Management System
Batch: DA-VSP-006

Demonstrates:
- Menu-driven console interface
- While loop for continuous menu execution
- if-elif-else statements for routing choices
- User input validation and friendly error handling
- Built-in modules (sys, datetime)
"""

import sys
from datetime import datetime
from manager import PlacementManager


def print_header(title):
    """Prints a styled section header."""
    print("\n" + "=" * 55)
    print(f" {title.upper()}")
    print("=" * 55)


def print_menu():
    """Displays the main 18-option application menu."""
    print("\n========== PLACEMENT READINESS SYSTEM ==========")
    print(" 1. Register Student")
    print(" 2. Create Batch")
    print(" 3. View Students")
    print(" 4. Record Attendance")
    print(" 5. Enter Python Assessment")
    print(" 6. Enter SQL / Excel / Power BI Scores")
    print(" 7. Update Project Status")
    print(" 8. Update Practice Sessions")
    print(" 9. Update Mock Interview Status")
    print("10. Search Student")
    print("11. View Student Progress")
    print("12. Check Placement Eligibility")
    print("13. View Top Performers")
    print("14. View Students Needing Improvement")
    print("15. Generate Student Report")
    print("16. Generate Overall Report")
    print("17. Update Student Details")
    print("18. View Batch Students")
    print(" 0. Exit")
    print("================================================")


# ==========================================
# MENU HANDLER FUNCTIONS
# ==========================================

def handle_register_student(manager):
    print_header("Register New Student")
    batches = manager.get_all_batches()
    if not batches:
        print("[Notice] No batches found. Please create a batch first (Option 2).")
        return

    print("Available Batches:")
    for b in batches:
        print(f"  - {b.batch_id} ({b.batch_name})")

    name = input("\nEnter Student Full Name: ").strip()
    email = input("Enter Student Email: ").strip()
    phone = input("Enter 10-digit Phone Number: ").strip()
    batch_id = input("Enter Batch ID: ").strip().upper()

    try:
        student = manager.register_student(name=name, email=email, phone=phone, batch_id=batch_id)
        print("\n[Success] Student registered successfully!")
        print(f"  Student ID : {student.student_id}")
        print(f"  Name       : {student.name}")
        print(f"  Email      : {student.email}")
        print(f"  Phone      : {student.phone}")
        print(f"  Batch      : {student.batch_id}")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_create_batch(manager):
    print_header("Create Training Batch")
    batch_id = input("Enter Batch ID (e.g., DA-VSP-006): ").strip().upper()
    batch_name = input("Enter Batch Name: ").strip()
    course_name = input("Enter Course Name: ").strip()

    try:
        batch = manager.create_batch(batch_id=batch_id, batch_name=batch_name, course_name=course_name)
        print("\n[Success] Batch created successfully!")
        print(f"  Batch ID   : {batch.batch_id}")
        print(f"  Batch Name : {batch.batch_name}")
        print(f"  Course     : {batch.course_name}")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_view_students(manager):
    print_header("Registered Students Roster")
    students = manager.get_all_students()
    if not students:
        print("No students registered yet.")
        return

    print(f"{'ID':<8} | {'Name':<20} | {'Batch':<12} | {'Email':<25} | {'Phone'}")
    print("-" * 80)
    for s in students:
        print(f"{s.student_id:<8} | {s.name:<20} | {s.batch_id:<12} | {s.email:<25} | {s.phone}")
    print("-" * 80)
    print(f"Total Students: {len(students)}")


def handle_record_attendance(manager):
    print_header("Record Attendance")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    print(f"Student: {student.name} ({student.student_id}) | Batch: {student.batch_id}")
    today_str = datetime.now().strftime("%Y-%m-%d")
    date_input = input(f"Enter Attendance Date (YYYY-MM-DD) [Default: {today_str}]: ").strip()
    record_date = date_input if date_input else today_str

    print("Attendance Options:")
    print("  1. Present")
    print("  2. Absent")
    choice = input("Enter choice (1 or 2): ").strip()
    if choice == "1":
        status = "Present"
    elif choice == "2":
        status = "Absent"
    else:
        status = choice

    try:
        manager.record_attendance(student_id=student_id, date_str=record_date, status=status)
        summary = manager.get_attendance_summary(student_id)
        print("\n[Success] Attendance recorded successfully!")
        print(f"  Date       : {record_date}")
        print(f"  Status     : {status}")
        print(f"  Attendance : {summary['present_days']}/{summary['total_days']} days ({summary['percentage']}%)")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_enter_python_assessment(manager):
    print_header("Enter Python Assessment Score")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    print(f"Student: {student.name} ({student.student_id})")
    py_summary = manager.get_python_assessment_summary(student_id)
    if py_summary["has_records"]:
        print(f"Existing Assessments: {py_summary['scores']} (Average: {py_summary['average']}%)")

    assessment_id = input("Enter Assessment ID (e.g., PY01, Quiz1): ").strip().upper()
    score_input = input("Enter Score (0 - 100): ").strip()

    try:
        manager.add_python_assessment(student_id=student_id, assessment_id=assessment_id, score=score_input)
        updated_summary = manager.get_python_assessment_summary(student_id)
        print("\n[Success] Python assessment score recorded successfully!")
        print(f"  Assessment ID : {assessment_id}")
        print(f"  Score Recorded: {float(score_input)}")
        print(f"  New Python Avg: {updated_summary['average']}% across {updated_summary['count']} assessment(s)")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_enter_technical_scores(manager):
    print_header("Enter SQL / Excel / Power BI Scores")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    assess_data = manager.get_assessment_details(student_id)
    print(f"Student: {student.name} ({student.student_id})")
    print("Current Scores:")
    print(f"  SQL      : {'Not Entered' if assess_data.get('sql_score') is None else assess_data.get('sql_score')}")
    print(f"  Excel    : {'Not Entered' if assess_data.get('excel_score') is None else assess_data.get('excel_score')}")
    print(f"  Power BI : {'Not Entered' if assess_data.get('powerbi_score') is None else assess_data.get('powerbi_score')}")

    print("\n(Press Enter to leave a score unchanged)")
    sql_input = input("Enter SQL Score (0-100): ").strip()
    excel_input = input("Enter Excel Score (0-100): ").strip()
    pbi_input = input("Enter Power BI Score (0-100): ").strip()

    sql_val = float(sql_input) if sql_input else None
    excel_val = float(excel_input) if excel_input else None
    pbi_val = float(pbi_input) if pbi_input else None

    try:
        manager.update_technical_scores(
            student_id=student_id,
            sql_score=sql_val,
            excel_score=excel_val,
            powerbi_score=pbi_val
        )
        updated = manager.get_assessment_details(student_id)
        print("\n[Success] Technical scores updated successfully!")
        print(f"  SQL      : {'Not Entered' if updated.get('sql_score') is None else updated.get('sql_score')}")
        print(f"  Excel    : {'Not Entered' if updated.get('excel_score') is None else updated.get('excel_score')}")
        print(f"  Power BI : {'Not Entered' if updated.get('powerbi_score') is None else updated.get('powerbi_score')}")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_update_project_status(manager):
    print_header("Update Project Status")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    assess = manager.get_assessment_details(student_id)
    print(f"Student: {student.name} | Current Project Status: {assess.get('project_status', 'Not Started')}")
    print("\nSelect New Status:")
    print("  1. Not Started")
    print("  2. In Progress")
    print("  3. Completed")

    choice = input("Enter choice (1-3): ").strip()
    status_map = {"1": "Not Started", "2": "In Progress", "3": "Completed"}
    status = status_map.get(choice, choice)

    try:
        new_status = manager.update_project_status(student_id, status)
        print(f"\n[Success] Project status updated to: '{new_status}'")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_update_practice_sessions(manager):
    print_header("Update Practice Sessions")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    current = manager.get_practice_summary(student_id)
    print(f"Student: {student.name} | Current Practice: {current['attended']}/{current['conducted']} sessions ({current['percentage']}%)")

    cond_input = input("Enter Total Sessions Conducted: ").strip()
    att_input = input("Enter Sessions Attended: ").strip()

    try:
        manager.update_practice_sessions(student_id, conducted=cond_input, attended=att_input)
        updated = manager.get_practice_summary(student_id)
        print("\n[Success] Practice sessions updated successfully!")
        print(f"  Conducted    : {updated['conducted']}")
        print(f"  Attended     : {updated['attended']}")
        print(f"  Participation: {updated['percentage']}%")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_update_mock_interview(manager):
    print_header("Update Mock Interview Status")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    current_status = manager.get_mock_interview_status(student_id)
    print(f"Student: {student.name} | Current Status: {current_status}")
    print("\nSelect New Status:")
    print("  1. Not Attended")
    print("  2. Attended")
    print("  3. Passed")

    choice = input("Enter choice (1-3): ").strip()
    status_map = {"1": "Not Attended", "2": "Attended", "3": "Passed"}
    status = status_map.get(choice, choice)

    try:
        new_status = manager.update_mock_interview_status(student_id, status)
        print(f"\n[Success] Mock interview status updated to: '{new_status}'")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_search_student(manager):
    print_header("Search Student Records")
    print("Search by:")
    print("  1. Student ID")
    print("  2. Student Name")
    print("  3. Batch ID")

    choice = input("Enter choice (1-3): ").strip()
    type_map = {"1": "id", "2": "name", "3": "batch"}
    search_type = type_map.get(choice)
    if not search_type:
        print("[Error] Invalid search option selected.")
        return

    query = input("Enter search term: ").strip()
    if not query:
        print("[Error] Search term cannot be empty.")
        return

    try:
        results = manager.search_students(query, search_type=search_type)
        if not results:
            print(f"\nNo students found matching '{query}'.")
            return

        print(f"\nFound {len(results)} matching student(s):")
        print(f"{'ID':<8} | {'Name':<20} | {'Batch':<12} | {'Email':<25} | {'Phone'}")
        print("-" * 80)
        for s in results:
            print(f"{s.student_id:<8} | {s.name:<20} | {s.batch_id:<12} | {s.email:<25} | {s.phone}")
        print("-" * 80)
    except ValueError as e:
        print(f"\n[Error] {e}")


def handle_view_student_progress(manager):
    print_header("View Student Progress Breakdown")
    student_id = input("Enter Student ID: ").strip().upper()
    try:
        p = manager.calculate_overall_progress(student_id)
        print("\n" + "=" * 60)
        print(f" PROGRESS SUMMARY FOR: {p['student_name']} ({p['student_id']})")
        print(f" Batch: {p['batch_id']}")
        print("=" * 60)

        # Attendance
        att_status = f"{p['attendance_pct']}%" if p['attendance_recorded'] else "Not Entered (0%)"
        print(f" 1. Attendance (20%)          : {att_status:<18} -> Contribution: {p['attendance_contrib']:>5.2f}%")

        # Python
        py_status = f"{p['python_avg']}%" if p['python_recorded'] else "Not Taken (0%)"
        print(f" 2. Python Assessment (20%)   : {py_status:<18} -> Contribution: {p['python_contrib']:>5.2f}%")

        # SQL
        sql_status = f"{p['sql_score']}/100" if p['sql_score'] is not None else "Not Entered (0)"
        print(f" 3. SQL Score (10%)           : {sql_status:<18} -> Contribution: {p['sql_contrib']:>5.2f}%")

        # Excel
        excel_status = f"{p['excel_score']}/100" if p['excel_score'] is not None else "Not Entered (0)"
        print(f" 4. Excel Score (10%)         : {excel_status:<18} -> Contribution: {p['excel_contrib']:>5.2f}%")

        # Power BI
        pbi_status = f"{p['powerbi_score']}/100" if p['powerbi_score'] is not None else "Not Entered (0)"
        print(f" 5. Power BI Score (10%)      : {pbi_status:<18} -> Contribution: {p['powerbi_contrib']:>5.2f}%")

        # Project
        print(f" 6. Project Status (10%)      : {p['project_status']:<18} -> Contribution: {p['project_contrib']:>5.2f}%")

        # Practice
        prac_status = f"{p['practice_pct']}%" if p['practice_recorded'] else "Not Conducted (0%)"
        print(f" 7. Practice Sessions (10%)   : {prac_status:<18} -> Contribution: {p['practice_contrib']:>5.2f}%")

        # Mock Interview
        print(f" 8. Mock Interview (10%)      : {p['mock_status']:<18} -> Contribution: {p['mock_contrib']:>5.2f}%")
        print("-" * 60)
        print(f" OVERALL PROGRESS             : {p['overall_progress']:>6.2f}%")
        print(f" PERFORMANCE CATEGORY         : {p['category']}")
        print("=" * 60)
    except ValueError as e:
        print(f"\n[Error] {e}")


def handle_check_placement_eligibility(manager):
    print_header("Check Placement Eligibility")
    student_id = input("Enter Student ID: ").strip().upper()
    try:
        student = manager.get_student_by_id(student_id)
        if not student:
            print(f"[Error] Student '{student_id}' does not exist.")
            return

        is_eligible, reasons = manager.check_placement_eligibility(student_id)
        prog = manager.calculate_overall_progress(student_id)

        print("\n" + "=" * 55)
        print(f" Student ID : {student.student_id}")
        print(f" Name       : {student.name}")
        print(f" Batch      : {student.batch_id}")
        print(f" Progress   : {prog['overall_progress']}% ({prog['category']})")
        print("-" * 55)

        if is_eligible:
            print(" PLACEMENT STATUS: >>> ELIGIBLE <<<")
            print(" All mandatory conditions are satisfied!")
        else:
            print(" PLACEMENT STATUS: >>> NOT ELIGIBLE <<<")
            print("\n Ineligibility Reasons:")
            for idx, r in enumerate(reasons, start=1):
                print(f"   {idx}. {r}")
        print("=" * 55)
    except ValueError as e:
        print(f"\n[Error] {e}")


def handle_view_top_performers(manager):
    print_header("Top Performers Ranking")
    top_list = manager.get_top_performers(limit=5)
    if not top_list:
        print("No student records available.")
        return

    print(f"{'Rank':<6} | {'ID':<8} | {'Name':<20} | {'Batch':<12} | {'Progress':<10} | {'Category'}")
    print("-" * 75)
    for idx, s in enumerate(top_list, start=1):
        print(f"{idx:<6} | {s['student_id']:<8} | {s['student_name']:<20} | {s['batch_id']:<12} | {s['overall_progress']:>6.2f}%   | {s['category']}")
    print("-" * 75)


def handle_view_students_needing_improvement(manager):
    print_header("Students Needing Improvement")
    improvement_list = manager.get_students_needing_improvement()
    if not improvement_list:
        print("No students currently flagged as needing improvement.")
        return

    print(f"Found {len(improvement_list)} student(s) requiring attention:\n")
    for s in improvement_list:
        print(f"• [{s['student_id']}] {s['student_name']} (Batch: {s['batch_id']})")
        print(f"  Overall Progress: {s['overall_progress']}% | Category: {s['category']}")
        print("  Identified Issues:")
        for r in s['reasons']:
            print(f"    - {r}")
        print("-" * 50)


def handle_generate_student_report(manager):
    print_header("Generate Individual Student Report")
    student_id = input("Enter Student ID: ").strip().upper()
    try:
        report_path, report_content = manager.generate_student_report(student_id)
        print(f"\n[Success] Report generated successfully!")
        print(f"Saved at: {report_path}")
        print("\n--- Report Preview ---")
        preview_lines = report_content.splitlines()[:22]
        print("\n".join(preview_lines))
        print("... [full report saved to file] ...")
    except ValueError as e:
        print(f"\n[Error] {e}")


def handle_generate_overall_report(manager):
    print_header("Generate Overall Institute Report")
    try:
        report_path, report_content = manager.generate_overall_report()
        print(f"\n[Success] Overall report generated successfully!")
        print(f"Saved at: {report_path}")
        print("\n--- Report Summary ---")
        preview_lines = report_content.splitlines()[:25]
        print("\n".join(preview_lines))
        print("... [full report saved to file] ...")
    except Exception as e:
        print(f"\n[Error] Failed to generate overall report: {e}")


def handle_update_student_details(manager):
    print_header("Update Student Details")
    student_id = input("Enter Student ID: ").strip().upper()
    student = manager.get_student_by_id(student_id)
    if not student:
        print(f"[Error] Student '{student_id}' does not exist.")
        return

    print("\nCurrent Details:")
    print(f"  Name  : {student.name}")
    print(f"  Email : {student.email}")
    print(f"  Phone : {student.phone}")
    print(f"  Batch : {student.batch_id}")
    print("\n(Press Enter to keep current value)")

    new_name = input(f"New Name [{student.name}]: ").strip()
    new_email = input(f"New Email [{student.email}]: ").strip()
    new_phone = input(f"New Phone [{student.phone}]: ").strip()
    new_batch = input(f"New Batch ID [{student.batch_id}]: ").strip().upper()

    try:
        updated = manager.update_student(
            student_id=student_id,
            name=new_name if new_name else None,
            email=new_email if new_email else None,
            phone=new_phone if new_phone else None,
            batch_id=new_batch if new_batch else None,
        )
        print("\n[Success] Student details updated successfully!")
        print(f"  ID    : {updated.student_id} (Unchanged)")
        print(f"  Name  : {updated.name}")
        print(f"  Email : {updated.email}")
        print(f"  Phone : {updated.phone}")
        print(f"  Batch : {updated.batch_id}")
    except ValueError as e:
        print(f"\n[Validation Error] {e}")


def handle_view_batch_students(manager):
    print_header("View Students in Batch")
    batches = manager.get_all_batches()
    if not batches:
        print("No batches created yet.")
        return

    print("Existing Batches:")
    for b in batches:
        print(f"  - {b.batch_id}: {b.batch_name} ({b.course_name})")

    batch_id = input("\nEnter Batch ID: ").strip().upper()
    try:
        students = manager.get_students_by_batch(batch_id)
        if not students:
            print(f"No students currently assigned to batch '{batch_id}'.")
            return

        print(f"\nStudents in Batch {batch_id} ({len(students)} total):")
        print(f"{'ID':<8} | {'Name':<20} | {'Email':<25} | {'Phone'}")
        print("-" * 65)
        for s in students:
            print(f"{s.student_id:<8} | {s.name:<20} | {s.email:<25} | {s.phone}")
        print("-" * 65)
    except ValueError as e:
        print(f"\n[Error] {e}")


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================

def main():
    """Entry point for the Placement Readiness Console Application."""
    manager = PlacementManager()

    while True:
        try:
            print_menu()
            choice = input("Enter your choice (0-18): ").strip()

            if choice == "1":
                handle_register_student(manager)
            elif choice == "2":
                handle_create_batch(manager)
            elif choice == "3":
                handle_view_students(manager)
            elif choice == "4":
                handle_record_attendance(manager)
            elif choice == "5":
                handle_enter_python_assessment(manager)
            elif choice == "6":
                handle_enter_technical_scores(manager)
            elif choice == "7":
                handle_update_project_status(manager)
            elif choice == "8":
                handle_update_practice_sessions(manager)
            elif choice == "9":
                handle_update_mock_interview(manager)
            elif choice == "10":
                handle_search_student(manager)
            elif choice == "11":
                handle_view_student_progress(manager)
            elif choice == "12":
                handle_check_placement_eligibility(manager)
            elif choice == "13":
                handle_view_top_performers(manager)
            elif choice == "14":
                handle_view_students_needing_improvement(manager)
            elif choice == "15":
                handle_generate_student_report(manager)
            elif choice == "16":
                handle_generate_overall_report(manager)
            elif choice == "17":
                handle_update_student_details(manager)
            elif choice == "18":
                handle_view_batch_students(manager)
            elif choice == "0":
                print("\nThank you for using the Placement Readiness System.")
                print("Good luck with your placements!\n")
                sys.exit(0)
            else:
                print("\n[Invalid Option] Please enter a valid number between 0 and 18.")

            # Pause before showing menu again for readability
            input("\nPress Enter to return to the menu...")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Returning to menu...")
        except Exception as e:
            print(f"\n[Unexpected Error] An unexpected error occurred: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
