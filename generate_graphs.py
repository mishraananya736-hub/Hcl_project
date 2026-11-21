"""
Standalone Graph Generator Script: generate_graphs.py
====================================================
Generates 4 graphs for the Hostel Room Allocation and Fee Management System
using standard Matplotlib functions and existing dataset columns:

Graph 1: Bar Chart   - Students per Room Type (room_type)
Graph 2: Pie Chart   - Fee Status Distribution (fee_status: Paid, Partial, Pending)
Graph 3: Bar Chart   - Total Outstanding Dues by Department (department & total_dues)
Graph 4: Histogram   - Distribution of Student Dues (total_dues)
Bonus:   Combined 2x2 Dashboard of all 4 graphs in one image!
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics_engine import load_and_clean_dataframe

def main():
    print("="*65)
    print("   GENERATING 4 MATPLOTLIB GRAPHS FOR HOSTEL DATASET")
    print("="*65)

    # 1. Load cleaned data using existing function
    df, _ = load_and_clean_dataframe()
    print(f"[*] Loaded dataset with {len(df)} records.\n")

    # -------------------------------------------------------------
    # GRAPH 1: Bar Chart - Room Allocation (Students per Room Type)
    # -------------------------------------------------------------
    print("[1/4] Generating Graph 1: Bar Chart (Room Type vs Student Count)...")
    plt.figure(figsize=(7, 4.5))
    room_counts = df["room_type"].value_counts()
    plt.bar(room_counts.index, room_counts.values, color="steelblue", edgecolor="black")
    plt.title("Graph 1: Student Count by Room Type")
    plt.xlabel("Room Type")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    g1_file = "graph1_room_allocation.png"
    plt.savefig(g1_file, dpi=300)
    plt.close()
    print(f"      Saved: {g1_file}")

    # -------------------------------------------------------------
    # GRAPH 2: Pie Chart - Fee Status Distribution
    # -------------------------------------------------------------
    print("[2/4] Generating Graph 2: Pie Chart (Fee Status Distribution)...")
    plt.figure(figsize=(6, 6))
    status_counts = df["fee_status"].value_counts()
    colors = ["#4CAF50", "#FFC107", "#F44336"]  # Green (Paid), Amber (Partial), Red (Pending)
    plt.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title("Graph 2: Fee Status Distribution (Paid / Partial / Pending)")
    plt.tight_layout()
    g2_file = "graph2_fee_status_distribution.png"
    plt.savefig(g2_file, dpi=300)
    plt.close()
    print(f"      Saved: {g2_file}")

    # -------------------------------------------------------------
    # GRAPH 3: Bar Chart - Total Dues by Department
    # -------------------------------------------------------------
    print("[3/4] Generating Graph 3: Bar Chart (Department-wise Dues)...")
    plt.figure(figsize=(7, 4.5))
    dept_dues = df.groupby("department")["total_dues"].sum()
    plt.bar(dept_dues.index, dept_dues.values, color="coral", edgecolor="black")
    plt.title("Graph 3: Total Outstanding Dues by Department")
    plt.xlabel("Department")
    plt.ylabel("Total Dues (in Rs.)")
    plt.tight_layout()
    g3_file = "graph3_department_dues.png"
    plt.savefig(g3_file, dpi=300)
    plt.close()
    print(f"      Saved: {g3_file}")

    # -------------------------------------------------------------
    # GRAPH 4: Histogram - Distribution of Student Outstanding Dues
    # -------------------------------------------------------------
    print("[4/4] Generating Graph 4: Histogram (Outstanding Dues Distribution)...")
    plt.figure(figsize=(7, 4.5))
    plt.hist(df["total_dues"], bins=10, color="mediumpurple", edgecolor="black")
    plt.title("Graph 4: Distribution of Student Outstanding Dues")
    plt.xlabel("Dues Amount (in Rs.)")
    plt.ylabel("Frequency (Number of Students)")
    plt.tight_layout()
    g4_file = "graph4_dues_distribution.png"
    plt.savefig(g4_file, dpi=300)
    plt.close()
    print(f"      Saved: {g4_file}")

    # -------------------------------------------------------------
    # COMBINED DASHBOARD: 2x2 Grid of all 4 Graphs
    # -------------------------------------------------------------
    print("[*] Generating Combined 2x2 Dashboard of all 4 Graphs...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Panel 1: Room Allocation Bar Chart
    axes[0, 0].bar(room_counts.index, room_counts.values, color="steelblue", edgecolor="black")
    axes[0, 0].set_title("1. Room Allocation (Students per Room Type)")
    axes[0, 0].set_xlabel("Room Type")
    axes[0, 0].set_ylabel("Student Count")
    axes[0, 0].tick_params(axis="x", rotation=15)

    # Panel 2: Fee Status Pie Chart
    axes[0, 1].pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", colors=colors, startangle=140)
    axes[0, 1].set_title("2. Fee Status Distribution")

    # Panel 3: Department Dues Bar Chart
    axes[1, 0].bar(dept_dues.index, dept_dues.values, color="coral", edgecolor="black")
    axes[1, 0].set_title("3. Outstanding Dues by Department")
    axes[1, 0].set_xlabel("Department")
    axes[1, 0].set_ylabel("Total Dues (in Rs.)")

    # Panel 4: Dues Distribution Histogram
    axes[1, 1].hist(df["total_dues"], bins=10, color="mediumpurple", edgecolor="black")
    axes[1, 1].set_title("4. Distribution of Outstanding Dues")
    axes[1, 1].set_xlabel("Dues Amount (in Rs.)")
    axes[1, 1].set_ylabel("Number of Students")

    plt.suptitle("Hostel Room Allocation & Fee Management Dashboard", fontsize=16, fontweight="bold")
    plt.tight_layout()
    dashboard_file = "graph_all_4_combined.png"
    plt.savefig(dashboard_file, dpi=300)
    plt.close()
    print(f"      Saved: {dashboard_file}")

    print("\n" + "="*65)
    print("   ALL 4 GRAPHS + DASHBOARD GENERATED SUCCESSFULLY!")
    print("="*65)
    print("Generated Image Files:")
    print(f" 1. {g1_file}         (Bar Chart: Students per Room Type)")
    print(f" 2. {g2_file} (Pie Chart: Fee Status Distribution)")
    print(f" 3. {g3_file}       (Bar Chart: Outstanding Dues by Dept)")
    print(f" 4. {g4_file}       (Histogram: Distribution of Dues)")
    print(f" 5. {dashboard_file}     (Combined 2x2 Full Visual Dashboard)")
    print("="*65 + "\n")

if __name__ == "__main__":
    main()
