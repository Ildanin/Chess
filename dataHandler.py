def file_transform(input_filename: str, output_filename: str | None = None) -> None:
    if output_filename == None:
        out_file = open(input_filename.partition('.')[0] + 'txt', 'w')
    else:
        out_file = open(output_filename, 'w')
    with open(input_filename) as inp_file:
        for line in inp_file:
            if line == '\n':
                pass
            elif line.split()[0][1:] in ["WhiteElo", "BlackElo"]:
                out_file.write(line[1:10] + line.split('"')[1] + '\n')
            elif line.split()[0] == '1.':
                out_file.write(line)
    out_file.close()

def data_load(filename: str) -> list:
    data: list[list] = [[]]
    with open(filename) as file:
        for line in file:
            if line.split()[0][1:] in ["WhiteElo", "BlackElo"]:
                data[-1].append(int(line.split()[-1]))
            elif line.split()[0] == '1.':
                data[-1].append(line)
                data.append([])
    return data[:-1]

if __name__ == '__main__':
    FILENAME = "lichess_db_standard_rated_2013-01.pgn"
    file_transform(FILENAME)