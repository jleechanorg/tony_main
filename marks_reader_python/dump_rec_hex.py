import struct

def dump_first_record():
    with open(r'S:\Chn\classes\Ics4m1-1.rec', 'rb') as f:
        # Read first 100 bytes to see the structure
        data = f.read(800)

        print("First 800 bytes of file (hex dump):")
        for i in range(0, min(len(data), 800), 16):
            hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
            print(f'{i:04x}: {hex_part:<48} {ascii_part}')

        print("\n\nFile size:", len(data), "bytes read")

        # Try to read name at offset 0
        print("\n\nAttempting to parse first record:")
        f.seek(0)

        # String[20] = 1 length byte + up to 20 chars
        name_len = struct.unpack('B', f.read(1))[0]
        print(f"Name length byte: {name_len}")
        name_data = f.read(20)
        name = name_data[:name_len].decode('latin-1', errors='replace')
        print(f"Name: '{name}'")

        # String[10] for student number
        studno_len = struct.unpack('B', f.read(1))[0]
        studno_data = f.read(10)
        studno = studno_data[:studno_len].decode('latin-1', errors='replace')
        print(f"Student #: '{studno}' (len={studno_len})")

        # String[10] for homeform
        hf_len = struct.unpack('B', f.read(1))[0]
        hf_data = f.read(10)
        homeform = hf_data[:hf_len].decode('latin-1', errors='replace')
        print(f"Homeform: '{homeform}' (len={hf_len})")

        print(f"\nCurrent file position: {f.tell()}")

        # Show next 50 bytes (start of marks array)
        marks_start = f.read(50)
        print("\nNext 50 bytes (marks array start):")
        print(' '.join(f'{b:02x}' for b in marks_start))

dump_first_record()
