import struct
import csv
import os
from pathlib import Path

def decode_turbo_real(bytes_data):
    """
    Decode Turbo Pascal/Delphi 48-bit real (6 bytes)
    Format: (-1)^s * (1.m) * 2^(exp-129)
    Byte 0: 8-bit exponent
    Bytes 1-5: 39-bit mantissa with sign bit
    """
    if len(bytes_data) != 6:
        return None

    exp_byte = bytes_data[0]
    mantissa_bytes = bytes_data[1:6]

    # Special case: exponent = 0 means the number is 0
    if exp_byte == 0:
        return -1.0  # Use -1 to indicate "no mark"

    # Convert mantissa bytes to integer (little-endian)
    mantissa_int = int.from_bytes(mantissa_bytes, 'little')

    # Extract sign bit (bit 39, which is bit 7 of the 5th byte)
    sign = 1 if (mantissa_int & 0x8000000000) == 0 else -1

    # Clear the sign bit to get the actual mantissa value
    mantissa_int = mantissa_int & 0x7FFFFFFFFF

    # Calculate the real exponent (bias is 129 for Turbo Pascal real)
    exponent = exp_byte - 129

    # The mantissa is normalized with implicit leading 1: (1.m)
    mantissa_value = 1.0 + (mantissa_int / (2.0 ** 39))

    # Calculate the floating point value: (-1)^s * (1.m) * 2^(exp-129)
    value = sign * mantissa_value * (2.0 ** exponent)

    return value

def read_pascal_string(f, max_len):
    """Read a Pascal-style string (length byte + characters)"""
    length = struct.unpack('B', f.read(1))[0]
    if length > max_len:
        length = max_len
    s = f.read(max_len).decode('latin-1', errors='replace')
    return s[:length].strip()

def read_config_file(config_path):
    """Read the .txt configuration file to get assignment details"""
    with open(config_path, 'r') as f:
        lines = f.readlines()

    # Parse version
    version = float(lines[0].strip())

    # Skip password and class info
    class_code = lines[2].strip()
    class_desc = lines[3].strip()

    # Get number of categories, marks, terms
    num_cat = int(lines[7].strip())
    num_marks = int(lines[8].strip())
    num_terms = int(lines[6].strip())

    # Parse category names and weights
    idx = 9
    categories = []
    for i in range(num_cat):
        cat_name = lines[idx].strip()
        cat_weight = float(lines[idx + 1].strip())
        categories.append((cat_name, cat_weight))
        idx += 2

    # Parse mark details
    marks = []
    for i in range(num_marks):
        mark_name = lines[idx].strip()
        mark_date = lines[idx + 1].strip()
        mark_desc = lines[idx + 2].strip()
        mark_total = float(lines[idx + 3].strip())
        mark_cat = int(lines[idx + 4].strip())
        mark_avg = float(lines[idx + 5].strip())
        marks.append({
            'name': mark_name,
            'date': mark_date,
            'desc': mark_desc,
            'total': mark_total,
            'category': mark_cat,
            'average': mark_avg
        })
        idx += 6

    return {
        'version': version,
        'class_code': class_code,
        'class_desc': class_desc,
        'num_cat': num_cat,
        'num_marks': num_marks,
        'num_terms': num_terms,
        'categories': categories,
        'marks': marks
    }

def read_student_record(f):
    """Read one studentrec40 record from the file"""
    # Read name (string[20])
    name = read_pascal_string(f, 20)

    # Read student number (string[10])
    studentno = read_pascal_string(f, 10)

    # Read homeform (string[10])
    homeform = read_pascal_string(f, 10)

    # Read marks array (100 reals - Delphi real = 6 bytes, 48-bit float)
    marks = []
    for i in range(100):
        real_bytes = f.read(6)
        mark = decode_turbo_real(real_bytes)
        marks.append(mark if mark is not None else 999.0)

    # Read category marks (10 reals)
    catmarks = []
    for i in range(10):
        real_bytes = f.read(6)
        catmark = decode_turbo_real(real_bytes)
        catmarks.append(catmark if catmark is not None else 999.0)

    # Read term marks (10 reals)
    termmarks = []
    for i in range(10):
        real_bytes = f.read(6)
        termmark = decode_turbo_real(real_bytes)
        termmarks.append(termmark if termmark is not None else 999.0)

    # Read final mark (real)
    real_bytes = f.read(6)
    finalmark = decode_turbo_real(real_bytes)
    if finalmark is None:
        finalmark = 999.0

    # Read telno (string[12])
    telno = read_pascal_string(f, 12)

    # Read absences (integer = 2 bytes)
    absences = struct.unpack('h', f.read(2))[0]

    # Read lates (integer = 2 bytes)
    lates = struct.unpack('h', f.read(2))[0]

    # Read comments (5 integers)
    comments = []
    for i in range(5):
        comment = struct.unpack('h', f.read(2))[0]
        comments.append(comment)

    return {
        'name': name,
        'studentno': studentno,
        'homeform': homeform,
        'marks': marks,
        'catmarks': catmarks,
        'termmarks': termmarks,
        'finalmark': finalmark,
        'telno': telno,
        'absences': absences,
        'lates': lates,
        'comments': comments
    }

def format_mark(m):
    """Format a mark for display"""
    if m < 0 or m >= 999:
        return ''
    return f'{m:.1f}'

def convert_class_to_csv(rec_file, txt_file, output_dir):
    """Convert a single class .rec file to CSV"""

    # Read configuration
    print(f"Processing {os.path.basename(rec_file)}...")
    config = read_config_file(txt_file)

    class_code = config['class_code']

    # Create CSV filename
    csv_filename = os.path.join(output_dir, f"{class_code}_marks.csv")
    csv_attendance = os.path.join(output_dir, f"{class_code}_attendance.csv")
    csv_transpose = os.path.join(output_dir, f"{class_code}_marks_transposed.csv")

    # Read all students
    students = []
    with open(rec_file, 'rb') as f:
        while True:
            try:
                student = read_student_record(f)
                if student['name']:  # Skip empty records
                    students.append(student)
            except:
                break

    if not students:
        print(f"  No students found in {rec_file}")
        return None

    # Write main marks CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        # Build header
        header = ['Student Name', 'Student Number', 'Homeform']

        # Add assignment columns
        for mark in config['marks']:
            header.append(f"{mark['name']} ({mark['date']})")

        # Add category columns
        for cat_name, cat_weight in config['categories']:
            header.append(f"{cat_name} %")

        # Add term columns
        for i in range(config['num_terms']):
            header.append(f"Term {i+1} %")

        header.append('Final Mark %')

        writer = csv.writer(f)
        writer.writerow(header)

        # Write student data
        for student in students:
            row = [student['name'], student['studentno'], student['homeform']]

            # Add assignment marks
            for i in range(config['num_marks']):
                row.append(format_mark(student['marks'][i]))

            # Add category marks
            for i in range(config['num_cat']):
                row.append(format_mark(student['catmarks'][i]))

            # Add term marks
            for i in range(config['num_terms']):
                row.append(format_mark(student['termmarks'][i]))

            row.append(format_mark(student['finalmark']))

            writer.writerow(row)

    print(f"  Created {csv_filename} ({len(students)} students)")

    # Write attendance CSV
    with open(csv_attendance, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Student Name', 'Student Number', 'Homeform', 'Phone', 'Absences', 'Lates'])

        for student in students:
            writer.writerow([
                student['name'],
                student['studentno'],
                student['homeform'],
                student['telno'],
                student['absences'] if student['absences'] >= 0 else '',
                student['lates'] if student['lates'] >= 0 else ''
            ])

    print(f"  Created {csv_attendance}")

    # Write transposed version (students as columns)
    with open(csv_transpose, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header row with student names
        header = ['Assignment']
        for student in students:
            header.append(student['name'])
        writer.writerow(header)

        # Assignment rows
        for i, mark in enumerate(config['marks']):
            row = [f"{mark['name']} ({mark['date']}) - {mark['total']} pts"]
            for student in students:
                row.append(format_mark(student['marks'][i]))
            writer.writerow(row)

        # Category rows
        for i, (cat_name, cat_weight) in enumerate(config['categories']):
            row = [f"{cat_name} % (weight: {cat_weight}%)"]
            for student in students:
                row.append(format_mark(student['catmarks'][i]))
            writer.writerow(row)

        # Term rows
        for i in range(config['num_terms']):
            row = [f"Term {i+1} %"]
            for student in students:
                row.append(format_mark(student['termmarks'][i]))
            writer.writerow(row)

        # Final mark row
        row = ['Final Mark %']
        for student in students:
            row.append(format_mark(student['finalmark']))
        writer.writerow(row)

    print(f"  Created {csv_transpose}")

    return {
        'class_code': class_code,
        'class_desc': config['class_desc'],
        'num_students': len(students),
        'num_marks': config['num_marks']
    }

def main():
    # Setup paths
    classes_dir = r'S:\Chn\classes'
    output_dir = r'S:\Chn\classes\csv_exports_corrected'

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}\n")

    # Find all .rec files
    rec_files = []
    for file in os.listdir(classes_dir):
        if file.endswith('.rec'):
            rec_path = os.path.join(classes_dir, file)
            txt_path = os.path.join(classes_dir, file.replace('.rec', '.txt'))
            if os.path.exists(txt_path):
                rec_files.append((rec_path, txt_path))

    print(f"Found {len(rec_files)} class files to convert\n")

    # Convert each class
    summary = []
    for rec_file, txt_file in rec_files:
        result = convert_class_to_csv(rec_file, txt_file, output_dir)
        if result:
            summary.append(result)
        print()

    # Write summary CSV
    summary_file = os.path.join(output_dir, '_summary.csv')
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Class Code', 'Class Description', 'Number of Students', 'Number of Assignments'])
        for item in summary:
            writer.writerow([item['class_code'], item['class_desc'], item['num_students'], item['num_marks']])

    print(f"Created summary file: {summary_file}")
    print(f"\nTotal classes converted: {len(summary)}")
    print(f"All CSV files saved to: {output_dir}")

if __name__ == '__main__':
    main()
