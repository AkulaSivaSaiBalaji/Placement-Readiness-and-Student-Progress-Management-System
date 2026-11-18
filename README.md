# Placement Readiness and Student Progress Management System

**Project Number:** 25  
**Course:** Python Programming  
**Batch:** DA-VSP-006  
**Developer:** Student, Data Analytics & Python Programming  
**Application Type:** Console-based Python Management System  
**Storage Engine:** Persistent TXT Files (JSON formatted)  
**Python Version:** Python 3.11 or above  

---

## 1. Project Title
**Placement Readiness and Student Progress Management System**

A centralized, menu-driven Python application designed for training institutes to evaluate, monitor, and report on student attendance, technical assessment scores, capstone project status, practice session engagement, mock interview results, and holistic placement eligibility.

---

## 2. Problem Statement
Professional training institutes often track various student learning milestones—such as daily lecture attendance, coding assessment marks, database and visualization scores, practical sessions, and mock interviews—across disconnected spreadsheets or paper records. This fragmented approach leads to:
- Inconsistent and duplicate student data.
- High manual effort in compiling composite progress marks.
- Subjective or delayed identification of students ready for placement drives.
- Delayed interventions for struggling learners.

The **Placement Readiness and Student Progress Management System** solves this by providing a unified, file-persisted console application where faculty and placement officers can manage training batches, register students, log performance indicators, compute weighted readiness scores, and generate official text reports.

---

## 3. Objectives
1. **Centralized Academic Records:** Combine attendance, assessments, project milestones, practice engagement, and mock interviews into a single system.
2. **Automate Performance Metrics:** Calculate weighted progress percentages consistently and accurately without manual spreadsheet formulas.
3. **Transparent Placement Eligibility:** Evaluate every student against 8 strict placement criteria and display transparent reasons for ineligibility.
4. **Identify At-Risk Students:** Flag students needing improvement early based on attendance, individual subject marks, or low overall progress.
5. **Demonstrate Core Python Competencies:** Apply fundamental Python constructs, collections, file I/O, and Object-Oriented Programming (OOP) without third-party frameworks.
6. **Data Integrity & Persistence:** Store records safely in persistent `.txt` files using atomic file writing techniques to avoid corruption.

---

## 4. Features

### Module 1: Student Registration
- Automatic generation of unique Student IDs (e.g., `ST001`, `ST002`).
- Validation of required fields: non-empty name, valid email address format, 10-digit phone number.
- Batch existence verification before student creation.
- Prevention of duplicate Student IDs and duplicate emails.
- Viewing all registered students and updating contact details while locking the Student ID.

### Module 2: Batch Management
- Creation of training batches with unique Batch IDs (e.g., `DA-VSP-006`).
- Mapping batch names and course names.
- Displaying students enrolled within a specific batch.

### Module 3: Attendance Tracking
- Records student presence on specific dates (`YYYY-MM-DD`).
- Valid status values: `Present` or `Absent`.
- Rejection of duplicate attendance on the same date for the same student.
- Calculates attendance percentage: `(Present Days / Total Days) * 100`. Returns `0.0%` for zero recorded days.

### Module 4: Python Assessment Scores
- Logs multiple assessment scores (0–100) per student.
- Prevents duplicate assessment IDs for the same student.
- Computes average Python assessment score across all taken tests.

### Module 5: SQL, Excel, and Power BI Scores
- Manual score entry and update for SQL, Excel, and Power BI modules (0–100).
- Distinguishes missing scores (`Not Entered / None`) from an actual score of `0.0`.

### Module 6: Project Completion Tracking
- Tracks capstone project progress with fixed statuses: `Not Started` (0 pts), `In Progress` (50 pts), `Completed` (100 pts).

### Module 7: Practice Session Tracking
- Tracks total practice sessions conducted and sessions attended.
- Validates that counts are non-negative and attended sessions never exceed conducted sessions.
- Calculates participation percentage: `(Attended / Conducted) * 100`.

### Module 8: Mock Interview Tracking
- Records interview readiness: `Not Attended` (0 pts), `Attended` (50 pts), `Passed` (100 pts).

### Module 9: Performance Category Classification
- Automatically classifies progress using straightforward conditional logic:
  - **Excellent:** 85.00% – 100.00%
  - **Good:** 70.00% – 84.99%
  - **Average:** 50.00% – 69.99%
  - **Needs Improvement:** Below 50.00%

### Module 10: Placement Eligibility Check
- Strictly checks all 8 mandatory benchmarks.
- Reports `ELIGIBLE` or `NOT ELIGIBLE` with exact bulleted reasons for each failed requirement.

### Module 11: Multi-Criteria Student Search
- Search by Student ID, Student Name, or Batch ID.
- Case-insensitive search with partial matching for names.

### Module 12: Top Performers Identification
- Ranks students in descending order by overall progress.
- Uses Student ID as a consistent tie-breaker.
- Displays the top 5 performers (handles batches with fewer than 5 students).

### Module 13: Students Needing Improvement
- Identifies students who have:
  - Overall progress below 50%, OR
  - Attendance below 75%, OR
  - Any assessment score below 60, OR
  - Missing assessment records.
- Prevents duplicate entries using sets and explains issues clearly.

### Module 14: Weighted Progress Percentage
- Computes a comprehensive 100% weighted score rounded to 2 decimal places.

### Module 15: TXT-Based Reports
- Generates formatted, human-readable student reports in `reports/student_report_<student_id>.txt`.
- Generates institute-wide summary reports in `reports/overall_placement_report.txt`.

---

## 5. Technologies Used
- **Programming Language:** Python 3.11+
- **Standard Library Modules Only:**
  - `json`: Structured serialization of Python collections into `.txt` files.
  - `os` & `pathlib`: File path manipulation and directory management.
  - `tempfile`: Atomic replacement and isolated unit test execution.
  - `datetime`: Timestamp generation and attendance date parsing.
  - `re`: Regular expressions for email format and phone number validation.
  - `sys`: Clean exit handling.
  - `unittest`: Automated testing suite.
- **External Dependencies:** **None** (zero third-party packages required).

---

## 6. Python Concepts Demonstrated

| Concept | File / Location | Demonstration Details |
|---|---|---|
| **Variables & Operators** | `utils.py`, `manager.py` | Arithmetic weights, percentage calculations, logical comparisons (`>=`, `and`, `or`). |
| **Strings** | `utils.py`, `models.py` | String formatting, case folding (`lower()`, `upper()`), stripping whitespace, regular expressions. |
| **Lists** | `manager.py`, `file_handler.py` | Collections of records, sorted rankings, dynamic accumulator lists. |
| **Tuples** | `utils.py` | Immutable choices: `VALID_ATTENDANCE_STATUSES`, `VALID_PROJECT_STATUSES`, `VALID_INTERVIEW_STATUSES`. |
| **Sets** | `manager.py` | Uniqueness checks for Student IDs, emails, batch IDs, and deduplicating students needing improvement. |
| **Dictionaries** | `manager.py`, `utils.py` | JSON record schemas, assessment score lookups, weight mapping (`PROGRESS_WEIGHTS`). |
| **Conditionals** | `manager.py` | `if-elif-else` branching for categorization, placement eligibility, and validation rules. |
| **Loops** | `main.py`, `manager.py` | `while` loop driving the interactive menu; `for` loops iterating over student records and files. |
| **Functions** | `utils.py`, `main.py` | Modular functions each with a single responsibility. |
| ***args** | `utils.py` (`calculate_average`) | Accepts arbitrary numbers of score arguments to compute an average: `calculate_average(*args)`. |
| ****kwargs** | `utils.py` (`format_details_card`) | Accepts arbitrary named attributes to format into a clean display card: `format_details_card(title, **kwargs)`. |
| **Classes & Objects** | `models.py`, `manager.py` | `Person`, `Student`, `Batch`, `FileManager`, `PlacementManager`. |
| **Encapsulation** | `models.py` (`Person`) | Private attribute `__email` accessible only via `get_email()`, `set_email()`, and `@property email`. |
| **Inheritance** | `models.py` (`Student`) | `Student` inherits base attributes (`name`, `email`, `phone`) from `Person` using `super().__init__()`. |
| **Polymorphism** | `models.py` (`Student`) | `Student` overrides `display_details()` from `Person` to display academic details. |
| **Exception Handling** | `file_handler.py`, `main.py` | `try-except` blocks handling `ValueError`, `json.JSONDecodeError`, `FileNotFoundError`, `PermissionError`. |
| **Built-in Modules** | Across all files | `json`, `datetime`, `os`, `pathlib`, `re`, `tempfile`, `unittest`. |
| **TXT File Handling** | `file_handler.py` | Persistent `.txt` files with UTF-8 encoding and atomic writing via `os.replace`. |

---

## 7. Project Folder Structure

```text
Placement-Readiness-and-Student-Progress-Management-System/
│
├── main.py              # Console menu loop and user interaction handlers
├── models.py            # OOP domain models: Person, Student(Person), Batch
├── manager.py           # Core business logic, calculations, and reporting
├── file_handler.py      # TXT file persistence and atomic file I/O operations
├── utils.py             # Validation helpers, mathematical formulas, *args & **kwargs
│
├── data/                # Persistent TXT data files (JSON formatted)
│   ├── students.txt
│   ├── batches.txt
│   ├── attendance.txt
│   ├── assessments.txt
│   ├── practice.txt
│   └── interviews.txt
│
├── reports/             # Generated TXT evaluation reports
│   ├── overall_placement_report.txt
│   └── student_report_ST001.txt
│
├── tests/               # Automated unit tests using unittest
│   └── test_project.py
│
├── README.md            # Comprehensive project documentation
├── requirements.txt     # Environment specifications (zero third-party dependencies)
└── .gitignore           # Git ignore rules for caches, venvs, and generated reports
```

---

## 8. Installation Instructions

1. **Prerequisites:**
   Ensure Python 3.11 or above is installed on your computer. Verify by opening a terminal or command prompt:
   ```bash
   python --version
   ```

2. **Clone / Open the Project:**
   Navigate into the project directory:
   ```bash
   cd d:\python_project
   ```

3. **Dependencies:**
   No third-party packages (pip install) are required. The project runs entirely on Python's built-in standard library.

---

## 9. How to Run the Application

Start the interactive console application:

```bash
python main.py
```

---

## 10. Console Menu Structure

When running `main.py`, the user is greeted with the following 18 options plus exit:

```text
========== PLACEMENT READINESS SYSTEM ==========
 1. Register Student
 2. Create Batch
 3. View Students
 4. Record Attendance
 5. Enter Python Assessment
 6. Enter SQL / Excel / Power BI Scores
 7. Update Project Status
 8. Update Practice Sessions
 9. Update Mock Interview Status
10. Search Student
11. View Student Progress
12. Check Placement Eligibility
13. View Top Performers
14. View Students Needing Improvement
15. Generate Student Report
16. Generate Overall Report
17. Update Student Details
18. View Batch Students
 0. Exit
================================================
Enter your choice (0-18):
```

---

## 11. Sample Workflow

1. **Option 2 (Create Batch):** Create a new batch, e.g., `DA-VSP-006` ("Data Analytics Visakhapatnam").
2. **Option 1 (Register Student):** Register student "Aarav Sharma" into batch `DA-VSP-006`. The system generates ID `ST001`.
3. **Option 4 (Record Attendance):** Log daily attendance as `Present` or `Absent`.
4. **Option 5 (Enter Python Assessment):** Enter score `85` for assessment `PY01`.
5. **Option 6 (Enter Technical Scores):** Enter SQL (`85`), Excel (`90`), and Power BI (`80`) scores.
6. **Option 7 (Update Project Status):** Mark the student's capstone project as `Completed`.
7. **Option 8 (Update Practice Sessions):** Record `20` conducted sessions and `18` attended sessions.
8. **Option 9 (Update Mock Interview):** Mark mock interview status as `Passed`.
9. **Option 11 (View Progress):** Review composite weighted score (e.g., `92.00%` – Excellent).
10. **Option 12 (Check Eligibility):** Verify that student meets all placement criteria (`ELIGIBLE`).
11. **Option 15 (Generate Report):** Create a permanent text report in `reports/student_report_ST001.txt`.

---

## 12. Progress Calculation Formula

The overall student progress percentage is calculated using the following weights:

$$\text{Overall Progress} = (\text{Att} \times 0.20) + (\text{PyAvg} \times 0.20) + (\text{SQL} \times 0.10) + (\text{Excel} \times 0.10) + (\text{PBI} \times 0.10) + (\text{Proj} \times 0.10) + (\text{Prac} \times 0.10) + (\text{Mock} \times 0.10)$$

Where:
- **Attendance (20%):** $\frac{\text{Present Days}}{\text{Total Recorded Days}} \times 100$ ($0.0\%$ if total is 0).
- **Python Average (20%):** $\frac{\sum \text{Python Scores}}{\text{Count of Assessments}}$ ($0.0\%$ if none recorded).
- **SQL (10%):** Manual score $0-100$ (contributes 0 if not entered).
- **Excel (10%):** Manual score $0-100$ (contributes 0 if not entered).
- **Power BI (10%):** Manual score $0-100$ (contributes 0 if not entered).
- **Project Completion (10%):**
  - Not Started = $0$
  - In Progress = $50$
  - Completed = $100$
- **Practice Participation (10%):** $\frac{\text{Sessions Attended}}{\text{Total Sessions Conducted}} \times 100$ ($0.0\%$ if conducted is 0).
- **Mock Interview (10%):**
  - Not Attended = $0$
  - Attended = $50$
  - Passed = $100$

The final result is rounded to **2 decimal places**. Missing scores contribute $0.0$ towards progress calculation, but are explicitly displayed as `"Not Entered (Missing)"` in views and reports to differentiate them from actual zero scores.

---

## 13. Placement Eligibility Rules

A student is classified as **Eligible** only when **ALL 8** conditions below are satisfied simultaneously:

| Milestone | Minimum Requirement | Notes |
|---|---|---|
| **Attendance** | $\ge 75.00\%$ | Must have at least 1 recorded session; 0 days does not qualify. |
| **Python Average** | $\ge 60.00\%$ | Must have completed at least 1 Python assessment. |
| **SQL Score** | $\ge 60$ | Must be recorded (missing scores are ineligible). |
| **Excel Score** | $\ge 60$ | Must be recorded (missing scores are ineligible). |
| **Power BI Score** | $\ge 60$ | Must be recorded (missing scores are ineligible). |
| **Project Status** | `Completed` | In Progress or Not Started are ineligible. |
| **Practice Participation** | $\ge 70.00\%$ | Must have at least 1 conducted practice session. |
| **Mock Interview** | `Passed` | Attended or Not Attended are ineligible. |

If any condition is not met, the student is marked as **Not Eligible**, and the exact list of failure reasons is displayed and logged in reports.

---

## 14. Data Integrity and Security Practices

1. **Atomic File Replacement:** Data files are updated by first writing to a temporary file (`.tmp`) and then atomically replacing the target file using `os.replace()`. This prevents file corruption if a process terminates midway.
2. **Corrupted Data Protection:** If any TXT file contains invalid or corrupted JSON, `FileManager` raises a descriptive `ValueError` and prevents the application from blindly overwriting or resetting valid records.
3. **No Code Execution:** The application never invokes `eval()` or `exec()`. User inputs are validated strictly as safe strings or converted to floats/integers with error handling.
4. **Path Traversal Protection:** Report filenames are generated strictly from sanitized Student IDs and saved using `os.path.basename` to prevent path traversal vulnerabilities.
5. **Referential Integrity:**
   - Students cannot be registered under non-existent Batch IDs.
   - Attendance and scores can only be recorded for valid, existing Student IDs.
   - Student IDs cannot be modified during student updates.
6. **UTF-8 Encoding:** All file operations explicitly use `encoding="utf-8"` for cross-platform compatibility.

---

## 15. Testing Instructions

The project includes an automated test suite with **30 unit tests** built on Python's built-in `unittest` module. Tests run in isolated temporary directories (`tempfile.TemporaryDirectory`) to ensure demonstration and production data are never modified.

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

### Verified Test Coverage:
- `test_person_encapsulation`: Private attribute `__email`, validation in getter/setter.
- `test_student_inheritance_and_polymorphism`: Inheritance from Person, polymorphic override of `display_details()`.
- `test_args_calculate_average`: Arbitrary arguments handling with `*args`.
- `test_kwargs_format_details_card`: Arbitrary keyword formatting with `**kwargs`.
- `test_student_registration_success`: Valid student creation.
- `test_duplicate_student_id_prevention`: Duplicate ID rejection.
- `test_duplicate_email_prevention`: Case-insensitive duplicate email rejection.
- `test_invalid_batch_rejection`: Foreign batch validation.
- `test_invalid_phone_and_name_rejection`: Field validation.
- `test_update_student_details`: Modifying details without changing Student ID.
- `test_attendance_tracking_and_percentage`: Attendance calculation.
- `test_attendance_zero_days`: Zero recorded days edge case.
- `test_duplicate_attendance_date_rejection`: Same day duplicate prevention.
- `test_python_assessment_average`: Python assessment averaging.
- `test_duplicate_assessment_id_rejection`: Duplicate test prevention.
- `test_invalid_score_rejection`: Rejection of scores $<0$ or $>100$.
- `test_technical_scores_missing_vs_zero`: Distinguishing `None` from `0.0`.
- `test_practice_sessions_calculation`: Practice percentage formula.
- `test_practice_invalid_inputs`: Rejecting negative sessions or attended $>$ conducted.
- `test_overall_progress_calculation`: Exact verification of all weighted components.
- `test_placement_eligibility_passed`: Verifying eligibility when all 8 criteria pass.
- `test_placement_ineligible_reasons`: Verifying specific failure reasons returned.
- `test_student_search`: Case-insensitive search by Name, ID, and Batch.
- `test_top_performers_ranking`: Top performers ranking and tie-breaker sorting.
- `test_report_generation`: Text file output generation for student and overall reports.
- `test_txt_persistence_after_restart`: Writing, reloading, and verifying persistence.
- `test_corrupted_data_handling`: Integrity protection against corrupted TXT files.

---

## 16. Project Limitations
- **Single Instance Support:** Designed for single-operator console execution; does not support concurrent multi-user write operations.
- **Local Console UI:** Runs in standard terminal environments rather than graphical desktop or web interfaces.
- **TXT/JSON Storage:** Optimized for institute batch sizes; larger enterprise datasets (e.g., 50,000+ students) would benefit from relational database indexing.

---

## 17. Future Enhancements
- Export reports to CSV or PDF formats.
- Add email dispatch functionality to send reports directly to students.
- Introduce attendance barcode/QR-code scanning integration.
- Graphical performance dashboards using Tkinter or web endpoints.

---

## 18. Conclusion
The **Placement Readiness and Student Progress Management System** satisfies all project and academic requirements for Capstone Project 25 (Batch: DA-VSP-006). It delivers a robust, transparent, and user-friendly console application demonstrating clean Python code, data integrity, thorough error handling, and core Object-Oriented Programming principles.
