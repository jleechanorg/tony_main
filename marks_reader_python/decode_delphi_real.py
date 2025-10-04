import struct

def decode_turbo_real(bytes_data):
    """
    Decode Turbo Pascal/Delphi 48-bit real (6 bytes)
    Format: 1 byte exponent + 5 bytes mantissa (39 bits + sign bit)
    """
    if len(bytes_data) != 6:
        return None

    # Unpack the 6 bytes
    exp_byte = bytes_data[0]
    mantissa_bytes = bytes_data[1:6]

    # Special case: exponent = 0 means the number is 0 or no mark
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

    # Calculate the floating point value
    # Mantissa is normalized, so we divide by 2^39 and multiply by 2^exponent
    value = sign * (mantissa_int / (2.0 ** 39)) * (2.0 ** exponent)

    return value

# Test with the actual bytes from the file
# From offset 0x2B (43): marks start
test_data = bytes.fromhex('85 00 00 00 00 08')
result = decode_turbo_real(test_data)
print(f"Test decode of 85 00 00 00 00 08: {result}")

# Another test
test_data2 = bytes.fromhex('84 00 00 00 00 08')
result2 = decode_turbo_real(test_data2)
print(f"Test decode of 84 00 00 00 00 08: {result2}")

# Test with zero (no mark)
test_data3 = bytes.fromhex('00 00 00 00 80 81')
result3 = decode_turbo_real(test_data3)
print(f"Test decode of 00 00 00 00 80 81: {result3}")

# Now let's read the actual file
print("\nReading first student from file:")
with open(r'S:\Chn\classes\Ics4m1-1.rec', 'rb') as f:
    # Skip to marks (after name, studno, homeform = 43 bytes)
    f.seek(43)

    # Read first 5 marks
    for i in range(5):
        mark_bytes = f.read(6)
        mark_val = decode_turbo_real(mark_bytes)
        print(f"  Mark {i+1}: {mark_bytes.hex()} = {mark_val}")
