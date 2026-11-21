"""
Module 2: fee_and_room_operations.py
====================================
Contains User-Defined Functions implementing:
1. Room Allocation & Vacancy Tracking (using Sets, Tuples, Dictionaries)
2. Fee Calculation & Defaulter Tracking
3. Complete CRUD Operations (Add, Display, Search, Update, Delete)
4. Operational Summary Report Generation
"""

from typing import List, Dict, Any, Tuple, Optional, Set
from dataset_manager import (
    ROOM_SPEC_CATALOG,
    ALL_ROOMS_INVENTORY,
    save_dataset_to_file,
    append_record_to_file
)

# ---------------------------------------------------------------------------
# Requirement 3: USER-DEFINED FUNCTIONS
# Implementing 8+ user-defined functions performing distinct operations
# ---------------------------------------------------------------------------

def calculate_fee_dues(
    hostel_total: float,
    hostel_paid: float,
    mess_total: float,
    mess_paid: float
) -> Tuple[float, float, float, float, str]:
    """
    User-Defined Function 1:
    Calculates hostel dues, mess dues, total fee, total paid, total dues,
    and determines payment status ('Paid', 'Partial', 'Pending').
    Returns a Tuple (demonstrating Tuple usage).
    """
    h_paid = float(hostel_paid) if hostel_paid not in ("", None) else 0.0
    m_paid = float(mess_paid) if mess_paid not in ("", None) else 0.0
    h_total = float(hostel_total) if hostel_total not in ("", None) else 0.0
    m_total = float(mess_total) if mess_total not in ("", None) else 0.0

    hostel_due = max(0.0, h_total - h_paid)
    mess_due = max(0.0, m_total - m_paid)
    total_fee = h_total + m_total
    total_paid = h_paid + m_paid
    total_due = hostel_due + mess_due

    if total_due <= 0.0:
        status = "Paid"
    elif total_paid <= 0.0:
        status = "Pending"
    else:
        status = "Partial"

    return (hostel_due, mess_due, total_paid, total_due, status)


def get_room_spec(room_type: str) -> Optional[Tuple[str, int, int, int]]:
    """
    User-Defined Function 2:
    Retrieves standard room specifications (Tuple) for a given room type.
    """
    for spec in ROOM_SPEC_CATALOG:
        if spec[0].lower() == room_type.strip().lower():
            return spec
    return None


def track_room_occupancy_and_vacancies(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    User-Defined Function 3:
    Tracks room occupancy and calculates vacant rooms using Set operations and Dictionaries.
    """
    occupied_rooms_count: Dict[str, int] = {}
    assigned_students_per_room: Dict[str, List[str]] = {}

    for r in records:
        room = r.get("room_no", "").strip()
        if room:
            occupied_rooms_count[room] = occupied_rooms_count.get(room, 0) + 1
            if room not in assigned_students_per_room:
                assigned_students_per_room[room] = []
            assigned_students_per_room[room].append(r.get("student_id", ""))

    allocated_rooms_set: Set[str] = set(occupied_rooms_count.keys())
    # Set difference to find completely unallocated rooms
    completely_vacant_rooms: Set[str] = ALL_ROOMS_INVENTORY.difference(allocated_rooms_set)

    return {
        "total_inventory_rooms": len(ALL_ROOMS_INVENTORY),
        "occupied_rooms_count": len(allocated_rooms_set),
        "fully_vacant_rooms_count": len(completely_vacant_rooms),
        "completely_vacant_list": sorted(list(completely_vacant_rooms)),
        "room_occupancy_map": occupied_rooms_count,
        "room_members_map": assigned_students_per_room
    }


def allocate_room_to_student(
    records: List[Dict[str, Any]],
    student_id: str,
    target_room: str,
    room_type: str
) -> Tuple[bool, str]:
    """
    User-Defined Function 4:
    Allocates or reallocates a room to a student after checking capacity and updating fee structures.
    """
    spec = get_room_spec(room_type)
    if not spec:
        return False, f"Invalid room type: '{room_type}'. Must be one of {[s[0] for s in ROOM_SPEC_CATALOG]}"

    max_capacity = spec[1]
    base_hostel_fee = spec[2]
    base_mess_fee = spec[3]

    # Check target room capacity
    current_occupants = sum(1 for r in records if r.get("room_no") == target_room and r.get("student_id") != student_id)
    if current_occupants >= max_capacity:
        return False, f"Room {target_room} is at maximum capacity ({max_capacity} students)."

    # Find student
    found = False
    for r in records:
        if r.get("student_id") == student_id:
            r["room_no"] = target_room
            r["room_type"] = spec[0]
            r["hostel_fee_total"] = base_hostel_fee
            r["mess_fee_total"] = base_mess_fee

            # Recalculate status
            _, _, _, _, status = calculate_fee_dues(
                r["hostel_fee_total"], r.get("hostel_fee_paid", 0),
                r["mess_fee_total"], r.get("mess_fee_paid", 0)
            )
            r["fee_status"] = status
            found = True
            break

    if not found:
        return False, f"Student ID '{student_id}' not found."

    save_dataset_to_file(records)
    return True, f"Successfully allocated Room {target_room} ({room_type}) to Student {student_id}."


# ---------------------------------------------------------------------------
# Requirement 8: PROJECT FUNCTIONALITY (CRUD OPERATIONS)
# Add, Display, Search, Update, Delete, Summary Report
# ---------------------------------------------------------------------------

def add_student_record(records: List[Dict[str, Any]], new_record: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Project Functionality 1: Add a new record.
    Validates uniqueness of student_id, calculates fee status, and persists to file.
    """
    stu_id = new_record.get("student_id", "").strip().upper()
    if not stu_id:
        return False, "Student ID cannot be empty."

    # Check for duplicate
    if any(r.get("student_id") == stu_id for r in records):
        return False, f"Error: Student with ID {stu_id} already exists."

    # Validate room spec
    r_type = new_record.get("room_type", "Single Non-AC")
    spec = get_room_spec(r_type)
    if spec:
        h_total = spec[2] if not new_record.get("hostel_fee_total") else float(new_record["hostel_fee_total"])
        m_total = spec[3] if not new_record.get("mess_fee_total") else float(new_record["mess_fee_total"])
    else:
        h_total = float(new_record.get("hostel_fee_total", 48000))
        m_total = float(new_record.get("mess_fee_total", 30000))

    h_paid = float(new_record.get("hostel_fee_paid", 0) or 0)
    m_paid = float(new_record.get("mess_fee_paid", 0) or 0)

    _, _, _, _, status = calculate_fee_dues(h_total, h_paid, m_total, m_paid)

    formatted_record = {
        "student_id": stu_id,
        "name": new_record.get("name", "").strip(),
        "gender": new_record.get("gender", "Other").strip(),
        "department": new_record.get("department", "GEN").strip().upper(),
        "year": int(new_record.get("year", 1)),
        "room_no": new_record.get("room_no", "").strip().upper(),
        "room_type": spec[0] if spec else r_type,
        "hostel_fee_total": int(h_total),
        "hostel_fee_paid": int(h_paid),
        "mess_fee_total": int(m_total),
        "mess_fee_paid": int(m_paid),
        "fee_status": status
    }

    records.append(formatted_record)
    save_dataset_to_file(records)
    return True, f"Student {stu_id} ({formatted_record['name']}) added successfully."


def display_all_records(records: List[Dict[str, Any]], limit: Optional[int] = None) -> None:
    """
    Project Functionality 2: Display all records.
    Renders records in an aligned, readable terminal table with dues and status.
    """
    if not records:
        print("\n[!] No records found in the database.")
        return

    display_subset = records[:limit] if limit else records
    total_count = len(records)

    header = f"{'ID':<9} | {'Name':<18} | {'Dept':<6} | {'Yr':<3} | {'Room':<7} | {'Room Type':<14} | {'H.Fee':<7} | {'H.Paid':<7} | {'M.Fee':<7} | {'M.Paid':<7} | {'Dues':<7} | {'Status':<7}"
    separator = "-" * len(header)

    print(f"\nHOSTEL STUDENT RECORDS ({len(display_subset)} of {total_count} shown)")
    print(separator)
    print(header)
    print(separator)

    for r in display_subset:
        h_tot = float(r.get("hostel_fee_total") or 0)
        h_pd = float(r.get("hostel_fee_paid") or 0)
        m_tot = float(r.get("mess_fee_total") or 0)
        m_pd = float(r.get("mess_fee_paid") or 0)
        dues = (h_tot - h_pd) + (m_tot - m_pd)
        status = r.get("fee_status", "Pending")

        print(
            f"{r.get('student_id',''):<9} | "
            f"{r.get('name','')[:18]:<18} | "
            f"{r.get('department',''):<6} | "
            f"{str(r.get('year','')):<3} | "
            f"{r.get('room_no','N/A')[:7]:<7} | "
            f"{r.get('room_type','N/A')[:14]:<14} | "
            f"{int(h_tot):<7} | "
            f"{int(h_pd):<7} | "
            f"{int(m_tot):<7} | "
            f"{int(m_pd):<7} | "
            f"{int(dues):<7} | "
            f"{status:<7}"
        )
    print(separator)
    print(f"Total Records: {total_count}\n")


def search_student_records(
    records: List[Dict[str, Any]],
    query: str,
    search_by: str = "all"
) -> List[Dict[str, Any]]:
    """
    Project Functionality 3: Search for a particular record.
    Supports search by ID, name, department, room, or fee status.
    """
    query_clean = query.strip().lower()
    matches = []

    for r in records:
        stu_id = str(r.get("student_id", "")).lower()
        name = str(r.get("name", "")).lower()
        dept = str(r.get("department", "")).lower()
        room = str(r.get("room_no", "")).lower()
        status = str(r.get("fee_status", "")).lower()

        if search_by == "student_id" and query_clean in stu_id:
            matches.append(r)
        elif search_by == "name" and query_clean in name:
            matches.append(r)
        elif search_by == "department" and query_clean == dept:
            matches.append(r)
        elif search_by == "room_no" and query_clean in room:
            matches.append(r)
        elif search_by == "fee_status" and query_clean == status:
            matches.append(r)
        elif search_by == "all":
            if (query_clean in stu_id or
                query_clean in name or
                query_clean in dept or
                query_clean in room or
                query_clean in status):
                matches.append(r)

    return matches


def update_student_record(
    records: List[Dict[str, Any]],
    student_id: str,
    updates: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    Project Functionality 4: Update an existing record.
    Allows updating payments, room, name, or department, and recalculates fee status.
    """
    target = None
    for r in records:
        if r.get("student_id") == student_id:
            target = r
            break

    if not target:
        return False, f"Student ID '{student_id}' does not exist."

    # Apply updates using dict update concepts
    for key, val in updates.items():
        if key in target and val is not None and str(val).strip() != "":
            if key in ["hostel_fee_total", "hostel_fee_paid", "mess_fee_total", "mess_fee_paid", "year"]:
                target[key] = int(float(val))
            else:
                target[key] = str(val).strip()

    # Recalculate fee status
    _, _, _, _, new_status = calculate_fee_dues(
        target["hostel_fee_total"],
        target.get("hostel_fee_paid", 0),
        target["mess_fee_total"],
        target.get("mess_fee_paid", 0)
    )
    target["fee_status"] = new_status

    save_dataset_to_file(records)
    return True, f"Record for {student_id} updated successfully. New Fee Status: {new_status}."


def delete_student_record(
    records: List[Dict[str, Any]],
    student_id: str
) -> Tuple[bool, str]:
    """
    Project Functionality 5: Delete a record.
    Removes student record from list and persists updated list to file.
    """
    idx_to_remove = None
    for idx, r in enumerate(records):
        if r.get("student_id") == student_id:
            idx_to_remove = idx
            break

    if idx_to_remove is None:
        return False, f"Student ID '{student_id}' not found."

    deleted = records.pop(idx_to_remove)  # Using List pop method
    save_dataset_to_file(records)
    return True, f"Student {student_id} ({deleted.get('name')}) removed successfully."


def generate_operational_summary(records: List[Dict[str, Any]]) -> str:
    """
    Project Functionality 6: Generate a summary report.
    Produces comprehensive overview of students, room occupancy, fee collections, and dues.
    """
    total_students = len(records)
    if total_students == 0:
        return "No student records available."

    total_hostel_expected = sum(float(r.get("hostel_fee_total") or 0) for r in records)
    total_hostel_collected = sum(float(r.get("hostel_fee_paid") or 0) for r in records)
    total_mess_expected = sum(float(r.get("mess_fee_total") or 0) for r in records)
    total_mess_collected = sum(float(r.get("mess_fee_paid") or 0) for r in records)

    overall_expected = total_hostel_expected + total_mess_expected
    overall_collected = total_hostel_collected + total_mess_collected
    overall_dues = overall_expected - overall_collected
    collection_rate = (overall_collected / overall_expected * 100) if overall_expected > 0 else 0

    status_counts = {"Paid": 0, "Partial": 0, "Pending": 0}
    for r in records:
        status = r.get("fee_status", "Pending")
        status_counts[status] = status_counts.get(status, 0) + 1

    vacancy_info = track_room_occupancy_and_vacancies(records)

    report_lines = [
        "=" * 65,
        "   HOSTEL ROOM ALLOCATION & FEE MANAGEMENT SYSTEM - SUMMARY REPORT",
        "=" * 65,
        f" Total Registered Students   : {total_students}",
        f" Total Capacity Rooms        : {vacancy_info['total_inventory_rooms']}",
        f" Rooms with Occupants        : {vacancy_info['occupied_rooms_count']}",
        f" Completely Vacant Rooms     : {vacancy_info['fully_vacant_rooms_count']}",
        "-" * 65,
        " FEE COLLECTION OVERVIEW:",
        f" - Hostel Fee Expected       : Rs. {total_hostel_expected:,.2f}",
        f" - Hostel Fee Collected      : Rs. {total_hostel_collected:,.2f}",
        f" - Mess Fee Expected         : Rs. {total_mess_expected:,.2f}",
        f" - Mess Fee Collected        : Rs. {total_mess_collected:,.2f}",
        f" - Overall Fee Expected      : Rs. {overall_expected:,.2f}",
        f" - Overall Fee Collected     : Rs. {overall_collected:,.2f}",
        f" - Outstanding Dues          : Rs. {overall_dues:,.2f}",
        f" - Overall Collection Rate   : {collection_rate:.2f}%",
        "-" * 65,
        " STUDENT FEE STATUS BREAKDOWN:",
        f" - Full Fee Paid Students    : {status_counts.get('Paid', 0)}",
        f" - Partial Paid Students     : {status_counts.get('Partial', 0)}",
        f" - Zero Paid (Pending)       : {status_counts.get('Pending', 0)}",
        "=" * 65
    ]

    return "\n".join(report_lines)

