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

    for move in line[1:]:
        print("awe")
        print(move)
        bw_move = move.split(" ")
        moves.append(bw_move[0])
        moves.append(bw_move[1])

    return moves


if __name__ == "__main__":
    parse("sample_game.pgn")
