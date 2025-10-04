# Marks Reader Conversion Toolkit

This repository contains a Python port of a legacy Turbo Pascal/Delphi gradebook reader. The tooling decodes `.rec` gradebook
files and exports class data to more accessible CSV or spreadsheet formats.

## Project Structure

- **marks_reader_python/** - Primary Python implementation and utilities for decoding and exporting marks.
  - `marks_reader.py` – Core conversion logic that parses configuration `.txt` files, decodes Real48 floating-point values, and
    generates CSV exports.
  - `convert_to_csv.py`, `display_class.py`, `display_spreadsheet.py`, `export_to_excel.py` – Helper scripts for specific export
    or display workflows.
  - `test_marks_reader.py`, `test_decode.py` – Unit tests covering the Real48 decoder and end-to-end conversion.
  - `output/` – Example output from running the conversion scripts.
- `README_marks_reader.md` - Detailed documentation for the Python port, including implementation notes and verification steps.

## Getting Started

1. Ensure you have Python 3.8+ installed.
2. Navigate into `marks_reader_python/` to run the utilities.

### Converting Gradebooks

Use the main conversion script to process a `.rec` file alongside its accompanying `.txt` configuration file:

```bash
python marks_reader_python/marks_reader.py
```

By default the script looks for the legacy directory structure. Update the paths in `marks_reader.py` or call helper functions
with explicit paths to match your environment.

### Running Tests

Execute the bundled unit tests to verify the decoder and conversion pipeline:

```bash
python -m unittest marks_reader_python/test_marks_reader.py
python -m unittest marks_reader_python/test_decode.py
```

## Additional Resources

Refer to `marks_reader_python/README_marks_reader.md` for a deep dive into the Real48 decoding algorithm, file format details,
and validation results for the converted gradebooks.
