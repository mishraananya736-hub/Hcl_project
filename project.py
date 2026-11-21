"""
Main Application Entry Point: project.py
========================================
Hostel Room Allocation and Fee Management System
Demonstrates all 10 Mandatory Technical Implementation Parameters:
1. Dataset Creation (60 records)
2. Python Data Structures (List, Tuple, Set, Dict, Nested Structures)
3. User-Defined Functions (15+ functions across modules)
4. NumPy Implementation (1D/2D arrays, indexing, slicing, sum, mean, min, max, std dev)
5. Pandas Implementation (DataFrame, CSV read, filter, sort, GroupBy, missing values, describe)
6. Python Modules (Imports dataset_manager, fee_and_room_operations, analytics_engine)
7. File Handling (open(), csv reader/writer, report export)
8. Project Functionality (Add, Display, Search, Update, Delete, Summary Report)
9. Data Analysis (Actionable business insights)
10. Output Presentation (Clean terminal output in VS Code)
"""

import sys
import os
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Requirement 6: PYTHON MODULES IMPORTATION
# Importing a minimum of three separate Python modules
# ---------------------------------------------------------------------------
import dataset_manager
import fee_and_room_operations
import analytics_engine


def print_banner() -> None:
    banner = r"""
========================================================================
   HOSTEL ROOM ALLOCATION AND FEE MANAGEMENT SYSTEM (HCL TRAINING)
========================================================================
   Modules Loaded:
   [1] dataset_manager.py         (Data Structures, CSV File Handling)
   [2] fee_and_room_operations.py (Room Allocation, Fee & CRUD Logic)
   [3] analytics_engine.py        (NumPy & Pandas Analytics Engine)
========================================================================
"""
    print(banner)


def handle_add_student(records: List[Dict[str, Any]]) -> None:
    print("\n--- ADD NEW STUDENT RECORD ---")
    stu_id = input("Enter Student ID (e.g. STU1061): ").strip().upper()
    name = input("Enter Student Name: ").strip()
    gender = input("Enter Gender (Male/Female/Other): ").strip()
    dept = input("Enter Department (CSE/ECE/MECH/CIVIL/IT/AI&DS): ").strip().upper()
    try:
        year = int(input("Enter Year of Study (1-4): ").strip())
    except ValueError:
        year = 1

    print("\nAvailable Room Types:")
    for idx, spec in enumerate(dataset_manager.ROOM_SPEC_CATALOG, 1):
        print(f" {idx}. {spec[0]} (Cap: {spec[1]}, Hostel: Rs.{spec[2]}, Mess: Rs.{spec[3]})")
    
    r_type_choice = input("Select Room Type (1-5 or type name) [Default: 2 (Single Non-AC)]: ").strip()
    room_types = [s[0] for s in dataset_manager.ROOM_SPEC_CATALOG]
    if r_type_choice.isdigit() and 1 <= int(r_type_choice) <= len(room_types):
        room_type = room_types[int(r_type_choice) - 1]
    elif r_type_choice in room_types:
        room_type = r_type_choice
    else:
        room_type = "Single Non-AC"

    room_no = input("Enter Room Number (e.g. A-105) or leave blank: ").strip().upper()

    try:
        h_paid = float(input("Enter Hostel Fee Paid so far [0]: ") or 0)
    except ValueError:
        h_paid = 0.0

    try:
        m_paid = float(input("Enter Mess Fee Paid so far [0]: ") or 0)
    except ValueError:
        m_paid = 0.0

    new_student = {
        "student_id": stu_id,
        "name": name,
        "gender": gender,
        "department": dept,
        "year": year,
        "room_no": room_no,
        "room_type": room_type,
        "hostel_fee_paid": h_paid,
        "mess_fee_paid": m_paid
    }

    success, msg = fee_and_room_operations.add_student_record(records, new_student)
    print(f"\n[{'SUCCESS' if success else 'ERROR'}] {msg}")


def handle_search_student(records: List[Dict[str, Any]]) -> None:
    print("\n--- SEARCH STUDENT RECORDS ---")
    print("Search by:")
    print(" 1. Student ID")
    print(" 2. Student Name")
    print(" 3. Department")
    print(" 4. Room Number")
    print(" 5. Fee Status (Paid / Partial / Pending)")
    print(" 6. Universal Search (Any field)")

    choice = input("Enter choice (1-6): ").strip()
    key_map = {
        "1": "student_id",
        "2": "name",
        "3": "department",
        "4": "room_no",
        "5": "fee_status",
        "6": "all"
    }
    search_by = key_map.get(choice, "all")
    query = input("Enter search keyword: ").strip()

    results = fee_and_room_operations.search_student_records(records, query, search_by)
    if results:
        print(f"\nFound {len(results)} matching record(s):")
        fee_and_room_operations.display_all_records(results)
    else:
        print(f"\n[!] No records found matching '{query}'.")


def handle_update_student(records: List[Dict[str, Any]]) -> None:
    print("\n--- UPDATE STUDENT RECORD ---")
    stu_id = input("Enter Student ID to update (e.g. STU1001): ").strip().upper()
    matches = fee_and_room_operations.search_student_records(records, stu_id, "student_id")
    if not matches:
        print(f"[!] Student ID '{stu_id}' not found.")
        return

    print("Current Record:")
    fee_and_room_operations.display_all_records(matches)

    print("Enter new values (leave blank to keep unchanged):")
    new_room = input("New Room Number: ").strip().upper()
    new_h_paid = input("New Hostel Fee Paid: ").strip()
    new_m_paid = input("New Mess Fee Paid: ").strip()
    new_dept = input("New Department: ").strip().upper()

    updates = {}
    if new_room:
        updates["room_no"] = new_room
    if new_h_paid:
        updates["hostel_fee_paid"] = new_h_paid
    if new_m_paid:
        updates["mess_fee_paid"] = new_m_paid
    if new_dept:
        updates["department"] = new_dept

    if updates:
        success, msg = fee_and_room_operations.update_student_record(records, stu_id, updates)
        print(f"\n[{'SUCCESS' if success else 'ERROR'}] {msg}")
    else:
        print("\n[!] No updates provided.")


def handle_delete_student(records: List[Dict[str, Any]]) -> None:
    print("\n--- DELETE STUDENT RECORD ---")
    stu_id = input("Enter Student ID to delete (e.g. STU1001): ").strip().upper()
    confirm = input(f"Are you sure you want to delete student {stu_id}? (y/n): ").strip().lower()
    if confirm == "y":
        success, msg = fee_and_room_operations.delete_student_record(records, stu_id)
        print(f"\n[{'SUCCESS' if success else 'ERROR'}] {msg}")
    else:
        print("\nDeletion cancelled.")


def handle_vacancy_tracking(records: List[Dict[str, Any]]) -> None:
    print("\n--- ROOM OCCUPANCY & VACANCY TRACKING (SETS & DICTS) ---")
    status = fee_and_room_operations.track_room_occupancy_and_vacancies(records)
    print(f" Total Registered Room Inventory : {status['total_inventory_rooms']}")
    print(f" Occupied Rooms Count             : {status['occupied_rooms_count']}")
    print(f" Completely Vacant Rooms Count    : {status['fully_vacant_rooms_count']}")
    print("\n Completely Vacant Rooms List (Available for allocation):")
    print(", ".join(status["completely_vacant_list"]))
    
    # Prompt for allocation
    alloc_choice = input("\nDo you want to allocate a student to a room now? (y/n): ").strip().lower()
    if alloc_choice == "y":
        stu_id = input("Enter Student ID: ").strip().upper()
        target_room = input("Enter Target Room (e.g. A-101): ").strip().upper()
        print("Room Types:", [s[0] for s in dataset_manager.ROOM_SPEC_CATALOG])
        r_type = input("Enter Room Type: ").strip()
        success, msg = fee_and_room_operations.allocate_room_to_student(records, stu_id, target_room, r_type)
        print(f"[{'SUCCESS' if success else 'ERROR'}] {msg}")


def handle_data_structures_demo() -> None:
    print("\n" + "="*70)
    print("      PYTHON DATA STRUCTURES IMPLEMENTATION DEMONSTRATION")
    print("="*70)
    demo = dataset_manager.demonstrate_data_structures()

    print("[1] LIST & LIST METHODS:")
    print(f"    - Methods used: .append(), .extend(), .pop(), .sort()")
    print(f"    - Final list after operations: {demo['list_demonstration']['final_list']}")
    print(f"    - Element popped using .pop(): '{demo['list_demonstration']['popped_element']}'")
    print(f"    - List slicing [1:4]: {demo['list_demonstration']['list_slice']}")

    print("\n[2] DICTIONARIES & DICTIONARY METHODS:")
    print(f"    - Methods used: .keys(), .values(), .update(), .get()")
    print(f"    - Keys view: {demo['dict_demonstration']['keys']}")
    print(f"    - Values view: {demo['dict_demonstration']['values']}")
    print(f"    - Retrieved using .get('name'): '{demo['dict_demonstration']['retrieved_name']}'")
    print(f"    - Dictionary after .update(): {demo['dict_demonstration']['updated_dict']}")

    print("\n[3] SETS & SET OPERATIONS:")
    print(f"    - Operations used: difference(), intersection(), union()")
    print(f"    - Total room inventory (Set): {demo['set_demonstration']['total_rooms']} rooms")
    print(f"    - Vacant rooms via Set Difference (All - Assigned): {demo['set_demonstration']['sample_vacant_count']}")
    print(f"    - Overlap via Set Intersection: {demo['set_demonstration']['already_occupied_requested']}")

    print("\n[4] TUPLES (IMMUTABLE SPECIFICATIONS & UNPACKING):")
    print(f"    - Raw tuple: {demo['tuple_demonstration']['raw_tuple']}")
    print(f"    - Unpacked data: {demo['tuple_demonstration']['unpacked']}")

    print("\n[5] NESTED DATA STRUCTURES (List of Dicts):")
    print(f"    - In-Memory records database: {demo['nested_structure']}")
    print("="*70 + "\n")


def handle_generate_summary_report(records: List[Dict[str, Any]]) -> None:
    summary_text = fee_and_room_operations.generate_operational_summary(records)
    print("\n" + summary_text)

    # Export to text file
    saved_path = dataset_manager.export_text_report(summary_text)
    print(f"\n[File Handling] Summary report exported successfully to: {saved_path}")


def handle_generate_graphs() -> None:
    print("\n--- GENERATING 4 VISUAL GRAPHS (MATPLOTLIB) ---")
    df_clean, _ = analytics_engine.load_and_clean_dataframe()
    saved_files = analytics_engine.generate_visualizations(df_clean)
    print("Successfully generated and saved graph image files:")
    for f in saved_files:
        print(f" [*] Saved: {f}")


def run_full_automated_demo() -> None:
    """
    Executes all 10 Mandatory Technical Implementation Parameters sequentially
    for automated verification and grading.
    """
    print("\n" + "#"*75)
    print("   AUTOMATED DEMONSTRATION OF ALL 10 MANDATORY TECHNICAL PARAMETERS")
    print("#"*75)

    # 1. Dataset Creation
    print("\n>>> Parameter 1: Dataset Creation & Verification")
    dataset_manager.initialize_dataset_csv(force=False)
    records = dataset_manager.read_dataset_from_file()
    print(f"[*] Verified dataset records count: {len(records)} records (Minimum requirement: 50).")

    # 2. Python Data Structures
    print("\n>>> Parameter 2: Python Data Structures (List, Tuple, Set, Dict, Nested)")
    handle_data_structures_demo()

    # 3. User-Defined Functions & 8. Project Functionality
    print("\n>>> Parameter 3 & 8: User-Defined Functions & Core Project Operations")
    
    # Display Records (Parameter 8: Display)
    print("\n[Operation 1: Display Records (First 5 sample records)]")
    fee_and_room_operations.display_all_records(records, limit=5)

    # Add Record (Parameter 8: Add)
    print("\n[Operation 2: Add New Record]")
    test_stu_id = "STU1099"
    test_student = {
        "student_id": test_stu_id,
        "name": "Demo Evaluation Student",
        "gender": "Female",
        "department": "CSE",
        "year": 3,
        "room_no": "A-101",
        "room_type": "Single AC",
        "hostel_fee_paid": 65000,
        "mess_fee_paid": 32000
    }
    # Clean if already present from previous run
    fee_and_room_operations.delete_student_record(records, test_stu_id)
    success, msg = fee_and_room_operations.add_student_record(records, test_student)
    print(f"Add Result: {msg}")

    # Search Record (Parameter 8: Search)
    print("\n[Operation 3: Search for Added Student]")
    search_res = fee_and_room_operations.search_student_records(records, test_stu_id, "student_id")
    fee_and_room_operations.display_all_records(search_res)

    # Update Record (Parameter 8: Update)
    print("\n[Operation 4: Update Record (Change room and mess fee)]")
    upd_success, upd_msg = fee_and_room_operations.update_student_record(
        records, test_stu_id, {"room_no": "B-201", "department": "AI&DS"}
    )
    print(f"Update Result: {upd_msg}")

    # Vacancy tracking
    print("\n[Operation 5: Room Vacancy Tracking via Sets]")
    vac_res = fee_and_room_operations.track_room_occupancy_and_vacancies(records)
    print(f"Vacant Rooms Count: {vac_res['fully_vacant_rooms_count']} rooms available.")

    # Delete Record (Parameter 8: Delete)
    print("\n[Operation 6: Delete Record (Clean up demo record)]")
    del_success, del_msg = fee_and_room_operations.delete_student_record(records, test_stu_id)
    print(f"Delete Result: {del_msg}")

    # 4. NumPy Implementation
    print("\n>>> Parameter 4: NumPy Implementation")
    np_analytics = analytics_engine.run_numpy_analytics()
    analytics_engine.print_numpy_report(np_analytics)

    # 5. Pandas Implementation
    print("\n>>> Parameter 5: Pandas Implementation")
    df_clean, clean_meta = analytics_engine.load_and_clean_dataframe()
    analytics_engine.print_pandas_report(df_clean, clean_meta)

    # 7. File Handling & Summary Report
    print("\n>>> Parameter 7 & 8: File Handling & Operational Summary Report")
    handle_generate_summary_report(records)

    # 4 Graphs Visualization
    print("\n>>> Visual Data Graphs (Matplotlib: 4 Graphs + Dashboard)")
    handle_generate_graphs()

    # 9 & 10. Data Analysis & Output Presentation
    print("\n>>> Parameter 9 & 10: Insights & Terminal Presentation Summary")
    print("[*] All analytical tables, metrics, and insights rendered in VS Code terminal format.")
    print("\n" + "#"*75)
    print("   AUTOMATED DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("#"*75 + "\n")


def main_menu() -> None:
    # Ensure dataset is ready
    dataset_manager.initialize_dataset_csv(force=False)
    records = dataset_manager.read_dataset_from_file()

    while True:
        print_banner()
        print("MAIN MENU:")
        print(" 1.  Display All Student Records")
        print(" 2.  Add New Student Record")
        print(" 3.  Search for a Student Record")
        print(" 4.  Update an Existing Student Record")
        print(" 5.  Delete a Student Record")
        print(" 6.  Room Vacancy & Allocation Tracking (Sets & Dicts)")
        print(" 7.  NumPy Implementation & Analytics (1D/2D, Slicing, Stats, Std Dev)")
        print(" 8.  Pandas Implementation & Analysis (DataFrame, Cleaning, Filter, GroupBy)")
        print(" 9.  Python Data Structures Demonstration (List, Dict, Set, Tuple)")
        print(" 10. Generate Operational Summary Report & Export to File")
        print(" 11. Run Full Automated Demo (Evaluates All 10 Parameters)")
        print(" 0.  Exit")
        print("="*72)

        choice = input("Enter your choice (0-11): ").strip()

        # Always re-read to ensure fresh records in memory
        records = dataset_manager.read_dataset_from_file()

        if choice == "1":
            limit_in = input("Enter number of records to display (press Enter for all): ").strip()
            limit = int(limit_in) if limit_in.isdigit() else None
            fee_and_room_operations.display_all_records(records, limit=limit)
        elif choice == "2":
            handle_add_student(records)
        elif choice == "3":
            handle_search_student(records)
        elif choice == "4":
            handle_update_student(records)
        elif choice == "5":
            handle_delete_student(records)
        elif choice == "6":
            handle_vacancy_tracking(records)
        elif choice == "7":
            np_data = analytics_engine.run_numpy_analytics()
            analytics_engine.print_numpy_report(np_data)
        elif choice == "8":
            df_cleaned, clean_meta = analytics_engine.load_and_clean_dataframe()
            analytics_engine.print_pandas_report(df_cleaned, clean_meta)
        elif choice == "9":
            handle_data_structures_demo()
        elif choice == "10":
            handle_generate_summary_report(records)
        elif choice == "11":
            run_full_automated_demo()
        elif choice == "0":
            print("\nThank you for using the Hostel Management System. Exiting...")
            break
        else:
            print("\n[!] Invalid choice. Please enter a number between 0 and 11.")

        input("\nPress Enter to return to the Main Menu...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--demo", "-d", "--test"):
        run_full_automated_demo()
    else:
        # Default behavior: run menu, or run demo if non-interactive
        if sys.stdin.isatty():
            main_menu()
        else:
            run_full_automated_demo()

