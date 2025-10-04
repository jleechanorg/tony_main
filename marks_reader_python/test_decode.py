import struct

def decode_turbo_real(bytes_data):
    """
    Decode Turbo Pascal/Delphi 48-bit real (6 bytes)
    """
    if len(bytes_data) != 6:
        return None

    exp_byte = bytes_data[0]
    mantissa_bytes = bytes_data[1:6]

    if exp_byte == 0:
        return -1.0

    mantissa_int = int.from_bytes(mantissa_bytes, 'little')
    sign = 1 if (mantissa_int & 0x8000000000) == 0 else -1
    mantissa_int = mantissa_int & 0x7FFFFFFFFF
    exponent = exp_byte - 129

    value = sign * (mantissa_int / (2.0 ** 39)) * (2.0 ** exponent)
    return value

# Test the marks from the hex dump
# A1 for CHAN BOBBY should be around 16-17 out of 20 (to get class avg of 83.9%)
test_cases = [
    ('85 00 00 00 00 08', 'First mark'),
    ('84 00 00 00 00 08', 'Second mark'),
    ('85 00 00 00 00 68', 'Fourth mark (showed as 13.0)'),
    ('87 00 00 00 00 0a', 'Eighth mark'),
]

for hex_str, desc in test_cases:
    bytes_val = bytes.fromhex(hex_str)
    result = decode_turbo_real(bytes_val)
    print(f"{desc}: {hex_str} = {result}")

print("\n\nLet me check what value would give us ~17/20 (85%):")
# If class average is 83.9% on a 20-point assignment, average score is 16.78

# Let's look at the pattern - maybe marks are stored as percentages?
print("\nChecking if marks are stored differently...")

# Read first student's first few marks directly
with open(r'S:\Chn\classes\Ics4m1-1.rec', 'rb') as f:
    f.seek(43)  # Skip to marks

    print("\nFirst 10 marks for CHAN BOBBY:")
    for i in range(10):
        mark_bytes = f.read(6)
        mark_val = decode_turbo_real(mark_bytes)
        print(f"  Mark {i+1}: {mark_bytes.hex()} = {mark_val:.2f}")
