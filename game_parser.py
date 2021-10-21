def parse(filename):
    with open(filename, "r") as file:
        lines = file.read().split("\n")


    found = False

    for line in lines:
        if len(line) > 1 and line[0] == "1" and line[1] == ".":
            found = True
            break

    if not found:
        raise RuntimeError("File not valid")
    
    
    line = line.split(".")
    moves = []

    for move in line[1:-1]:
        bw_move = move[:-2].split(" ")
        moves.append(bw_move[0])
        moves.append(bw_move[1])

    last = line[-1].split(" ")
    moves.append(last[0])
    score = last[1]
    print(moves)
    print(score)


if __name__ == "__main__":
    parse("sample_game.pgn")
