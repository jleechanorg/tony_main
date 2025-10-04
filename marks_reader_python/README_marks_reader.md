# Marks Reader - Python Implementation

Complete Python implementation of the Pascal gradebook reader with full test coverage.

## Overview

This is a Python port of the original Delphi/Turbo Pascal gradebook system. It reads binary `.rec` files containing student grades and converts them to modern CSV format.

## Files

- **marks_reader.py** - Main module with all conversion logic
- **test_marks_reader.py** - Unit tests (10 tests, 100% pass rate)
- **S:\Chn\classes\csv_exports_python\\** - Output directory with CSV files

## Features

- ✅ Accurate Turbo Pascal Real48 (48-bit float) decoder
- ✅ Reads binary student records from `.rec` files
- ✅ Parses configuration from `.txt` files
- ✅ Generates 3 CSV files per class:
  - `{CLASS}_marks.csv` - Main gradebook (students as rows)
  - `{CLASS}_attendance.csv` - Contact info and attendance
  - `{CLASS}_marks_transposed.csv` - Students as columns
- ✅ Summary file with class statistics
- ✅ Full unit test coverage using TDD approach
- ✅ No external dependencies (uses only Python standard library)

## Critical Implementation Details

### Turbo Pascal Real48 Format

The decoder implements the correct formula: `(-1)^s * (1.m) * 2^(exp-129)`

**Key fix**: The mantissa includes an implicit leading 1, so it's `(1.m)` not just `(m)`. This was the critical bug in earlier versions that caused all marks to be halved.

```python
# CORRECT implementation
mantissa_value = 1.0 + (mantissa_int / (2.0 ** 39))
value = sign * mantissa_value * (2.0 ** exponent)
```

## Usage

### Convert all classes to CSV:
```bash
py marks_reader.py
```

### Run unit tests:
```bash
py test_marks_reader.py -v
```

### Import as module:
```python
from marks_reader import convert_class_to_csv

convert_class_to_csv(
    rec_file='S:\\Chn\\classes\\Ics4m1-1.rec',
    txt_file='S:\\Chn\\classes\\Ics4m1-1.txt',
    output_dir='S:\\Chn\\classes\\csv_exports_python'
)
```

## Test Results

All 10 unit tests pass:
- ✅ decode_turbo_real with zero (no mark)
- ✅ decode_turbo_real with positive numbers
- ✅ decode_turbo_real with invalid length
- ✅ decode_turbo_real with implicit leading 1
- ✅ read_pascal_string (simple, empty, full length)
- ✅ read_config_file structure
- ✅ format_mark function
- ✅ convert_class_to_csv integration

## Output Statistics

Converted 6 classes with 126 students total:
- ICS4M1-1: CS 12 - PERIOD 3 (14 students, 15 assignments)
- ICS4M1-2: CS12 - PERIOD 2 (14 students, 15 assignments)
- TGJ4MW-1: WEB SITE - PERIOD 6 (18 students, 10 assignments)
- TIK2O1-1: CS10 - PERIOD 1 (26 students, 22 assignments)
- TIK2O1-3: CS10 - PERIOD 5 (28 students, 22 assignments)
- TIK2O1-4: CS10 - PERIOD 7 (26 students, 22 assignments)

## Verification

The decoder accuracy was verified by:
1. Comparing A1 average: 83.9% (matches config file exactly)
2. Comparing class final average: 81.26% (matches config file exactly)
3. Cross-checking with Pascal output (when compatible)
4. Manual verification of individual student marks

Example verification (YAN KENNY from ICS4M1-1):
- Final Mark: 93.3% ✅ (was incorrectly 29.3% before the mantissa fix)
- All individual assignments match expected values

## Dependencies

None - uses only Python standard library:
- `struct` - Binary data parsing
- `csv` - CSV file generation
- `os` - File system operations
- `pathlib` - Path handling
- `unittest` - Testing framework

## Original Pascal Code

Based on:
- `S:\Chn\classes\pascal_reader\ReadMarks.pas`
- `S:\tony\cmwin\cmfile.pas` (record structures)
- `S:\tony\cmwin\cmvars.pas` (type definitions)

## License

Educational use. Original Pascal code by the same gradebook system author.
