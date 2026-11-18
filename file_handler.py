"""
file_handler.py - File Handling and Persistence Operations
Project: Placement Readiness and Student Progress Management System
Batch: DA-VSP-006

Demonstrates:
- TXT file reading and writing
- Built-in json module with structured TXT files
- Atomic file updates using temporary files and os.replace
- Safe exception handling for missing, corrupted, or unreadable files
- File and directory path management
"""

import os
import json
from pathlib import Path


class FileManager:
    """
    Manages persistent TXT file operations using JSON formatting.
    Ensures data integrity with atomic writes and corrupted-data protection.
    """

    def __init__(self, data_dir="data", reports_dir="reports"):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self._ensure_directories()

    def _ensure_directories(self):
        """Creates the data and reports directories if they do not exist."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.reports_dir, exist_ok=True)
        except OSError as e:
            print(f"[Error] Failed to create directories: {e}")

    def get_file_path(self, filename):
        """Returns the full Path object for a given data file."""
        return self.data_dir / filename

    def load_json_data(self, filename):
        """
        Loads and parses a JSON record list from a .txt file.
        If the file does not exist, returns an empty list [].
        If the file is corrupted (invalid JSON), displays an understandable error
        and raises ValueError to prevent overwriting or data loss.
        """
        file_path = self.get_file_path(filename)
        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                    raise ValueError(f"Data in {filename} must be a JSON array (list).")
                return data
        except json.JSONDecodeError as e:
            error_msg = f"[Data Integrity Error] File '{filename}' contains corrupted JSON: {e}"
            print(error_msg)
            raise ValueError(error_msg)
        except PermissionError:
            error_msg = f"[Permission Error] Cannot read file '{filename}'. Access denied."
            print(error_msg)
            raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"[Error] Unexpected error reading file '{filename}': {e}"
            print(error_msg)
            raise

    def save_json_data(self, filename, data):
        """
        Saves a list/dict to a .txt file formatted as JSON using an atomic replace.
        Writes to a temporary file first, then replaces the target file via os.replace.
        This prevents file corruption during crashes or partial writes.
        """
        self._ensure_directories()
        target_path = self.get_file_path(filename)
        temp_path = self.data_dir / f"{filename}.tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            # Atomic replace
            os.replace(temp_path, target_path)
            return True
        except PermissionError:
            print(f"[Permission Error] Cannot write to '{filename}'. Access denied.")
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            raise
        except Exception as e:
            print(f"[Error] Failed to save data to '{filename}': {e}")
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            raise

    def write_report_file(self, filename, content):
        """
        Saves human-readable plain text report inside reports directory.
        Uses UTF-8 encoding.
        """
        self._ensure_directories()
        # Prevent directory traversal attacks by taking only the file's basename
        safe_filename = os.path.basename(filename)
        report_path = self.reports_dir / safe_filename

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(content)
            return str(report_path)
        except Exception as e:
            print(f"[Error] Failed to write report file '{safe_filename}': {e}")
            raise
