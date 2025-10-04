import csv

# Read the CSV file
with open(r'S:\Chn\classes\csv_exports_corrected\ICS4M1-1_marks.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Print header
print('=' * 200)
print('ICS4M1-1 - CS 12 - PERIOD 3 - COMPLETE MARKS SPREADSHEET')
print('=' * 200)
print()

# Print column headers
header = rows[0]
print(f"{'Student Name':<20} {'ID':<10} {'HF':<4} ", end='')
for i in range(3, 18):  # Assignment columns
    col = header[i].split('(')[0].strip()
    print(f"{col:>6}", end=' ')
print(f"{'TESTS':>6} {'ASSN':>6} {'NOTE':>6} {'EXAM':>6} {'PROJ':>6} {'TERM':>6} {'FINAL':>6}")

print('-' * 200)

# Print each student's data
for row in rows[1:]:
    if not row[0]:  # Skip empty rows
        continue

    name = row[0][:20]
    student_id = row[1]
    homeform = row[2]

    print(f"{name:<20} {student_id:<10} {homeform:<4} ", end='')

    # Print assignment marks (columns 3-17)
    for i in range(3, 18):
        mark = row[i] if row[i] else '--'
        if mark != '--':
            try:
                mark = f"{float(mark):.1f}"
            except:
                pass
        print(f"{mark:>6}", end=' ')

    # Print category marks (columns 18-22)
    for i in range(18, 23):
        mark = row[i] if row[i] else '--'
        if mark != '--':
            try:
                mark = f"{float(mark):.1f}"
            except:
                pass
        print(f"{mark:>6}", end=' ')

    # Print term and final (columns 23-24)
    for i in range(23, 25):
        mark = row[i] if row[i] else '--'
        if mark != '--':
            try:
                mark = f"{float(mark):.1f}"
            except:
                pass
        print(f"{mark:>6}", end=' ')

    print()

print('=' * 200)
print()
print('Legend:')
print('  HF = Homeform')
print('  TESTS = Tests Category %')
print('  ASSN = Assignments Category %')
print('  NOTE = Notebook Category %')
print('  EXAM = Dec Exam Category %')
print('  PROJ = Final Project Category %')
print('  TERM = Term 1 Mark %')
print('  FINAL = Final Mark %')
print()
print('Assignment Point Values:')
print('  A1=20, Q1=11, A2=3, T1=35, N1=8, A3=10, A4=30, E1=78, A5=40, N2=8, Q2=10, T2=31, A6=20, C1=40, C2=40')
print()
print('Category Weights:')
print('  TESTS=25%, ASSIGN=20%, NOTEBOOK=10%, DEC EXAM=15%, FINAL PROJ=30%')
