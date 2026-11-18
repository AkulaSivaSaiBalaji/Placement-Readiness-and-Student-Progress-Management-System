"""
utils.py - Utility Functions and Validation Helpers
Project: Placement Readiness and Student Progress Management System
Batch: DA-VSP-006

This module contains reusable validation functions, mathematical calculations,
and helper utilities demonstrating *args and **kwargs.
"""

import re
from datetime import datetime

# Tuples of fixed system choices (Demonstrating Tuples)
VALID_ATTENDANCE_STATUSES = ("Present", "Absent")
VALID_PROJECT_STATUSES = ("Not Started", "In Progress", "Completed")
VALID_INTERVIEW_STATUSES = ("Not Attended", "Attended", "Passed")
PERFORMANCE_CATEGORIES = ("Excellent", "Good", "Average", "Needs Improvement")

# Dictionary of scoring weights for overall progress (Demonstrating Dictionaries)
PROGRESS_WEIGHTS = {
    "attendance": 0.20,
    "python": 0.20,
    "sql": 0.10,
    "excel": 0.10,
    "powerbi": 0.10,
    "project": 0.10,
    "practice": 0.10,
    "interview": 0.10,
}


# ==========================================
# VALIDATION FUNCTIONS
# ==========================================

def validate_string(value, field_name="Field"):
    """
    Validates that a string is non-empty after stripping whitespace.
    """
    if value is None:
        raise ValueError(f"{field_name} cannot be empty.")
    stripped = str(value).strip()
    if not stripped:
        raise ValueError(f"{field_name} cannot be blank.")
    return stripped


def validate_email(email):
    """
    Validates email format using a simple regex pattern.
    Requires at least one '@' and a domain dot.
    """
    cleaned = validate_string(email, "Email")
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, cleaned):
        raise ValueError(f"Invalid email format: '{email}'. Example: student@example.com")
    return cleaned.lower()


def validate_phone(phone):
    """
    Validates phone number: must be 10 digits (common standard).
    Allows leading/trailing spaces and optional dashes.
    """
    cleaned = validate_string(phone, "Phone number")
    digits_only = re.sub(r"[^\d]", "", cleaned)
    if len(digits_only) != 10:
        raise ValueError(f"Phone number must contain exactly 10 digits. Got {len(digits_only)} digits.")
    return digits_only


def validate_date(date_str):
    """
    Validates that a date matches YYYY-MM-DD format and is a valid calendar date.
    """
    cleaned = validate_string(date_str, "Date")
    try:
        parsed_date = datetime.strptime(cleaned, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_str}'. Expected format is YYYY-MM-DD.")


def validate_score(score, field_name="Score"):
    """
    Validates that a score is a number between 0 and 100 inclusive.
    """
    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number. Got: '{score}'")

    if numeric_score < 0.0 or numeric_score > 100.0:
        raise ValueError(f"{field_name} must be between 0 and 100. Got: {numeric_score}")

    return round(numeric_score, 2)


def validate_choice(value, valid_choices, field_name="Choice"):
    """
    Validates that value belongs to valid_choices (tuple/list).
    Case-insensitive matching that returns the canonical choice.
    """
    cleaned = validate_string(value, field_name)
    for choice in valid_choices:
        if cleaned.lower() == choice.lower():
            return choice

    valid_str = ", ".join(valid_choices)
    raise ValueError(f"Invalid {field_name}: '{value}'. Must be one of: {valid_str}")


# ==========================================
# MATHEMATICAL & PROGRESS HELPERS
# ==========================================

def calculate_percentage(part, total):
    """
    Calculates percentage (part / total) * 100.
    Returns 0.0 if total is 0 or negative.
    """
    if total <= 0:
        return 0.0
    percentage = (part / total) * 100.0
    return round(percentage, 2)


# ==========================================
# *ARGS & **KWARGS DEMONSTRATIONS
# ==========================================

def calculate_average(*args):
    """
    Demonstrates *args:
    Accepts an arbitrary number of numeric arguments and returns their average.
    Ignores None values. If no valid numbers are passed, returns 0.0.
    """
    valid_scores = []
    for item in args:
        if item is not None and isinstance(item, (int, float)):
            valid_scores.append(float(item))

    if not valid_scores:
        return 0.0

    total_sum = sum(valid_scores)
    count = len(valid_scores)
    return round(total_sum / count, 2)


def format_details_card(title, **kwargs):
    """
    Demonstrates **kwargs:
    Formats arbitrary key-value pairs into a clean readable text card.
    Useful for console views and report sections.
    """
    border = "=" * 50
    lines = [border, f" {title.upper()}", border]
    for key, val in kwargs.items():
        formatted_key = key.replace("_", " ").title()
        val_str = "Not Entered" if val is None else str(val)
        lines.append(f"  {formatted_key:<25}: {val_str}")
    lines.append(border)
    return "\n".join(lines)


def format_table_row(*args, width=15):
    """
    Demonstrates *args with a default keyword argument:
    Formats columns into a clean table row.
    """
    formatted_cols = []
    for item in args:
        val_str = "N/A" if item is None else str(item)
        formatted_cols.append(val_str.ljust(width))
    return " | ".join(formatted_cols)
