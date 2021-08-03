#Server for Ships Game
import socket
from threading import Thread
from colorama import init
from colorama import Fore, Back, Style
import pickle
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 56400
host = 'localhost'
s.bind((host, port))
init()

players = []

def gameHandler(player1, player2):
    global player
    global playerO
    global playerOLocalShips
    global playerLocalShips
    player1[1].send("Game Started".encode())
    player2[1].send("Game Started".encode())
    playerLocalShips = pickle.loads(player1[1].recv(1024))
    playerOLocalShips = pickle.loads(player2[1].recv(1024))
    player = player1
    playerO = player2
    def switchplayers():
        global player
        global playerO
        global playerOLocalShips
        global playerLocalShips
        if(player == player1):
            player = player2
            playerLocalShips, playerOLocalShips = playerOLocalShips, playerLocalShips
            playerO = player1
        elif(player == player2):
            player = player1
            playerLocalShips, playerOLocalShips = playerOLocalShips, playerLocalShips
            playerO = player2

    while(1):

        player[1].send("It's your turn".encode())
        playerO[1].send("It's the opponents turn".encode())
        useraction = player[1].recv(1024).decode()
        useraction = useraction.split(",")

        if(useraction[0] == "ML"):
            print(useraction[0], useraction[1])
            print(playerOLocalShips)
            if(useraction[1] in playerOLocalShips):
                playerOLocalShips[useraction[1]] += -1
                if(playerOLocalShips[useraction[1]] == 0):
                    del playerOLocalShips[useraction[1]]
                    if not playerOLocalShips:
                        player[1].send("You won!".encode())
                        playerO[1].send(("You lost.").encode())
                        break


                    else:
                        player[1].send("You Destroyed Enemy Ship!".encode())
                        playerO[1].send(("Missile incoming...Your " + str(useraction[1]) + " ship was hit and destroyed!").encode())
                        playerO[1].send(pickle.dumps(playerOLocalShips, -1))
                        switchplayers()
                else:
                    player[1].send("Hit!".encode())
                    playerO[1].send(("Missile incoming...Your " + useraction[1] + " ship was hit!").encode())
                    switchplayers()
            else:
                player[1].send("Miss".encode())
                playerO[1].send(("Missile incoming...It missed your ships").encode())
                switchplayers()
        if(useraction[0] == "MS"):
            shipcom = useraction[1].split(" ")
            if(shipcom[0] in playerLocalShips and shipcom[1] not in playerLocalShips):
                playerLocalShips[shipcom[1]] = playerLocalShips[shipcom[0]]
                del playerLocalShips[shipcom[0]]
                player[1].send("Ship moved!".encode())
                playerO[1].send("Enemy fleet movment detected.".encode())
                player[1].send(pickle.dumps(playerLocalShips, -1))
                switchplayers()
            elif(shipcom[0] not in playerLocalShips):
                player[1].send("Ship doesn't exist!".encode())
            elif(shipcom[1] in playerLocalShips):
                player[1].send("You cannot put ship on ship..".encode())







def listener():
    global players
    while(1):
        s.listen(5)
        conn, addr = s.accept()
        print(Fore.CYAN + "New connection from: " + addr[0])
        username = conn.recv(1024).decode()
        conn.send("Matchmaking started.".encode())
        players += [[username, conn, addr]]


def matchMaking():
    while(1):

        if len(players) >= 2:
            Thread(target=gameHandler, args=(players[0], players[1])).start()
            del players[0]
            del players[0]


Thread(target=matchMaking).start()

listener()
