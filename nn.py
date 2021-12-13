from prepare_data import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import os


#INPUT OF 385
#OUTPUT OF 4096



#get data
moves = []
boards = []
for filename in os.listdir("stored_games/"):
    try:
        _moves, _boards = prepare_data(f"stored_games/{filename}")
        moves = moves + _moves
        boards = boards + _boards

    except Exception as e:
        print("*******************************************************************************************************************************")
        print(e)

X, Y = get_XY(moves, boards)

print(X)
print(Y)
    


model = Sequential()
model.add(Dense(385, activation="relu"))
model.add(Dense(500, activation="relu"))
model.add(Dense(1000, activation="relu"))
model.add(Dense(2000, activation="relu"))
model.add(Dense(4096, activation="relu"))
