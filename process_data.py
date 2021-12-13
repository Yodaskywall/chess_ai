from prepare_data import *
import os
import pickle


#INPUT OF 385
#OUTPUT OF 4096



#get data
moves = []
boards = []
c = 0
i = 0
for filename in os.listdir("stored_games/"):
    c+=1
    if c  - i > 10:
        break
    try:
        _moves, _boards = prepare_data(f"stored_games/{filename}")
        moves = moves + _moves
        boards = boards + _boards

    except Exception as e:
        print("*******************************************************************************************************************************")
        print(e)
        print(filename)
        i+=1

X, Y = get_XY(moves, boards)

print(X)
print(type(X))
print(X.shape)

print(Y)
print(type(Y))
print(Y.shape)


print("err")
print(i)


with open("X.pkl", "wb") as file:
    pickle.dump(X, file)

with open("Y.pkl", "wb") as file:
    pickle.dump(Y, file)


print("Success")
