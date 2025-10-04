# Claude Code Project Instructions

## Working Style

**Autonomy Level: HIGH**

- Make implementation decisions independently
- Ask clarifying questions only at the start of new tasks
- Once goals are agreed upon, work autonomously without asking permission
- Don't present multiple options - choose the best approach and execute
- Only ask the user if truly ambiguous or critical decision required

## Project Context

This is a Python conversion of a Delphi/Turbo Pascal gradebook system that reads binary `.rec` files and converts them to CSV format.

### Critical Technical Details

**Turbo Pascal Real48 Decoder:**
- Format: `(-1)^s * (1.m) * 2^(exp-129)`
- **CRITICAL**: Mantissa has implicit leading 1: `(1.m)` not `(m)`
- This was the key bug fix - missing this halves all values

```python
mantissa_value = 1.0 + (mantissa_int / (2.0 ** 39))
value = sign * mantissa_value * (2.0 ** exponent)
```

### File Structure

**Source Data:**
- `S:\Chn\classes\*.rec` - Binary student records (796 bytes per student)
- `S:\Chn\classes\*.txt` - Configuration files with assignment details
- `S:\tony\cmwin\*.pas` - Original Delphi source code (reference only)

**Python Implementation:**
- `marks_reader.py` - Main conversion module (464 lines, Python stdlib only)
- `test_marks_reader.py` - Unit tests (10 tests, 100% pass rate)
- `display_class.py` - Display class in text spreadsheet format
- `export_to_excel.py` - Export class to Excel .xlsx format (requires openpyxl)
- `README_marks_reader.md` - Documentation

**Output:**
- `S:\Chn\classes\csv_exports_python\` - Generated CSV files
  - 3 CSV files per class: marks, attendance, marks_transposed
  - `_summary.csv` - Summary of all classes
- `S:\Chn\classes\` - Excel exports and text spreadsheets
- All marks formatted to 1 decimal place

### Development Approach

**Test-Driven Development:**
- Write tests first
- All changes must pass existing tests
- Use Python stdlib only (no external dependencies)

**File Safety:**
- Never modify original `.rec` or `.txt` files
- Never modify Pascal source code in `S:\tony\`
- Only write to `csv_exports_python` output directory

### Code Standards

- Python 3.8+ compatible
- Use type hints where helpful
- Keep functions focused and testable
- Document complex algorithms (like Real48 decoder)
- Format all marks to 1 decimal place in CSV output

### Common Tasks

**Run all tests:**
```bash
py test_marks_reader.py -v
```

**Convert all classes to CSV:**
```bash
py marks_reader.py
```

**Display class in spreadsheet format:**
```bash
py display_class.py TIK2O1-1
```

**Export class to Excel:**
```bash
py export_to_excel.py TIK2O1-1
```
Output: `S:\Chn\classes\TIK2O1-1_marks.xlsx`

**Verify output:**
- Compare against `S:\Chn\classes\csv_exports_corrected\` (known good output)
- Check specific student marks (e.g., YAN KENNY: 93.3% final)
- Verify class averages match config files
- Use `fc` command to compare CSV files

### Known Good Data Points

**ICS4M1-1 Class (CS 12 - PERIOD 3):**
- 14 students, 15 assignments
- A1 average: 83.9%
- Class final average: 81.26%
- Top student: PHUNG GARY (95.4%)
- YAN KENNY: 93.3% (was 29.3% before decoder fix)

**All Classes Summary:**
- ICS4M1-1: CS 12 - PERIOD 3 (14 students, 15 assignments)
- ICS4M1-2: CS12 - PERIOD 2 (14 students, 15 assignments)
- TGJ4MW-1: WEB SITE - PERIOD 6 (18 students, 10 assignments)
- TIK2O1-1: CS10 - PERIOD 1 (26 students, 22 assignments)
- TIK2O1-3: CS10 - PERIOD 5 (28 students, 22 assignments)
- TIK2O1-4: CS10 - PERIOD 7 (26 students, 22 assignments)
- **Total: 6 classes, 126 students**

### Project History

**Development Timeline:**
1. Initial exploration of Delphi `.rec` and `.txt` files
2. Found Turbo Pascal Real48 decoder bug - missing implicit leading 1 in mantissa
3. Web search confirmed correct formula: `(-1)^s * (1.m) * 2^(exp-129)`
4. Fixed decoder, verified with YAN KENNY (29.3% → 93.3%)
5. Built complete Python system with TDD approach
6. Created CSV export (3 files per class)
7. Added text spreadsheet display
8. Added Excel export with formatting
9. All output verified against original corrected CSV files (100% match)

**Key Lessons:**
- The implicit leading 1 in Turbo Pascal Real48 mantissa is critical
- TDD approach caught edge cases early
- Python stdlib sufficient for binary parsing
- openpyxl needed for Excel export

### Working Rules

1. **Decide and execute** - don't ask permission for implementation details
2. **Test everything** - run tests after changes
3. **Stay autonomous** - only interrupt for truly critical decisions
4. **Keep it simple** - Python stdlib only, no unnecessary complexity
5. **Format consistently** - all marks to 1 decimal place

### User Preferences

- High autonomy - make decisions independently
- Ask clarifying questions only at task start
- Once goals agreed, work without interruption
- Don't present options - choose best approach and execute
