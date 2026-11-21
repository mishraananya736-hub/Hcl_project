"""
Module 3: analytics_engine.py
=============================
Implements:
1. NumPy Operations:
   - 1D and 2D arrays
   - Array indexing and slicing
   - Array sum, mean, maximum, minimum
   - Standard deviation calculation and dispersion analysis
2. Pandas Operations:
   - DataFrame creation and reading from CSV
   - Handling missing values (detection, fillna)
   - Displaying selected rows and columns
   - Data filtering and sorting
   - GroupBy operations (Room Type, Department, Fee Status)
   - Statistical analysis (df.describe(), aggregation)
3. Actionable Insights Generation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, List
from dataset_manager import DATA_FILE

# ---------------------------------------------------------------------------
# Requirement 4: NUMPY IMPLEMENTATION
# 1D/2D arrays, indexing, slicing, sum, mean, max, min, standard deviation
# ---------------------------------------------------------------------------

def run_numpy_analytics(csv_path: str = DATA_FILE) -> Dict[str, Any]:
    """
    Executes comprehensive NumPy operations on student fee data:
    1. 1D Array creation (Dues array)
    2. 2D Array creation (Financial Matrix: [Hostel_Tot, Hostel_Pd, Mess_Tot, Mess_Pd, Due])
    3. Indexing (extract specific row / specific column)
    4. Slicing (sub-matrix of top 10 students, fee columns)
    5. Mathematical aggregates (sum, mean, max, min)
    6. Standard Deviation calculation
    """
    # Load dataset using pandas or csv to feed clean numeric array to numpy
    df = pd.read_csv(csv_path)

    # Impute missing values with 0 for numerical computation
    df_clean = df.copy()
    df_clean["hostel_fee_paid"] = pd.to_numeric(df_clean["hostel_fee_paid"], errors="coerce").fillna(0)
    df_clean["mess_fee_paid"] = pd.to_numeric(df_clean["mess_fee_paid"], errors="coerce").fillna(0)
    df_clean["hostel_fee_total"] = pd.to_numeric(df_clean["hostel_fee_total"], errors="coerce").fillna(0)
    df_clean["mess_fee_total"] = pd.to_numeric(df_clean["mess_fee_total"], errors="coerce").fillna(0)

    # Calculate total due per record
    dues = (
        (df_clean["hostel_fee_total"] - df_clean["hostel_fee_paid"]) +
        (df_clean["mess_fee_total"] - df_clean["mess_fee_paid"])
    ).values

    # 1. NUMPY 1D ARRAY
    dues_1d_array: np.ndarray = np.array(dues, dtype=np.float64)

    # 2. NUMPY 2D ARRAY: Financial Matrix [Hostel_Total, Hostel_Paid, Mess_Total, Mess_Paid, Total_Dues]
    financial_matrix_2d: np.ndarray = np.column_stack((
        df_clean["hostel_fee_total"].values,
        df_clean["hostel_fee_paid"].values,
        df_clean["mess_fee_total"].values,
        df_clean["mess_fee_paid"].values,
        dues_1d_array
    ))

    # 3. ARRAY INDEXING
    # Indexing row 0 (First student's entire financial record)
    first_student_row = financial_matrix_2d[0]
    # Indexing column 4 (Dues column via indexing)
    dues_column = financial_matrix_2d[:, 4]
    # Specific element at [row 5, column 1] (Hostel fee paid by 6th student)
    single_element = financial_matrix_2d[5, 1]

    # 4. ARRAY SLICING
    # Slice first 5 students, only fee paid columns (Hostel Paid index 1, Mess Paid index 3)
    slice_top5_paid = financial_matrix_2d[0:5, [1, 3]]
    # Slice first 10 students, all financial columns
    slice_top10_all = financial_matrix_2d[:10, :]

    # 5. MATHEMATICAL AGGREGATES (sum, mean, max, min)
    total_dues_sum = float(np.sum(dues_1d_array))
    avg_due_per_student = float(np.mean(dues_1d_array))
    max_due = float(np.max(dues_1d_array))
    min_due = float(np.min(dues_1d_array))

    total_hostel_paid = float(np.sum(financial_matrix_2d[:, 1]))
    total_mess_paid = float(np.sum(financial_matrix_2d[:, 3]))

    # 6. STANDARD DEVIATION
    std_dev_dues = float(np.std(dues_1d_array))
    std_dev_hostel_paid = float(np.std(financial_matrix_2d[:, 1]))

    return {
        "1d_array_shape": dues_1d_array.shape,
        "2d_matrix_shape": financial_matrix_2d.shape,
        "first_student_row": first_student_row,
        "single_element_sample": single_element,
        "slice_top5_paid": slice_top5_paid,
        "slice_top10_shape": slice_top10_all.shape,
        "total_dues_sum": total_dues_sum,
        "avg_due_per_student": avg_due_per_student,
        "max_due": max_due,
        "min_due": min_due,
        "total_hostel_paid": total_hostel_paid,
        "total_mess_paid": total_mess_paid,
        "std_dev_dues": std_dev_dues,
        "std_dev_hostel_paid": std_dev_hostel_paid
    }


def print_numpy_report(analytics: Dict[str, Any]) -> None:
    """
    Renders formatted terminal output for NumPy calculations.
    """
    print("\n" + "="*70)
    print("             NUMPY IMPLEMENTATION & ANALYTICS REPORT")
    print("="*70)
    print(f"[*] 1D Array Created: Shape = {analytics['1d_array_shape']} (Student Total Dues)")
    print(f"[*] 2D Array Created: Shape = {analytics['2d_matrix_shape']} (Matrix: [H.Tot, H.Pd, M.Tot, M.Pd, Due])")
    print("\n--- Array Indexing Examples ---")
    print(f" - Student #1 Row (Index 0)       : {analytics['first_student_row']}")
    print(f" - Element at [Row 5, Col 1]     : Rs. {analytics['single_element_sample']:,.2f} (Hostel Fee Paid)")
    print("\n--- Array Slicing Examples ---")
    print(f" - Slicing Top 5 Students [Hostel Paid, Mess Paid]:\n{analytics['slice_top5_paid']}")
    print(f" - Slicing Top 10 Sub-Matrix Shape : {analytics['slice_top10_shape']}")
    print("\n--- Mathematical Aggregations ---")
    print(f" - Total Outstanding Dues (sum)  : Rs. {analytics['total_dues_sum']:,.2f}")
    print(f" - Average Outstanding Due (mean): Rs. {analytics['avg_due_per_student']:,.2f}")
    print(f" - Maximum Outstanding Due (max) : Rs. {analytics['max_due']:,.2f}")
    print(f" - Minimum Outstanding Due (min) : Rs. {analytics['min_due']:,.2f}")
    print(f" - Total Hostel Fee Paid (sum)   : Rs. {analytics['total_hostel_paid']:,.2f}")
    print(f" - Total Mess Fee Paid (sum)     : Rs. {analytics['total_mess_paid']:,.2f}")
    print("\n--- Standard Deviation Analysis ---")
    print(f" - Std Dev of Outstanding Dues   : Rs. {analytics['std_dev_dues']:,.2f}")
    print(f" - Std Dev of Hostel Paid Fees   : Rs. {analytics['std_dev_hostel_paid']:,.2f}")
    print(f"   [Insight] High standard deviation (Rs. {analytics['std_dev_dues']:,.2f}) indicates significant disparity")
    print(f"   between fully cleared students and pending fee defaulters.")
    print("="*70 + "\n")


# ---------------------------------------------------------------------------
# Requirement 5: PANDAS IMPLEMENTATION
# DataFrame, read CSV, missing values, filter & sort, GroupBy, statistical analysis
# ---------------------------------------------------------------------------

def load_and_clean_dataframe(csv_path: str = DATA_FILE) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Pandas Operation:
    - Reads CSV into DataFrame
    - Detects missing values
    - Handles missing values via imputation
    - Calculates derived columns: total_fee, total_paid, total_dues
    """
    # 1. Read CSV into DataFrame
    df_raw = pd.read_csv(csv_path)

    # 2. Detect missing values
    missing_before = df_raw.isna().sum().to_dict()

    # 3. Handle missing values
    df_cleaned = df_raw.copy()
    
    # Impute missing room numbers with 'Unassigned'
    df_cleaned["room_no"] = df_cleaned["room_no"].fillna("Unassigned")
    
    # Impute missing mess_fee_paid with median paid fee or 0
    median_mess_fee = df_cleaned["mess_fee_paid"].median()
    df_cleaned["mess_fee_paid"] = df_cleaned["mess_fee_paid"].fillna(0)
    
    # Impute missing hostel_fee_paid with 0
    df_cleaned["hostel_fee_paid"] = df_cleaned["hostel_fee_paid"].fillna(0)

    # Convert numeric columns safely
    numeric_cols = ["hostel_fee_total", "hostel_fee_paid", "mess_fee_total", "mess_fee_paid", "year"]
    for col in numeric_cols:
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce").fillna(0)

    # 4. Create calculated fields
    df_cleaned["total_fee"] = df_cleaned["hostel_fee_total"] + df_cleaned["mess_fee_total"]
    df_cleaned["total_paid"] = df_cleaned["hostel_fee_paid"] + df_cleaned["mess_fee_paid"]
    df_cleaned["total_dues"] = df_cleaned["total_fee"] - df_cleaned["total_paid"]

    missing_after = df_cleaned.isna().sum().to_dict()

    cleaning_metadata = {
        "raw_record_count": len(df_raw),
        "cleaned_record_count": len(df_cleaned),
        "missing_before": missing_before,
        "missing_after": missing_after,
        "imputed_mess_median_reference": median_mess_fee
    }

    return df_cleaned, cleaning_metadata


def pandas_filtering_and_sorting(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Pandas Operation:
    - Display selected rows and columns
    - Data filtering (defaulters, room types, pending status)
    - Data sorting (by total dues descending, by department & name)
    """
    # Selected Rows and Columns (loc and iloc)
    selected_cols = ["student_id", "name", "department", "room_no", "room_type", "total_dues", "fee_status"]
    
    # Filtering 1: Students with high outstanding dues (> Rs. 20,000)
    high_defaulters = df[df["total_dues"] > 20000][selected_cols].sort_values(by="total_dues", ascending=False)

    # Filtering 2: Single AC room students
    single_ac_residents = df[df["room_type"] == "Single AC"][selected_cols].sort_values(by="student_id")

    # Filtering 3: Complete Defaulters (Status == 'Pending')
    zero_paid_students = df[df["fee_status"] == "Pending"][selected_cols]

    # Sorting: Top 10 fee dues across entire hostel
    top_dues_sorted = df.sort_values(by="total_dues", ascending=False)[selected_cols].head(10)

    return {
        "high_defaulters": high_defaulters,
        "single_ac_residents": single_ac_residents,
        "zero_paid_students": zero_paid_students,
        "top_dues_sorted": top_dues_sorted
    }


def pandas_groupby_analysis(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Pandas Operation:
    - GroupBy Room Type (student count, total fee expected, total fee paid, avg dues)
    - GroupBy Department (student count, total dues, fee recovery rate)
    - GroupBy Fee Status (count, total dues sum)
    """
    # 1. GroupBy Room Type
    room_type_summary = df.groupby("room_type").agg(
        student_count=("student_id", "count"),
        avg_hostel_fee=("hostel_fee_total", "mean"),
        total_collected=("total_paid", "sum"),
        total_dues=("total_dues", "sum")
    ).reset_index()

    # 2. GroupBy Department
    dept_summary = df.groupby("department").agg(
        student_count=("student_id", "count"),
        total_expected=("total_fee", "sum"),
        total_collected=("total_paid", "sum"),
        total_dues=("total_dues", "sum")
    ).reset_index()
    dept_summary["recovery_rate_pct"] = (dept_summary["total_collected"] / dept_summary["total_expected"] * 100).round(2)

    # 3. GroupBy Fee Status
    status_summary = df.groupby("fee_status").agg(
        student_count=("student_id", "count"),
        total_dues=("total_dues", "sum"),
        avg_due_per_student=("total_dues", "mean")
    ).reset_index()

    return {
        "room_type_summary": room_type_summary,
        "dept_summary": dept_summary,
        "status_summary": status_summary
    }


def pandas_statistical_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pandas Operation:
    - Generates descriptive statistics using describe() on numeric financial columns
    """
    numeric_cols = ["hostel_fee_total", "hostel_fee_paid", "mess_fee_total", "mess_fee_paid", "total_dues"]
    return df[numeric_cols].describe()


# ---------------------------------------------------------------------------
# Requirement 9: MEANINGFUL DATA INSIGHTS
# Combines NumPy & Pandas results into actionable managerial insights
# ---------------------------------------------------------------------------

def generate_actionable_insights(df: pd.DataFrame) -> List[str]:
    """
    Generates meaningful insights from the dataset.
    """
    total_students = len(df)
    total_expected = df["total_fee"].sum()
    total_collected = df["total_paid"].sum()
    total_dues = df["total_dues"].sum()
    collection_rate = (total_collected / total_expected * 100) if total_expected > 0 else 0

    defaulters_count = len(df[df["total_dues"] > 0])
    defaulter_percentage = (defaulters_count / total_students * 100) if total_students > 0 else 0

    # Department with lowest recovery
    dept_grp = df.groupby("department").agg(
        total_expected=("total_fee", "sum"),
        total_collected=("total_paid", "sum")
    )
    dept_grp["rate"] = dept_grp["total_collected"] / dept_grp["total_expected"] * 100
    worst_dept = dept_grp["rate"].idxmin()
    worst_rate = dept_grp["rate"].min()
    best_dept = dept_grp["rate"].idxmax()
    best_rate = dept_grp["rate"].max()

    # Most demanded room type
    popular_room = df["room_type"].mode()[0]
    popular_room_count = (df["room_type"] == popular_room).sum()

    insights = [
        f"1. Overall Fee Recovery Rate: {collection_rate:.2f}% (Rs. {total_collected:,.2f} collected out of Rs. {total_expected:,.2f}).",
        f"2. Outstanding Defaulters: {defaulters_count} out of {total_students} students ({defaulter_percentage:.1f}%) have unpaid dues.",
        f"3. Department Performance: '{best_dept}' has highest fee compliance at {best_rate:.2f}%, while '{worst_dept}' has lowest compliance at {worst_rate:.2f}%.",
        f"4. Room Type Preference: '{popular_room}' is the most occupied configuration with {popular_room_count} student residents.",
        f"5. Total Hostel Fee Balance: Outstanding mess & hostel dues total Rs. {total_dues:,.2f}; recovery notices should be prioritized for students with > Rs. 20,000 due."
    ]
    return insights


def print_pandas_report(df: pd.DataFrame, clean_meta: Dict[str, Any]) -> None:
    """
    Renders formatted terminal output for Pandas operations.
    """
    print("\n" + "="*70)
    print("             PANDAS IMPLEMENTATION & DATA ANALYSIS")
    print("="*70)
    print("[*] DataFrame Successfully Loaded from CSV.")
    print(f"    - Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
    
    print("\n--- Missing Value Detection & Handling ---")
    print("    - Missing values before cleaning:")
    for col, count in clean_meta["missing_before"].items():
        if count > 0:
            print(f"      * {col}: {count} missing records")
    print("    - Strategy applied: room_no filled with 'Unassigned'; fee dues imputed with 0.0.")
    print(f"    - Missing values after cleaning: {sum(clean_meta['missing_after'].values())} remaining.")

    # Filter & Sort
    fs_results = pandas_filtering_and_sorting(df)
    print("\n--- Data Filtering & Sorting: Top 5 Fee Defaulters ---")
    print(fs_results["high_defaulters"].head(5).to_string(index=False))

    # GroupBy
    grp_results = pandas_groupby_analysis(df)
    print("\n--- GroupBy Operation: Summary by Room Type ---")
    print(grp_results["room_type_summary"].to_string(index=False))

    print("\n--- GroupBy Operation: Fee Recovery by Department ---")
    print(grp_results["dept_summary"].to_string(index=False))

    # Statistical Analysis
    stats_df = pandas_statistical_analysis(df)
    print("\n--- Statistical Analysis (describe()) ---")
    print(stats_df.round(2).to_string())

    # Insights
    insights = generate_actionable_insights(df)
    print("\n--- Meaningful Actionable Insights ---")
    for ins in insights:
        print(f"    {ins}")
    print("="*70 + "\n")


# ---------------------------------------------------------------------------
# DATA VISUALIZATIONS (4 GRAPHS USING MATPLOTLIB)
# Graph 1: Bar Graph - Room Allocation (Students per Room Type)
# Graph 2: Pie Chart - Hostel Fee Status Distribution (Paid, Partial, Pending)
# Graph 3: Bar Graph - Total Outstanding Dues by Department
# Graph 4: Histogram - Distribution of Student Dues
# Bonus:   Combined 2x2 Dashboard
# ---------------------------------------------------------------------------

def generate_visualizations(df: pd.DataFrame, show: bool = False) -> List[str]:
    """
    Generates 4 graphs from the hostel dataset using standard Matplotlib functions:
    - plt.bar()
    - plt.pie()
    - plt.hist()
    - Combined 2x2 dashboard
    Saves image files to project folder.
    """
    saved_files = []

    # Graph 1: Bar Graph - Room Allocation (Number of students per room type)
    plt.figure(figsize=(7, 4.5))
    room_counts = df["room_type"].value_counts()
    plt.bar(room_counts.index, room_counts.values, color="steelblue", edgecolor="black")
    plt.title("Graph 1: Students Count by Room Type")
    plt.xlabel("Room Type")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    g1_path = "graph1_room_allocation.png"
    plt.savefig(g1_path, dpi=300)
    saved_files.append(g1_path)
    if show:
        plt.show()
    plt.close()

    # Graph 2: Pie Chart - Fee Status Distribution (Paid, Partial, Pending)
    plt.figure(figsize=(6, 6))
    status_counts = df["fee_status"].value_counts()
    colors = ["#4CAF50", "#FFC107", "#F44336"]
    plt.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title("Graph 2: Fee Status Distribution")
    plt.tight_layout()
    g2_path = "graph2_fee_status_distribution.png"
    plt.savefig(g2_path, dpi=300)
    saved_files.append(g2_path)
    if show:
        plt.show()
    plt.close()

    # Graph 3: Bar Graph - Total Outstanding Dues by Department
    plt.figure(figsize=(7, 4.5))
    dept_dues = df.groupby("department")["total_dues"].sum()
    plt.bar(dept_dues.index, dept_dues.values, color="coral", edgecolor="black")
    plt.title("Graph 3: Total Outstanding Dues by Department")
    plt.xlabel("Department")
    plt.ylabel("Total Dues (Rs.)")
    plt.tight_layout()
    g3_path = "graph3_department_dues.png"
    plt.savefig(g3_path, dpi=300)
    saved_files.append(g3_path)
    if show:
        plt.show()
    plt.close()

    # Graph 4: Histogram - Distribution of Student Outstanding Dues
    plt.figure(figsize=(7, 4.5))
    plt.hist(df["total_dues"], bins=10, color="mediumpurple", edgecolor="black")
    plt.title("Graph 4: Distribution of Student Outstanding Dues")
    plt.xlabel("Dues Amount (Rs.)")
    plt.ylabel("Frequency (Number of Students)")
    plt.tight_layout()
    g4_path = "graph4_dues_distribution.png"
    plt.savefig(g4_path, dpi=300)
    saved_files.append(g4_path)
    if show:
        plt.show()
    plt.close()

    # Combined Dashboard: All 4 graphs in a single 2x2 grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1
    axes[0, 0].bar(room_counts.index, room_counts.values, color="steelblue", edgecolor="black")
    axes[0, 0].set_title("1. Room Allocation by Type")
    axes[0, 0].set_xlabel("Room Type")
    axes[0, 0].set_ylabel("Student Count")
    axes[0, 0].tick_params(axis="x", rotation=15)

    # Subplot 2
    axes[0, 1].pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", colors=colors, startangle=140)
    axes[0, 1].set_title("2. Fee Status Distribution")

    # Subplot 3
    axes[1, 0].bar(dept_dues.index, dept_dues.values, color="coral", edgecolor="black")
    axes[1, 0].set_title("3. Total Dues by Department")
    axes[1, 0].set_xlabel("Department")
    axes[1, 0].set_ylabel("Total Dues (Rs.)")

    # Subplot 4
    axes[1, 1].hist(df["total_dues"], bins=10, color="mediumpurple", edgecolor="black")
    axes[1, 1].set_title("4. Distribution of Dues")
    axes[1, 1].set_xlabel("Dues Amount (Rs.)")
    axes[1, 1].set_ylabel("Number of Students")

    plt.suptitle("Hostel Room Allocation & Fee Management Dashboard", fontsize=16, fontweight="bold")
    plt.tight_layout()
    dashboard_path = "graph_all_4_combined.png"
    plt.savefig(dashboard_path, dpi=300)
    saved_files.append(dashboard_path)
    if show:
        plt.show()
    plt.close()

    return saved_files

