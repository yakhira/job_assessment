import sys
import os

def main(input_file, l_number):
    dna_letters = {
        "00": "A",
        "01": "C",
        "10": "G",
        "11": "T"
    }

    print(f"L = {l_number}")
    print(f"Input file = {input_file}")
    print(f"Output file = output{l_number}\n")

    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found.")
        return

    out_file = open(f"output{l_number}", "w")

    with open(input_file, "rb") as in_file:
        sequence_index = 0

        # Read l_number bytes each iteration
        while(bytes := in_file.read(l_number)):
            q_score = ''
            dna_letter = ''

            for byte in bytes:
                # Convert dec to bin
                byte = bin(byte)[2:]
                # Get amount of missing first 0 bits
                formated_bits = f"{(8 - len(byte))*'0'}{byte}"
                # Read first 2 bits and determine DNA letter
                dna_letter += dna_letters[formated_bits[:2]]
                # Read next 6 bits, add 33 and convert to ASCII
                q_score += chr(int(formated_bits[2:], 2) + 33)

            sequence_index+=1

            # Save data to output file
            out_file.write(
                f"@READ_{sequence_index}\n"
                f"{dna_letter}\n"
                f"+READ_{sequence_index}\n"
                f"{q_score}\n"
            )
    out_file.close()

if len(sys.argv) == 3:
    main(sys.argv[1], int(sys.argv[2]))
else:
    print(f"usage: {sys.argv[0]} <encoded file> <L-number>")