#A battleship game by Moltas Thörnblom
#####################################
# One Move per player, shoot, move, search,
# Server sided game, clients connect to server
# Button for displaying enemy board(disguised with hits)
# live feed and commandos
######################################
import time
import pickle
from time import sleep
import sys
import random
from colorama import init
from colorama import Fore, Back, Style
from termcolor import cprint
from pyfiglet import figlet_format
import playsound
import os
import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "localhost"
port = 56400
init()
letters = ["A","B","C","D","E","F","G","H","I"]
messages = []

def clear():
    os.system("cls")
def typingEffect(words):
    for char in words:
        sleep(0.02) 
        sys.stdout.write(char)
        sys.stdout.flush()

def build2(pos):
    print("                                   1      2      3      4      5      6      7      8     9    ")
    print("                               =================================================================")
    for x in letters:
        row = ""
        for y in range(1,10):
            if x+str(y) in pos:
                row += "<*==>> "

            else:
                row += "       "




        print("                             " + x + " " + "#" + row + "#")
        print("                               #                                                               #")



    print("                               #                                                               #")
    print("                               =================================================================")
def generateShips():
    ships = {}
    shipNr = 1
    amountShips = 0
    while(amountShips < 4):
        newShip = random.choice(letters) + str(random.randint(1,9))
        if newShip not in ships:
            ships[newShip] = 1
            shipNr += 1
            amountShips += 1
    return ships
def introGame():
    global usrname
    localShips = generateShips()
    build2(localShips)
    print(Fore.YELLOW)
    usrname = input("Choose a username => ")
    words = "  Welcome Lieutenant "+ usrname + " to the operation center..."
    typingEffect(words)
    time.sleep(2) 
    print("")
    print("")
    typingEffect("  From here you will be able to control your fleet")
    print("")
    typingEffect("  and make sure we do win this war")
    print("")
    print("")
    time.sleep(0.2)
    input("  Are you ready?[Press Enter]")
    startGame(localShips)

def startGame(localShips):
    global messages
    s.connect((host,port))
    s.send(usrname.encode())
    print(s.recv(1024).decode())
    print(s.recv(1024).decode())
    shipsOverNet = pickle.dumps(localShips, -1)
    s.send(shipsOverNet)
    time.sleep(2)
    while(1):
        clear()
        build2(localShips)
        print("                              Controls: [1] Fire Missile [2] Move Ship [3] Radar Scan [4] Give up")
        if(messages):
            for x in messages:
                print(x)
            messages = []
        if(s.recv(1024).decode() == "It's your turn"):
            print("It's your turn")
            localTurn = True
        else:
            print("It's the opponents turn")
            localTurn = False
            resp = s.recv(1024).decode()
            if("destroyed!" in resp):
                localShips = pickle.loads(s.recv(1024))
                messages.append(resp)
            elif("lost." in resp):
                print(resp)
                time.sleep(5)
                mainmenu()
            else:
                print(resp)
        while(localTurn):
            userinput = input("=> ")

            if(userinput == "1"):
                while(1):
                    aim = input("Square? => ")
                    if(input("<Missile Fire : "+ aim + " [Y/n]> ") in ["Y", "y", ""]):
                       print("Missile Launched!")
                       s.send(("ML," + aim).encode())
                       resp = s.recv(1024).decode()
                       if("won!" in resp):
                           print(resp)
                           time.sleep(5)
                           mainmenu()

                       else:
                           print(resp)

                       time.sleep(2)
                       break
                    else:
                        pass
                break


                
            elif(userinput == "2"):
                while(1):
                    movementship = input("Which Ship? => ")
                    movementsquare = input("Square? => ")
                    if(input("<Move Ship " + movementship + " to : "+ movementsquare + " [Y/n]> ") in ["Y", "y", ""]):
                       s.send(("MS," + movementship+" " + movementsquare).encode())
                       resp = s.recv(1024).decode()
                       if(resp == "Ship moved!"):
                           localShips = pickle.loads(s.recv(1024))
                           print("Ship moved!")
                       else:
                           print(resp)

                       time.sleep(2)
                       break
                    else:
                        pass
                break
            elif(userinput == "3"):
                print("Scanning...")
                #server code goes here
            elif(userinput == "4"):
                if(input("Surrender?[y/N]") in ["y","Y"]):
                    print("You surrendered..")
                    #server code goes here








def mainmenu():
    clear()
    print(Fore.YELLOW)
    print("")
    print("")
    print("")
    print("                                               _____ __    _")
    print("                                              / ___// /_  (_)___  _____")
    print("                                              \__ \/ __ \/ / __ \/ ___/")
    print("                                             ___/ / / / / / /_/ (__  )")
    print("                                            /____/_/ /_/_/ .___/____/")
    print("                                                        /_/")
    print("")
    print(Fore.CYAN + "                                                        |\/")
    print("                                                        ---")
    print("                                                        / | [")
    print("                          " + Fore.GREEN + "[1] Start Game" + Fore.CYAN + "         !      | |||" + Fore.RED + "             [2] Exit")
    print(Fore.CYAN + "                                               _/|     _/|-++'")
    print("                                           +  +--|    |--|--|_ |-")
    print("                                        { /|__|  |/\__|  |--- |||__/")
    print("                                       +---------------___[}-_===_.'____                 ")
    print("                                   ____`-' ||___-{]_| _[}-  |     |_[___\==--               _")
    print("                    __..._____--==/___]_|__|_____________________________[___\==--____,------' .7")
    print("                   |                               Welcome to Ships                           /")
    print("                    \_________________________________________________________________________|")


    userinput = input("=> ")
    if(userinput == "1"):
        clear()
        introGame()
    elif(userinput == "2"):
        exit()
    else:
        print(Fore.RED + "Bad option.")
        time.sleep(2)
        mainmenu()






mainmenu()
time.sleep(100)
