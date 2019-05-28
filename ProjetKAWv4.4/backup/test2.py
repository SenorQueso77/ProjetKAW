# from flask import Flask,request,render_template
# from flask_socketio import SocketIO

# testKAW = Flask(__name__)
# socketio = SocketIO(testKAW)

# if __name__ == "__main__":
#     socketio.run(testKAW)

# @testKAW.route('/')
# @testKAW.route('/test_log', methods=['POST'])
# def testintro():
# 	return render_template("formtest.html")

Number_Of_Players = 3
Players = []

class Player:
    def __init__(self, Id):
        self.Id = Id
        self.Flag = 0
        self.tag = ""
        self.Cards = []

# for num in range(1,4):
#     x = Player(num)                                       #Un objet Player est cree avec l'index actuel
#     Players.append(x)                                     #Ajout de l'objet Player a la liste Players

x = Player("raspberry")
x.tag = "banana"
Players.append(x) 
print(Player)
print(Players[0].Id)