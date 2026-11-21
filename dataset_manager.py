"""
Module 1: dataset_manager.py
============================
Responsible for:
1. Dataset Creation (Generates 60 detailed student records for the hostel system)
2. Python Data Structures Implementation (Demonstrating 5+ Data Structure concepts)
3. File Handling using standard Python I/O and CSV library
"""

import os
import csv
from typing import List, Dict, Any, Tuple, Set

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "hostel_students.csv")
REPORT_FILE = os.path.join(os.path.dirname(__file__), "hostel_summary_report.txt")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Requirement 2: PYTHON DATA STRUCTURES IMPLEMENTATION
# Demonstrating:
# 1. Tuples: Immutable room catalog & fee tier definitions
# 2. Lists & List Methods: Dynamic student lists, append, pop, sort, extend
# 3. Dictionaries & Dictionary Methods: Student entity, keys, values, items, get, update
# 4. Sets & Set Operations: Unique room tracking, union, intersection, difference
# 5. Nested Data Structures: List of Dictionaries for in-memory database
# ---------------------------------------------------------------------------

# Concept 1: TUPLES (Immutable hostel room configurations: Room_Type, Capacity, Base_Hostel_Fee, Base_Mess_Fee)
ROOM_SPEC_CATALOG: Tuple[Tuple[str, int, int, int], ...] = (
    ("Single AC", 1, 65000, 32000),
    ("Single Non-AC", 1, 48000, 30000),
    ("Double AC", 2, 52000, 32000),
    ("Double Non-AC", 2, 40000, 30000),
    ("Triple Non-AC", 3, 32000, 28000),
)

# Concept 2: SETS (Pre-defined room inventory for vacancy tracking)
ALL_ROOMS_INVENTORY: Set[str] = {
    "A-101", "A-102", "A-103", "A-104", "A-105",
    "B-201", "B-202", "B-203", "B-204", "B-205",
    "C-301", "C-302", "C-303", "C-304", "C-305",
    "D-401", "D-402", "D-403", "D-404", "D-405",
    "E-501", "E-502", "E-503", "E-504", "E-505",
    "F-601", "F-602", "F-603", "F-604", "F-605"
}

def demonstrate_data_structures() -> Dict[str, Any]:
    """
    Explicitly demonstrates 5 key Python Data Structure concepts covered in training.
    """
    demo_log = {}

    # 1. LIST & LIST METHODS
    departments: List[str] = ["CSE", "ECE", "MECH"]
    departments.append("CIVIL")              # List Method 1: append
    departments.extend(["IT", "AI&DS"])      # List Method 2: extend
    removed_dept = departments.pop()         # List Method 3: pop
    departments.sort()                       # List Method 4: sort
    demo_log["list_demonstration"] = {
        "final_list": departments,
        "popped_element": removed_dept,
        "list_slice": departments[1:4]
    }

    # 2. DICTIONARIES & DICTIONARY METHODS
    sample_student: Dict[str, Any] = {
        "student_id": "STU1001",
        "name": "Aarav Sharma",
        "room_no": "A-101",
        "hostel_fee_paid": 65000
    }
    keys_view = list(sample_student.keys())      # Dict Method 1: keys()
    values_view = list(sample_student.values())  # Dict Method 2: values()
    sample_student.update({"mess_fee_paid": 32000, "status": "Paid"}) # Dict Method 3: update()
    retrieved_name = sample_student.get("name", "Unknown")           # Dict Method 4: get()
    demo_log["dict_demonstration"] = {
        "keys": keys_view,
        "values": values_view,
        "retrieved_name": retrieved_name,
        "updated_dict": sample_student
    }

    # 3. SETS & SET OPERATIONS
    assigned_rooms: Set[str] = {"A-101", "A-102", "B-201", "C-301"}
    requested_rooms: Set[str] = {"A-101", "D-401", "E-501"}

    vacant_rooms_sample = ALL_ROOMS_INVENTORY.difference(assigned_rooms)     # Set difference
    common_requests = assigned_rooms.intersection(requested_rooms)           # Set intersection
    all_combined = assigned_rooms.union(requested_rooms)                     # Set union

    demo_log["set_demonstration"] = {
        "total_rooms": len(ALL_ROOMS_INVENTORY),
        "assigned_count": len(assigned_rooms),
        "sample_vacant_count": len(vacant_rooms_sample),
        "already_occupied_requested": list(common_requests),
        "all_distinct_combined": len(all_combined)
    }

    # 4. TUPLES & TUPLE UNPACKING
    room_tuple = ROOM_SPEC_CATALOG[0]
    room_type, capacity, base_hostel, base_mess = room_tuple
    demo_log["tuple_demonstration"] = {
        "raw_tuple": room_tuple,
        "unpacked": f"Type: {room_type}, Cap: {capacity}, Hostel: Rs.{base_hostel}, Mess: Rs.{base_mess}"
    }

    # 5. NESTED DATA STRUCTURE (List of Dicts)
    mini_db = [
        {"id": "STU1001", "fee_status": "Paid"},
        {"id": "STU1002", "fee_status": "Partial"}
    ]
    mini_db.append({"id": "STU1003", "fee_status": "Pending"})
    demo_log["nested_structure"] = mini_db

    return demo_log


# ---------------------------------------------------------------------------
# Requirement 1: DATASET CREATION (60 realistic student records)
# Contains diverse students across 4 years, multiple departments, room types,
# fee payment levels, and intentional missing values for cleaning demonstration.
# ---------------------------------------------------------------------------

def generate_initial_dataset() -> List[Dict[str, Any]]:
    """
    Creates a comprehensive dataset with 60 records.
    Includes intentional missing values (e.g. unassigned rooms, unrecorded fees)
    to rigorously test Pandas missing value handling.
    """
    raw_data = [
        ("STU1001", "Aarav Sharma", "Male", "CSE", 1, "A-101", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1002", "Diya Patel", "Female", "ECE", 2, "B-201", "Double AC", 52000, 52000, 32000, 32000),
        ("STU1003", "Rohan Verma", "Male", "MECH", 3, "C-301", "Triple Non-AC", 32000, 20000, 28000, 14000),
        ("STU1004", "Ananya Iyer", "Female", "CSE", 4, "A-102", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1005", "Kabir Singh", "Male", "CIVIL", 1, "D-401", "Double Non-AC", 40000, 25000, 30000, 15000),
        ("STU1006", "Ishita Gupta", "Female", "IT", 2, "B-202", "Single AC", 65000, 65000, 32000, 16000),
        ("STU1007", "Aditya Nair", "Male", "AI&DS", 3, "E-501", "Double AC", 52000, 30000, 32000, 0),
        ("STU1008", "Meera Joshi", "Female", "ECE", 4, "C-302", "Triple Non-AC", 32000, 32000, 28000, 28000),
        ("STU1009", "Siddharth Rao", "Male", "CSE", 1, "A-103", "Single AC", 65000, 0, 32000, 0),
        ("STU1010", "Pooja Reddy", "Female", "IT", 2, "B-203", "Double Non-AC", 40000, 40000, 30000, 30000),
        ("STU1011", "Vikram Malhotra", "Male", "MECH", 3, "D-402", "Triple Non-AC", 32000, 16000, 28000, 14000),
        ("STU1012", "Neha Kulkarni", "Female", "CSE", 4, "A-104", "Single Non-AC", 48000, 48000, 30000, 15000),
        ("STU1013", "Arjun Das", "Male", "CIVIL", 1, "E-502", "Double AC", 52000, 52000, 32000, 32000),
        ("STU1014", "Sneha Menon", "Female", "ECE", 2, "C-303", "Triple Non-AC", 32000, 32000, 28000, 28000),
        ("STU1015", "Kunal Kapoor", "Male", "AI&DS", 3, "B-204", "Single AC", 65000, 45000, 32000, 32000),
        ("STU1016", "Riya Sen", "Female", "IT", 4, "D-403", "Double Non-AC", 40000, 40000, 30000, 30000),
        ("STU1017", "Gaurav Bhat", "Male", "CSE", 1, "A-105", "Double AC", 52000, 26000, 32000, 16000),
        ("STU1018", "Tanya Bansal", "Female", "MECH", 2, "E-503", "Triple Non-AC", 32000, 0, 28000, 0),
        ("STU1019", "Rahul Deshmukh", "Male", "ECE", 3, "B-205", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1020", "Priya Nambiar", "Female", "CIVIL", 4, "C-304", "Double Non-AC", 40000, 35000, 30000, 30000),
        ("STU1021", "Manish Pandey", "Male", "AI&DS", 1, "D-404", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1022", "Kavya Pillai", "Female", "CSE", 2, "A-101", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1023", "Nikhil Saxena", "Male", "IT", 3, "E-504", "Triple Non-AC", 32000, 32000, 28000, 14000),
        ("STU1024", "Swati Chatterjee", "Female", "ECE", 4, "B-201", "Double AC", 52000, 52000, 32000, 32000),
        ("STU1025", "Harshvardhan Jain", "Male", "MECH", 1, "C-305", "Double Non-AC", 40000, 20000, 30000, 10000),
        ("STU1026", "Deepika Roy", "Female", "CIVIL", 2, "D-405", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1027", "Pranav Hegde", "Male", "CSE", 3, "E-505", "Single AC", 65000, 50000, 32000, 32000),
        ("STU1028", "Anusha Prabhu", "Female", "AI&DS", 4, "F-601", "Triple Non-AC", 32000, 32000, 28000, 28000),
        ("STU1029", "Varun Chopra", "Male", "IT", 1, "F-602", "Double AC", 52000, 0, 32000, 0),
        ("STU1030", "Shreya Ghosh", "Female", "ECE", 2, "A-102", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1031", "Akash Mishra", "Male", "MECH", 3, "B-202", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1032", "Sanjana Murthy", "Female", "CSE", 4, "C-301", "Triple Non-AC", 32000, 16000, 28000, 14000),
        ("STU1033", "Mohit Tiwari", "Male", "CIVIL", 1, "D-401", "Double Non-AC", 40000, 40000, 30000, 30000),
        ("STU1034", "Shruti Varma", "Female", "AI&DS", 2, "E-501", "Double AC", 52000, 52000, 32000, 20000),
        ("STU1035", "Abhishek Dubey", "Male", "IT", 3, "A-103", "Single AC", 65000, 35000, 32000, 16000),
        ("STU1036", "Ritika Saxena", "Female", "ECE", 4, "B-203", "Double Non-AC", 40000, 40000, 30000, 30000),
        ("STU1037", "Ayush Agrawal", "Male", "CSE", 1, "C-302", "Triple Non-AC", 32000, 32000, 28000, 28000),
        ("STU1038", "Divya Krishnan", "Female", "MECH", 2, "D-402", "Triple Non-AC", 32000, 0, 28000, 0),
        ("STU1039", "Karthik Sundaram", "Male", "AI&DS", 3, "E-502", "Double AC", 52000, 52000, 32000, 32000),
        ("STU1040", "Bhavna Chawla", "Female", "CIVIL", 4, "A-104", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1041", "Yash Singhal", "Male", "IT", 1, "B-204", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1042", "Nandini Bhatt", "Female", "CSE", 2, "C-303", "Triple Non-AC", 32000, 20000, 28000, 28000),
        ("STU1043", "Sameer Qureshi", "Male", "ECE", 3, "D-403", "Double Non-AC", 40000, 40000, 30000, 15000),
        ("STU1044", "Pallavi Joshi", "Female", "MECH", 4, "E-503", "Triple Non-AC", 32000, 32000, 28000, 28000),
        ("STU1045", "Rajat Sethi", "Male", "AI&DS", 1, "F-603", "Single AC", 65000, 40000, 32000, 20000),
        ("STU1046", "Aastha Grover", "Female", "CIVIL", 2, "F-604", "Double Non-AC", 40000, 40000, 30000, 30000),
        ("STU1047", "Chirag Gandhi", "Male", "IT", 3, "A-105", "Double AC", 52000, 52000, 32000, 32000),
        ("STU1048", "Simran Kaur", "Female", "CSE", 4, "B-205", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1049", "Devendra Rathore", "Male", "ECE", 1, "C-304", "Double Non-AC", 40000, 20000, 30000, 0),
        ("STU1050", "Tanvi Shinde", "Female", "MECH", 2, "D-404", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1051", "Kishore Kumar", "Male", "AI&DS", 3, "E-504", "Triple Non-AC", 32000, 32000, 28000, 28000),
        ("STU1052", "Monika Trivedi", "Female", "CIVIL", 4, "F-605", "Double AC", 52000, 52000, 32000, 32000),
        ("STU1053", "Jatin Solanki", "Male", "CSE", 1, "B-202", "Single AC", 65000, 0, 32000, 0),
        ("STU1054", "Gayatri Venkat", "Female", "IT", 2, "C-305", "Double Non-AC", 40000, 40000, 30000, 15000),
        ("STU1055", "Mayank Bhardwaj", "Male", "ECE", 3, "D-405", "Single Non-AC", 48000, 48000, 30000, 30000),
        ("STU1056", "Vandana Rawat", "Female", "MECH", 4, "E-505", "Single AC", 65000, 65000, 32000, 32000),
        ("STU1057", "Tarun Bajaj", "Male", "CIVIL", 1, "A-102", "Single Non-AC", 48000, 24000, 30000, 15000),
        # 3 Intentional records with missing data (None/Empty) for Pandas missing values demonstration
        ("STU1058", "Alok Sengupta", "Male", "CSE", 2, None, "Single AC", 65000, 65000, 32000, None),
        ("STU1059", "Preeti Dasgupta", "Female", "AI&DS", 3, "B-204", "Single AC", 65000, 30000, 32000, None),
        ("STU1060", "Naveen Jindal", "Male", "IT", 4, None, "Triple Non-AC", 32000, 0, 28000, 0)
    ]

    records = []
    for item in raw_data:
        stu_id, name, gender, dept, year, room, r_type, h_tot, h_pd, m_tot, m_pd = item
        
        # Calculate dues and status
        h_pd_val = h_pd if h_pd is not None else 0
        m_pd_val = m_pd if m_pd is not None else 0
        total_fee = h_tot + m_tot
        total_paid = h_pd_val + m_pd_val
        total_due = total_fee - total_paid

        if total_due == 0 and (h_pd is not None and m_pd is not None):
            status = "Paid"
        elif total_paid == 0:
            status = "Pending"
        else:
            status = "Partial"

        record = {
            "student_id": stu_id,
            "name": name,
            "gender": gender,
            "department": dept,
            "year": year,
            "room_no": room if room else "",
            "room_type": r_type,
            "hostel_fee_total": h_tot,
            "hostel_fee_paid": h_pd if h_pd is not None else "",
            "mess_fee_total": m_tot,
            "mess_fee_paid": m_pd if m_pd is not None else "",
            "fee_status": status
        }
        records.append(record)

    return records


# ---------------------------------------------------------------------------
# Requirement 7: FILE HANDLING IMPLEMENTATION
# Reading, writing, appending, and updating records using pure Python file handling
# ---------------------------------------------------------------------------

CSV_FIELDNAMES = [
    "student_id", "name", "gender", "department", "year",
    "room_no", "room_type", "hostel_fee_total", "hostel_fee_paid",
    "mess_fee_total", "mess_fee_paid", "fee_status"
]

def initialize_dataset_csv(force: bool = False) -> str:
    """
    Creates and populates the CSV file with at least 60 records if not already present.
    Uses standard Python file handling (open, csv.DictWriter).
    """
    if not os.path.exists(DATA_FILE) or force:
        records = generate_initial_dataset()
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)
        return f"Initialized dataset with {len(records)} records at {DATA_FILE}"
    return f"Dataset already exists at {DATA_FILE}"

def read_dataset_from_file() -> List[Dict[str, Any]]:
    """
    Reads the dataset from CSV using Python's with open() and csv.DictReader.
    """
    if not os.path.exists(DATA_FILE):
        initialize_dataset_csv()

    records = []
    with open(DATA_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))
    return records

def save_dataset_to_file(records: List[Dict[str, Any]]) -> bool:
    """
    Overwrites the dataset CSV file with the updated records list.
    """
    try:
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)
        return True
    except IOError as e:
        print(f"[File Error] Unable to write to file: {e}")
        return False

def append_record_to_file(record: Dict[str, Any]) -> bool:
    """
    Appends a single new record to the CSV file.
    """
    try:
        file_exists = os.path.exists(DATA_FILE)
        with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)
        return True
    except IOError as e:
        print(f"[File Error] Append failed: {e}")
        return False

def export_text_report(report_content: str, filename: str = REPORT_FILE) -> str:
    """
    Demonstrates writing analytical summary reports to a text file using open().
    """
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(report_content)
    return filename

