"""
models.py - Object-Oriented Domain Models
Project: Placement Readiness and Student Progress Management System
Batch: DA-VSP-006

Demonstrates:
- Classes and Objects
- Constructors (__init__)
- Inheritance (Student inherits from Person)
- Polymorphism (Overriding display_details)
- Encapsulation (Private attribute __email with getters/setters)
"""

from utils import validate_string, validate_email, validate_phone


class Person:
    """
    Parent class representing a person with contact details.
    Demonstrates Encapsulation via private attribute __email.
    """

    def __init__(self, name, email, phone):
        self.name = validate_string(name, "Name")
        # Private attribute __email (Encapsulation)
        self.__email = ""
        self.set_email(email)
        self.phone = validate_phone(phone)

    def get_email(self):
        """Getter method for private __email."""
        return self.__email

    def set_email(self, email):
        """Setter method for private __email with validation."""
        self.__email = validate_email(email)

    # Property decorators for Pythonic access
    @property
    def email(self):
        """Property getter for email."""
        return self.get_email()

    @email.setter
    def email(self, new_email):
        """Property setter for email."""
        self.set_email(new_email)

    def display_details(self):
        """
        Base method to display contact details.
        Overridden by Student to demonstrate Polymorphism.
        """
        return f"Name: {self.name} | Email: {self.email} | Phone: {self.phone}"


class Student(Person):
    """
    Child class representing a registered Student.
    Inherits from Person and demonstrates Inheritance and Polymorphism.
    """

    def __init__(self, student_id, name, email, phone, batch_id):
        # Call parent constructor (Inheritance)
        super().__init__(name, email, phone)
        self.student_id = validate_string(student_id, "Student ID").upper()
        self.batch_id = validate_string(batch_id, "Batch ID").upper()

    def display_details(self):
        """
        Polymorphic method: Overrides Person.display_details()
        to include student ID and assigned batch ID.
        """
        return (
            f"Student ID: {self.student_id:<8} | "
            f"Name: {self.name:<20} | "
            f"Batch: {self.batch_id:<12} | "
            f"Email: {self.email:<25} | "
            f"Phone: {self.phone}"
        )

    def to_dict(self):
        """Converts the Student object into a dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "batch_id": self.batch_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Factory method to create a Student object from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            batch_id=data["batch_id"],
        )


class Batch:
    """
    Represents a training batch in the institute.
    """

    def __init__(self, batch_id, batch_name, course_name):
        self.batch_id = validate_string(batch_id, "Batch ID").upper()
        self.batch_name = validate_string(batch_name, "Batch Name")
        self.course_name = validate_string(course_name, "Course Name")

    def display_details(self):
        """Displays batch details."""
        return (
            f"Batch ID: {self.batch_id:<12} | "
            f"Batch Name: {self.batch_name:<30} | "
            f"Course: {self.course_name}"
        )

    def to_dict(self):
        """Converts the Batch object into a dictionary for JSON serialization."""
        return {
            "batch_id": self.batch_id,
            "batch_name": self.batch_name,
            "course_name": self.course_name,
        }

    @classmethod
    def from_dict(cls, data):
        """Factory method to create a Batch object from a dictionary."""
        return cls(
            batch_id=data["batch_id"],
            batch_name=data["batch_name"],
            course_name=data["course_name"],
        )
