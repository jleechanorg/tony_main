import struct
import sys

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
    # So we add 1.0 to the fractional part
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
    # Line 4 (index 4) has some number
    # Line 7 (index 7) has num categories
    # Line 8 (index 8) has num marks
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

def format_mark(mark):
    """Format a mark for display"""
    if mark < 0 or mark >= 999:
        return '__'
    return f'{mark:.1f}'

def main():
    rec_file = r'S:\Chn\classes\Ics4m1-1.rec'
    txt_file = r'S:\Chn\classes\Ics4m1-1.txt'

    # Read configuration
    print("Reading configuration...")
    config = read_config_file(txt_file)

    print(f"\n{'='*80}")
    print(f"Class: {config['class_code']} - {config['class_desc']}")
    print(f"Version: {config['version']}")
    print(f"{'='*80}\n")

    # Display categories
    print("CATEGORIES:")
    for i, (name, weight) in enumerate(config['categories'], 1):
        print(f"  {i}. {name:12s} - Weight: {weight:.1f}%")
    print()

    # Display assignments
    print("ASSIGNMENTS:")
    for i, mark in enumerate(config['marks'], 1):
        cat_name = config['categories'][mark['category']-1][0] if mark['category'] > 0 else 'N/A'
        print(f"  {i:2d}. {mark['name']:4s} - {mark['date']:10s} - {mark['desc']:30s} - {mark['total']:5.1f} pts - Cat: {cat_name}")
    print()

    # Read student records
    print("STUDENT RECORDS:")
    print(f"{'='*80}\n")

    with open(rec_file, 'rb') as f:
        student_num = 0
        while True:
            try:
                student = read_student_record(f)
                student_num += 1

                # Skip empty records
                if not student['name']:
                    continue

                print(f"Student #{student_num}: {student['name']}")
                print(f"  Student No: {student['studentno']}")
                print(f"  Homeform:   {student['homeform']}")
                print(f"  Phone:      {student['telno']}")
                print(f"  Absences:   {student['absences']}")
                print(f"  Lates:      {student['lates']}")
                print()

                # Display assignment marks
                print("  Assignment Marks:")
                for i in range(config['num_marks']):
                    mark_info = config['marks'][i]
                    mark_val = student['marks'][i]
                    print(f"    {mark_info['name']:4s} ({mark_info['date']:10s}): {format_mark(mark_val):>5s} / {mark_info['total']:.1f}")
                print()

                # Display category marks
                print("  Category Marks:")
                for i in range(config['num_cat']):
                    cat_name = config['categories'][i][0]
                    cat_mark = student['catmarks'][i]
                    print(f"    {cat_name:12s}: {format_mark(cat_mark):>5s}%")
                print()

                # Display term marks
                if config['num_terms'] > 0:
                    print("  Term Marks:")
                    for i in range(config['num_terms']):
                        term_mark = student['termmarks'][i]
                        if term_mark > 0 and term_mark < 999:
                            print(f"    Term {i+1}: {format_mark(term_mark):>5s}%")
                    print()

                # Display final mark
                print(f"  FINAL MARK: {format_mark(student['finalmark'])}%")
                print(f"\n{'-'*80}\n")

            except Exception as e:
                # End of file or error
                break

    print(f"\nTotal students read: {student_num}")

if __name__ == '__main__':
    main()
