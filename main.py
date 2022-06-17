from os import listdir

def convertLittleBytes(raw: int):
    """Convert input to little bytes"""
    raw = raw.to_bytes(4, 'little').hex()
    processed = []
    odd_byte = None
    for byte in raw:
        if odd_byte is None:
            odd_byte = byte
        else:
            processed.append(odd_byte + byte)
            odd_byte = None

    return ' '.join(processed)


def run():
    csv = 'enum,name,id\n'

    for path in listdir('gamefiles/'):
        if path.endswith('.cs') and '#' not in path:
            with open('gamefiles/' + path, 'r') as f:
                raw_data = f.readlines()
            # Remove whitespace
            raw_data = [s.strip() for s in raw_data]
            # Remove namespace
            raw_data = raw_data[2:][::-1][1:][::-1]

            while True:
                if raw_data == []:
                    break
                enum = raw_data.pop(0)[12:]
                if enum == '':
                    break
                print(enum)
                
                if raw_data.pop(0) != '{':
                    raise Exception('This file is not formatted correctly.')
                
                while raw_data[0] != '}':
                    entry = raw_data.pop(0)
                    entry = entry.strip(',')
                    entry = entry.split(' = ')
                    if not entry[0].startswith('///'):
                        name, oid = entry[0], entry[1]
                        oid = convertLittleBytes(int(oid))
                        print(name, oid)
                        csv += (f'{enum},{name},{oid}\n')
                raw_data.pop(0)
            input('Press Enter...')

    with open('output.csv', 'w') as f:
        f.truncate()
        f.write(csv)


if __name__ == '__main__':
    run()
