# Hostel Room Allocation and Fee Management System

A Python-based system designed to manage student hostel room allocations, room vacancies, mess fees, and hostel dues. Built with core **Python Data Structures**, **File Handling**, **NumPy**, and **Pandas** for high-performance financial analytics and reporting.

---

## 📌 Compliance with Mandatory Technical Parameters

| # | Mandatory Parameter | Implementation Details | Source Module |
|---|---|---|---|
| **1** | **Dataset Creation** (Min. 50 records) | Generated **60 realistic student records** with diverse fields (`student_id`, `name`, `gender`, `department`, `year`, `room_no`, `room_type`, `hostel_fee_total`, `hostel_fee_paid`, `mess_fee_total`, `mess_fee_paid`, `fee_status`). Contains intentional missing entries for cleaning tests. | `data/hostel_students.csv`, `dataset_manager.py` |
| **2** | **Python Data Structures** (5+ Concepts) | • **List & List Methods**: `append()`, `extend()`, `pop()`, `sort()`, slicing `[1:4]`<br>• **Dictionary & Dict Methods**: `keys()`, `values()`, `items()`, `get()`, `update()`<br>• **Set & Set Operations**: `union()`, `intersection()`, `difference()` for room vacancy tracking<br>• **Tuples**: Immutable room specifications catalog `ROOM_SPEC_CATALOG` & tuple unpacking<br>• **Nested Structures**: List of Dictionaries database | `dataset_manager.py`, `fee_and_room_operations.py` |
| **3** | **User-Defined Functions** (Min. 5) | Over 15 modular functions with type hints and docstrings: `calculate_fee_dues()`, `get_room_spec()`, `track_room_occupancy_and_vacancies()`, `allocate_room_to_student()`, `add_student_record()`, `display_all_records()`, `search_student_records()`, `update_student_record()`, `delete_student_record()`, `generate_operational_summary()`, etc. | `fee_and_room_operations.py`, `analytics_engine.py` |
| **4** | **NumPy Implementation** | • **1D Array**: Student fee dues array<br>• **2D Array**: Financial Matrix (`[H.Total, H.Paid, M.Total, M.Paid, Dues]`)<br>• **Indexing**: Row extraction `matrix[0]`, element extraction `matrix[5, 1]`<br>• **Slicing**: Sub-matrix of top 5 students `matrix[0:5, [1, 3]]`<br>• **Aggregations**: `np.sum()`, `np.mean()`, `np.max()`, `np.min()`<br>• **Standard Deviation**: `np.std(dues)` with dispersion analysis | `analytics_engine.py` |
| **5** | **Pandas Implementation** | • **DataFrame Creation**: Reading from CSV via `pd.read_csv()`<br>• **Selected Rows/Columns**: Projection of specific columns using `loc`/`iloc`<br>• **Filtering & Sorting**: Filtering students by dues > 20,000, sorting by dues descending<br>• **GroupBy Operations**: Aggregation by `room_type`, `department`, and `fee_status`<br>• **Missing Values**: Detected using `isna().sum()`, imputed using `fillna()`<br>• **Statistical Analysis**: `df.describe()` for all numerical fee columns | `analytics_engine.py` |
| **6** | **Python Modules** (Min. 3 Modules) | **1.** `dataset_manager.py`<br>**2.** `fee_and_room_operations.py`<br>**3.** `analytics_engine.py`<br>Main Controller: `project.py` | Project root |
| **7** | **File Handling** | Dataset reading/writing via standard `open()`, `csv.DictReader`, and `csv.DictWriter`. Analytical summary report exported to `hostel_summary_report.txt`. | `dataset_manager.py` |
| **8** | **Project Functionality** | • **Add**: Add student record with fee validation<br>• **Display**: Formatted ASCII table of student records<br>• **Search**: By ID, Name, Department, Room, Fee Status, or Universal<br>• **Update**: Update room, fees, department with automatic status recalculation<br>• **Delete**: Delete record by ID<br>• **Summary Report**: Fee and occupancy overview | `fee_and_room_operations.py`, `project.py` |
| **9** | **Data Analysis & Insights** | Meaningful insights generated: Fee recovery rates, department compliance ranking, defaulter percentages, room type demand trends. | `analytics_engine.py` |
| **10** | **Output Presentation** | Clean, formatted CLI terminal output with tables, dividers, and intuitive navigation. | `project.py` |

---

## 📂 Project Architecture

```
Hcl_project/
├── data/
│   └── hostel_students.csv        # 60 records dataset
├── dataset_manager.py             # Module 1: File handling, Seed dataset, Data structures demo
├── fee_and_room_operations.py     # Module 2: CRUD, Room allocation, Vacancy tracking & fee logic
├── analytics_engine.py            # Module 3: NumPy & Pandas analytics, cleaning, groupby, stats
├── project.py                     # Main CLI Application & Automated Demonstration
├── hostel_summary_report.txt      # Exported operational report file
└── README.md                      # Project documentation and parameters mapping
```

---

## 🚀 How to Run the Project

### Option A: Run the Automated Evaluation Mode
To evaluate all 10 mandatory parameters in one shot:
```powershell
python project.py --demo
```

### Option B: Run the Interactive Menu
To use the interactive CLI interface:
```powershell
python project.py
```

### Interactive Menu Options:
1. **Display All Student Records**
2. **Add New Student Record**
3. **Search for a Student Record**
4. **Update an Existing Student Record**
5. **Delete a Student Record**
6. **Room Vacancy & Allocation Tracking (Sets & Dicts)**
7. **NumPy Implementation & Analytics (1D/2D, Slicing, Stats, Std Dev)**
8. **Pandas Implementation & Analysis (DataFrame, Cleaning, Filter, GroupBy)**
9. **Python Data Structures Demonstration (List, Dict, Set, Tuple)**
10. **Generate Operational Summary Report & Export to File**
11. **Run Full Automated Demo (Evaluates All 10 Parameters)**
0. **Exit**
