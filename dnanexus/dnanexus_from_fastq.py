import sys
import os

def main(input_file):
    dna_letters = {
        "A": "00",
        "C": "01",
        "G": "10",
        "T": "11"
    }

    print(f"Input file = {input_file}")
    print(f"Output file = input_from_{input_file}\n")

    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found.")
        return
    
    out_file = open(f"input_from_{input_file}", "wb")

    bin_entries = []
    index = 0

    with open(input_file, "r") as in_file:
        while(line := in_file.readline()):
            if "@READ_" in line:
                # Read DNA letters and convert it to first to bits 
                for dna_letter in in_file.readline().rstrip():
                    bin_entries.append(dna_letters[dna_letter])

                # Skip line with +READ_
                in_file.readline()

                for q_score in in_file.readline().rstrip():
                    # Get score, convert to dec, minus 33 and convert bin
                    score_bits = str(bin(ord(q_score) - 33)[2:])
                    # Fill missing first 0 bits
                    bin_entries[index] += f"{(6 - len(score_bits))*'0'}{score_bits}"
                    # Convert bin to dec
                    bin_entries[index] = int(bin_entries[index], 2)
                    index += 1

                # Flush binary data
                out_file.write(bytearray(bin_entries))
                index = 0
                bin_entries = []
    out_file.close()

if len(sys.argv) == 2:
    main(sys.argv[1])
else:
    print(f"usage: {sys.argv[0]} <encoded file>")