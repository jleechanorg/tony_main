"""
Display class marks in spreadsheet format
"""

import sys
import csv


def display_class_spreadsheet(class_code, csv_dir=r'S:\Chn\classes\csv_exports_python'):
    """Display a class in spreadsheet format"""

    csv_file = f"{csv_dir}\\{class_code}_marks.csv"

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    students = rows[1:]

    # Parse header to find sections
    name_idx = 0
    id_idx = 1
    hf_idx = 2

    # Find where assignments end and categories begin
    assignment_end = 0
    for i, col in enumerate(header):
        if '%' in col:
            assignment_end = i
            break

    assignments = header[3:assignment_end]
    categories = header[assignment_end:]

    # Print class header
    print("=" * 200)
    print(f"{class_code} - COMPLETE MARKS SPREADSHEET")
    print("=" * 200)
    print()

    # Print header row
    print(f"{'Student Name':<25} {'ID':<12} {'HF':<5}", end='')

    # Print assignment headers (shortened)
    for assign in assignments:
        col_name = assign.split('(')[0].strip()
        print(f"{col_name:>7}", end='')

    # Print category headers
    for cat in categories:
        col_name = cat.replace(' %', '').strip()
        print(f"{col_name:>8}", end='')

    print()
    print("-" * 200)

    # Print each student row
    for student in students:
        # Name, ID, Homeform
        print(f"{student[name_idx]:<25} {student[id_idx]:<12} {student[hf_idx]:<5}", end='')

        # Assignment marks
        for i in range(3, assignment_end):
            mark = student[i]
            if mark:
                print(f"{mark:>7}", end='')
            else:
                print(f"{'--':>7}", end='')

        # Category and final marks
        for i in range(assignment_end, len(header)):
            mark = student[i]
            if mark:
                print(f"{mark:>8}", end='')
            else:
                print(f"{'--':>8}", end='')

        print()

    print("=" * 200)
    print()

    # Print legend
    print("Legend:")
    print("  HF = Homeform")
    print("  All marks shown to 1 decimal place")
    print()


if __name__ == '__main__':
    class_code = sys.argv[1] if len(sys.argv) > 1 else 'TIK2O1-1'
    display_class_spreadsheet(class_code)
