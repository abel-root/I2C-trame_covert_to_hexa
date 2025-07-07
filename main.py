import re

def find_S_indices(line):
    return [m.start() for m in re.finditer('S', line)]

def ckeck_if_line_start_by_S(line):
    return line[0] != "S"

def decode_i2c_frames(line):
    frames_output = []
    
    if not ckeck_if_line_start_by_S(line):
        S_indices = find_S_indices(line)
        size_line = len(line)

        for i in range(len(S_indices)):
            start = S_indices[i]
            end = S_indices[i + 1] if i + 1 < len(S_indices) else size_line
            frame = line[start:end]

            try:
                current = 1  # après le 'S'
                output = ["[S]"]

                # Adresse + R/W
                if current + 8 > len(frame):
                    continue
                addr_rw = frame[current:current+8]
                current += 8

                addr = int(addr_rw[:7], 2)
                rw = addr_rw[7]
                output.append(f"0x{addr:02X}")
                output.append(rw)

                # ACK/NACK après adresse
                if current >= len(frame):
                    continue
                ack = frame[current]
                if ack not in ('A', 'N'):
                    continue
                output.append(ack)
                current += 1

                # Lecture des données : [8 bits données] + A/N
                while current < len(frame):
                    if frame[current] == 's':
                        output.append('[s]')
                        current += 1
                        break

                    if current + 8 > len(frame):
                        break
                    data_bits = frame[current:current+8]
                    data = int(data_bits, 2)
                    output.append(f"0x{data:02X}")
                    current += 8

                    if current >= len(frame):
                        break
                    ack = frame[current]
                    if ack not in ('A', 'N'):
                        break
                    output.append(ack)
                    current += 1

                frames_output.append(' '.join(output))

            except Exception as e:
                frames_output.append(f"[ERROR] decoding frame: {e}")
    else:
        # Ajoute 'S' au début de la ligne et relance la fonction pour ne pas changer le code déjà fait
        line_with_S = 'S' + line
        return decode_i2c_frames(line_with_S)
    
    return ''.join(frames_output)


# Exemple d'utilisation
#line="1000000WA00000000A00000000A00000000A00000001A10000000A00000000A00000000A00000000A00000001A10000011N101s"
"""line = (
    "S1000001WA00010000A00010000A1"
    "S1000001RA00000001A00000010A10100111A00000111A00110001A00001010"
    "A00000000A00000000A00000000A00000000A00001010A00000000A00000000"
    "A00000000A00000000A00001010A00000000A00000000A00000000A00000000"
    "A00001010A00000000A00000000A00000000A00000000A00001010A00011110Ns"
)"""

line = ("S1000001WA00010000A00010000A1S1000001RA00000001A00000010A10100111A00000111A00110001A00001010A00000000A00000000A00000000A00000000A00001010A00000000A00000000A00000000A00000000A00001010A00000000A00000000A00000000A00000000A00011010A00000000A00000000A00000000A00000000A00001S0100000WA00000000A00000000A00000000A00000000N01000001N1101s"     )
if __name__=="__main__":
    #line =input('entree votre data \n')
    print(decode_i2c_frames(line))
   
