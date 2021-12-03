import json

with open("games", "r") as file:
    data = file.read().split("\n")[13]
    data = json.loads(data)["result"]
    n_games = data["total_games"]
    data = data["games"]

c = 0
for game in data:
    with open(f"stored_games/{c}game.pgn", "w") as file:
        to_write = ""
        for move in game["moves_san"]:
            to_write += move
            to_write += " "
        to_write = to_write[:-1]
        file.write(to_write)

    c += 1
