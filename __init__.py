
######## This is the main file that creates an instance of the game using Tkinter
######## Run the "server.py" file before you run this file


import socket
import threading
from queue import Queue

HOST = input("Enter server's IP address: ") # user should enter the IP address displayed on the server window
PORT = int(input("Enter PORT number: ")) # user should enter the PORT number displayed on the server window
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        server.connect((HOST,PORT))
        print("Connected to server.")
        break
    except:
        print("\nConnection failed. Try again.\n")
        HOST = input("Enter server's IP address:")
        PORT = int(input("Enter PORT number:"))

#################################################################
# Sockets client code copied from 15-112 Sockets mini-lecture

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

#################################################################

from pieceClasses import *
from algorithms import *
import copy
import random


#### Graphics Functions

from tkinter import *

def init(data):
    data.background = PhotoImage(file="background.gif", width=data.width, height=data.height) # image downloaded from https://v.paixin.com/photocopyright/132056282
    data.countdown = 20
    data.isPaused = False
    data.board = [  [Post(0, 0, LMN("A")), Headquarters(0, 1, Flag("A")), Post(0, 2, Capt("A")), Headquarters(0, 3, LMN("A")), Post(0, 4, LMN("A"))],
                    [Post(1, 0, Capt("A")), Post(1, 1, Lt("A")), Post(
                        1, 2, BGen("A")), Post(1, 3, Spr("A")), Post(1, 4, Spr("A"))],
                    [Post(2, 0, MGen("A")), Camp(2, 1), Post(
                        2, 2, Lt("A")), Camp(2, 3), Post(2, 4, Maj("A"))],
                    [Post(3, 0, Gen("A")), Post(3, 1, Bomb("A")), Camp(
                        3, 2), Post(3, 3, Lt("A")), Post(3, 4, Mar("A"))],
                    [Post(4, 0, Maj("A")), Camp(4, 1), Post(4, 2, Spr("A")),
                          Camp(4, 3), Post(4, 4, Bomb("A"))],
                    [Post(5, 0, MGen("A")), Post(5, 1, Col("A")), Post(
                        5, 2, BGen("A")), Post(5, 3, Capt("A")), Post(5, 4, Col("A"))],
                    [Post(6, 0, MGen("B")), Post(6, 1, Spr("B")), Post(
                        6, 2, Capt("B")), Post(6, 3, Mar("B")), Post(6, 4, Col("B"))],
                    [Post(7, 0, Bomb("B")), Camp(7, 1), Post(
                        7, 2, Spr("B")), Camp(7, 3), Post(7, 4, Bomb("B"))],
                    [Post(8, 0, Capt("B")), Post(8, 1, Maj("B")), Camp(
                        8, 2), Post(8, 3, BGen("B")), Post(8, 4, Lt("B"))],
                    [Post(9, 0, Maj("B")), Camp(9, 1), Post(
                        9, 2, BGen("B")), Camp(9, 3), Post(9, 4, Gen("B"))],
                    [Post(10, 0, LMN("B")), Post(10, 1, Lt("B")), Post(
                        10, 2, Spr("B")), Post(10, 3, MGen("B")), Post(10, 4, LMN("B"))],
                    [Post(11, 0, Capt("B")), Headquarters(11, 1, Lt("B")), Post(11, 2, Col("B")), Headquarters(11, 3, Flag("B")), Post(11, 4, LMN("B"))]]

    data.mode = "start"
    data.lastMode = data.mode
    data.turn = "B"
    data.selectCount = 0
    data.firstSelect, data.secondSelect = None, None
    data.move = None
    data.myPID = None
    data.selfPlayerReady, data.otherPlayerReady = False, False
    data.darkMode = False
    data.marA = True
    data.marB = True
    data.winner = None
    data.errorMsg = None
    data.maxDepth = 0
    data.otherPlayerOnline = False
    data.displaySuggestedMove = 0
    data.timer = None
    data.playerMove = None


# a helper function that switches two piece for the layout mode
# return an error message if the switch is illegal (and return None if legal)
def switch(data):
    (a, b) = data.firstSelect
    (c, d) = data.secondSelect
    # pieces must stay within their own side
    if data.board[a][b].piece.side != data.board[c][d].piece.side:
        return "Cannot switch pieces of the other side!"
    # flags must remain in headquarters
    if data.board[a][b].piece.order == 0 and (((a, b) == (0, 1) or (a, b) == (0, 3)) and ((c, d) != (0, 1) and (c, d) != (0, 3))) or \
    (((a, b) == (11, 1) or (a, b) == (11, 3)) and ((c, d) != (11, 1) and (c, d) != (11, 3))):
        return "Flags must be placed in a Headquarter!"
    if data.board[c][d].piece.order == 0 and (((c, d) == (0, 1) or (c, d) == (0, 3)) and ((a, b) != (0, 1) and (a, b) != (0, 3))) or \
    (((c, d) == (11, 1) or (c, d) == (11, 3)) and ((a, b) != (11, 1) and (a, b) != (11, 3))):
        return "The Flag must be placed in one of the two Headquarters!"
    # bombs cannot be on the front row
    if data.board[a][b].piece.order == None and (c == 5 or c == 6):
        return "Bombs cannot be placed on the front row!"
    if data.board[c][d].piece.order == None and (a == 5 or a == 6):
        return "Bombs cannot be placed on the front row!"
    # landmines must remain at the last two rows
    if data.board[a][b].piece.order == 10 and (c in [2, 3, 4, 5, 6, 7, 8, 9]):
        return "Landmines can only be placed on the last two rows!"
    if data.board[c][d].piece.order == 10 and (a in [2, 3, 4, 5, 6, 7, 8, 9]):
        return "Landmines can only be placed on the last two rows!"
    data.board[a][b].piece, data.board[c][d].piece = data.board[c][d].piece, data.board[a][b].piece
    # undo selection
    data.selectCount = 0
    data.board[a][b].select()
    data.board[c][d].select()
    return None


def mousePressed(event, data):
    if data.mode == "start":
        if 200 < event.x < 400 and 500 < event.y < 580:
            data.darkMode = True
        if 200 < event.x < 400 and 340 < event.y < 400:
            data.mode = "selectDifficulty"
        elif 200 < event.x < 400 and (420 < event.y < 480 or 500 < event.y < 580):
            data.mode = "twoPlayerLayout"
    
    elif data.mode == "selectDifficulty":
        if 200 < event.x < 400 and 340 < event.y < 400:
            # easy mode
            data.maxDepth = 2
            data.mode = "onePlayerLayout"
        elif 200 < event.x < 400 and 420 < event.y < 480:
            # hard mode
            data.maxDepth = 4
            data.mode = "onePlayerLayout"

    elif data.mode == "twoPlayerLayout" and data.otherPlayerOnline:
        if 385 < event.x < 465 and 380 < event.y < 420:
            # player is ready
            data.selectCount = 0
            data.firstSelect = None
            data.selfPlayerReady = True
            for x in range(12):
                for y in range(5):
                    if data.board[x][y].selected:
                        data.board[x][y].selected = False
            msg = "playerReady +1\n"
            print("sending: ", msg)
            data.server.send(msg.encode())

        if getLocation(event.x, event.y) != None:
            (i, j) = getLocation(event.x, event.y)
            if data.myPID == "PlayerA":
                (i, j) = (11-i, 4-j) # reverse the board
            # cannot put pieces in Camps during layout stage
            if type(data.board[i][j]) == Camp:
                return None
            # cannot change the layout of the other side
            if data.myPID == "PlayerA" and i >= 6:
                return None
            elif data.myPID == "PlayerB" and i < 6:
                return None

            data.selectCount += 1
            data.board[i][j].select()
            if data.selectCount == 1:
                data.firstSelect = (i, j)
            elif data.selectCount == 2:
                data.secondSelect = (i, j)
                (a, b) = data.firstSelect
                (c, d) = data.secondSelect
                data.errorMsg = switch(data)
                if data.errorMsg == None:

                    msg = "playerSwitched %d %d %d %d\n" % (a, b, c, d)
                    print("sending: ", msg)
                    data.server.send(msg.encode())
        else:
            # undo selection
            data.selectCount = 0
            data.errorMsg = None
            data.firstSelect = None
            for x in range(12):
                for y in range(5):
                    if data.board[x][y].selected:
                        data.board[x][y].selected = False

    elif data.mode == "onePlayerLayout":
        if 385 < event.x < 465 and 380 < event.y < 420:
            # start game
            data.selectCount = 0
            data.firstSelect = None
            for x in range(12):
                for y in range(5):
                    if data.board[x][y].selected:
                        data.board[x][y].selected = False
            data.mode = "onePlayerGame"

        if getLocation(event.x, event.y) != None:
            (i, j) = getLocation(event.x, event.y)
            if type(data.board[i][j]) == Camp:
                return None
            data.selectCount += 1
            data.board[i][j].select()
            if data.selectCount == 1:
                data.firstSelect = (i, j)
            elif data.selectCount == 2:
                data.secondSelect = (i, j)
                data.errorMsg = switch(data)
        else:
            # undo selection
            data.selectCount = 0
            data.firstSelect = None
            data.errorMsg = None
            for x in range(12):
                for y in range(5):
                    if data.board[x][y].selected:
                        data.board[x][y].selected = False


    elif data.mode == "twoPlayerGame" and data.displaySuggestedMove == 0:
        if getLocation(event.x, event.y) == None:
            # clear selection
            data.selectCount = 0
            if data.firstSelect != None:
                for (a, b) in isLegal(data.board, data.firstSelect):
                    data.board[a][b].highlight()
                (i, j) = data.firstSelect
                data.firstSelect = None
                data.board[i][j].select()
        else:
            # a piece is selected
            (i, j) = getLocation(event.x, event.y)
            if data.myPID == "PlayerA":
                (i, j) = (11-i, 4-j) # reverse the board

            # selected a piece to move
            if data.selectCount == 0 and data.board[i][j].piece != None and data.board[i][j].piece.side == data.turn:
                # cannot move opponent's pieces
                if (data.myPID == "PlayerA" and data.turn == "A") or (data.myPID == "PlayerB" and data.turn == "B"):
                    data.selectCount += 1
                    data.board[i][j].select()
                    data.firstSelect = (i, j)
                    for (a, b) in isLegal(data.board, data.firstSelect):
                        data.board[a][b].highlight()

            # selected a spot to move to
            elif data.selectCount == 1:
                if (i, j) in isLegal(data.board, data.firstSelect):
                    (a, b) = data.firstSelect
                    msg = "playerMoved %d %d %d %d\n" % (a, b, i, j)
                    print("sending: ", msg)
                    data.server.send(msg.encode())
                    data.timer = 0
                    data.playerMove = (a, b, i, j)
                    for x in range(12):
                        for y in range(5):
                            if data.board[x][y].highlighted:
                                data.board[x][y].highlighted = False
                            if data.board[x][y].selected:
                                data.board[x][y].selected = False

    elif data.mode == "onePlayerGame" and data.turn == "B":
        if getLocation(event.x, event.y) == None:
            #clear selection
            data.selectCount = 0
            if data.firstSelect != None:
                for (a, b) in isLegal(data.board, data.firstSelect):
                    data.board[a][b].highlight()
                (i, j) = data.firstSelect
                data.firstSelect = None
                data.board[i][j].select()
        else:
            # a piece is selected
            (i, j) = getLocation(event.x, event.y)
            # selected a piece to move
            if data.selectCount == 0 and data.board[i][j].piece != None and data.board[i][j].piece.side == data.turn:
                data.selectCount += 1
                data.board[i][j].select()
                data.firstSelect = (i, j)
                for (a, b) in isLegal(data.board, data.firstSelect):
                    data.board[a][b].highlight()
            # selected a spot to move to
            elif data.selectCount == 1:
                if (i, j) in isLegal(data.board, data.firstSelect):
                    (a, b) = data.firstSelect
                    if data.board[i][j].piece == None:
                        data.board[i][j].piece = data.board[a][b].piece
                        data.board[a][b].piece = None
                    else: 
                        # two pieces contact
                        contactWithGameOverCheck(a, b, i, j, data)
                    data.firstSelect = None
                    data.selectCount = 0
                    data.countdown = 20
                    data.turn = "A"
                    for x in range(12):
                        for y in range(5):
                            if data.board[x][y].highlighted:
                                data.board[x][y].highlighted = False
                            if data.board[x][y].selected:
                                data.board[x][y].selected = False


def keyPressed(event, data):
    # enter help mode
    if event.char == "h" and data.mode != "help" and data.mode != "help2":
        data.lastMode = data.mode
        data.mode = "help"
    # return to game
    elif event.char == "r":
        data.mode = data.lastMode
    # next page in help mode
    elif event.char == "n" and data.mode == "help":
        data.mode = "help2"
    # restart game
    elif event.char == "s":
        myPID = data.myPID
        otherPlayerOnline = data.otherPlayerOnline
        init(data)
        data.myPID = myPID
        data.otherPlayerOnline = otherPlayerOnline
    # getting AI-suggested move
    elif data.mode == "twoPlayerGame" and event.char == "a" and data.displaySuggestedMove == 0 and not data.darkMode:
        for x in range(12):
            for y in range(5):
                if data.board[x][y].highlighted:
                    data.board[x][y].highlighted = False
                if data.board[x][y].selected:
                    data.board[x][y].selected = False
        # get suggested A move
        if data.myPID == "PlayerA":
            
            board = copy.deepcopy(data.board)
            ((a, b, i, j), bestScore) = AIMove(board, 4) # maxDepth = 4
            data.move = (a, b, i, j)
            data.board[a][b].select()
            data.board[i][j].highlight()
            data.displaySuggestedMove = 1

        # get suggested B move
        elif data.myPID == "PlayerB":
            board = copy.deepcopy(data.board)
            ((a, b, i, j), bestScore) = PlayerMove(board, 4) # maxDepth = 4
            data.move = (a, b, i, j)
            data.board[a][b].select()
            data.board[i][j].highlight()
            data.displaySuggestedMove = 1




def getServerMsg(data):
    while serverMsg.qsize() > 0:
        if data.winner != None:
            break
        msg = serverMsg.get(False)
        try:
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]

            if command == "myIDis":
                myPID = msg[1]
                data.myPID = myPID

            elif command == "newPlayer":
                data.otherPlayerOnline = True

            elif data.mode == "twoPlayerLayout" and command == "playerSwitched":
                PID = msg[1]
                a = int(msg[2])
                b = int(msg[3])
                c = int(msg[4])
                d = int(msg[5])
                data.board[a][b].piece, data.board[c][d].piece = data.board[c][d].piece, data.board[a][b].piece

            elif data.mode == "twoPlayerGame" and command == "playerMoved":
                PID = msg[1]
                a = int(msg[2])
                b = int(msg[3])
                i = int(msg[4])
                j = int(msg[5])
                data.playerMove = (a, b, i, j)
                data.timer = 0

            elif command == "playerReady":
                data.otherPlayerReady = True
                print("received ready")

        except:
            print("failed")
        serverMsg.task_done()



def timerFired(data):
    getServerMsg(data)

    if data.selfPlayerReady and data.otherPlayerReady and data.mode == "twoPlayerLayout":
        data.mode = "twoPlayerGame"

    elif data.mode == "twoPlayerGame":
        # displaying AI-suggested move
        if data.displaySuggestedMove > 0:
            data.displaySuggestedMove += 1
        if data.displaySuggestedMove == 4:
            data.displaySuggestedMove = 0
            # undo suggestion
            (a, b, i, j) = data.move
            data.board[a][b].select()
            data.board[i][j].highlight()
            data.move = None

        # display move
        if data.timer == 0:
            data.timer += 1
            (a, b, i, j) = data.playerMove
            data.board[a][b].select()
        elif data.timer == 1:
            data.timer += 1
            (a, b, i, j) = data.playerMove
            data.board[i][j].highlight()

        # make move
        elif data.timer == 2:
            data.timer = None
            (a, b, i, j) = data.playerMove
            if data.board[i][j].piece == None:
                data.board[i][j].piece = data.board[a][b].piece
                data.board[a][b].piece = None
            else: # two pieces contact
                contactWithGameOverCheck(a, b, i, j, data)
            data.firstSelect = None
            data.selectCount = 0
            data.countdown = 20

            if data.turn == "B":
                data.turn = "A"
            else:
                data.turn = "B"

            marA = marB = False
            for x in range(12):
                for y in range(5):
                    if data.board[x][y].highlighted:
                        data.board[x][y].highlighted = False
                    if data.board[x][y].selected:
                        data.board[x][y].selected = False
                    if data.board[x][y].piece != None and data.board[x][y].piece.order == 9:
                        if data.board[x][y].piece.side == "A":
                            marA = True
                        else:
                            marB = True
            data.marA, data.marB = marA, marB

        # not making or displaying move
        else:
            data.countdown -= 1
            if data.countdown <= 0:
                data.countdown = 20
                data.firstSelect = None
                data.selectCount = 0
                if data.turn == "B":
                    data.turn = "A"
                else:
                    data.turn = "B"
                for x in range(12):
                    for y in range(5):
                        try:
                            if data.board[x][y].highlighted:
                                data.board[x][y].highlighted = False
                            if data.board[x][y].selected:
                                data.board[x][y].selected = False
                        except:
                            pass

    elif data.mode == "onePlayerGame":
        data.countdown -= 1
        if data.countdown <= 0:
            data.countdown = 20
            data.firstSelect = None
            data.selectCount = 0
            if data.turn == "B":
                data.turn = "A"
            else:
                data.turn = "B"
            for x in range(12):
                for y in range(5):
                    try:
                        if data.board[x][y].highlighted:
                            data.board[x][y].highlighted = False
                        if data.board[x][y].selected:
                            data.board[x][y].selected = False
                    except:
                        pass
        # get AI move
        if data.turn == "A" and data.countdown == 19 and data.winner == None:
            board = copy.deepcopy(data.board)
            ((a, b, i, j), bestScore) = AIMove(board, data.maxDepth)
            data.move = (a, b, i, j)
            data.board[a][b].select()

        # display AI move
        elif data.turn == "A" and data.countdown == 18 and data.winner == None and data.move != None:
            (a, b, i, j) = data.move
            data.board[i][j].highlight()

        elif data.turn == "A" and data.countdown == 17 and data.winner == None and data.move != None:
            (a, b, i, j) = data.move
            # undo highlight and selection
            data.board[a][b].select()
            data.board[i][j].highlight()
            data.move = None
            # make move
            if data.board[i][j].piece == None:
                data.board[i][j].piece = data.board[a][b].piece
                data.board[a][b].piece = None
            else: # two pieces contact
                contactWithGameOverCheck(a, b, i, j, data)
            data.turn = "B"
            data.countdown = 20


def redrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.background)

    if data.mode == "start":
        drawStartPage(canvas, data)

    elif data.mode == "selectDifficulty":
        canvas.create_text(300, 180, text="Select Difficulty", font="Copperplate 50")

        #canvas.create_rectangle(200, 340, 400, 400, width=3)
        canvas.create_line(210, 340, 390, 340, width=3)
        canvas.create_line(210, 400, 390, 400, width=3)
        canvas.create_line(200, 350, 200, 390, width=3)
        canvas.create_line(400, 350, 400, 390, width=3)
        canvas.create_arc(200, 340, 220, 360, start=90, extent=90, width=3, style="arc")
        canvas.create_arc(380, 340, 400, 360, start=0, extent=90, width=3, style="arc")
        canvas.create_arc(200, 380, 220, 400, start=180, extent=90, width=3, style="arc")
        canvas.create_arc(380, 380, 400, 400, start=270, extent=90, width=3, style="arc")
        canvas.create_text(300, 370, text="Easy", font="Arial 23")

        #canvas.create_rectangle(200, 420, 400, 480, width=3)
        canvas.create_line(210, 420, 390, 420, width=3)
        canvas.create_line(210, 480, 390, 480, width=3)
        canvas.create_line(200, 430, 200, 470, width=3)
        canvas.create_line(400, 430, 400, 470, width=3)
        canvas.create_arc(200, 420, 220, 440, start=90, extent=90, width=3, style="arc")
        canvas.create_arc(380, 420, 400, 440, start=0, extent=90, width=3, style="arc")
        canvas.create_arc(200, 460, 220, 480, start=180, extent=90, width=3, style="arc")
        canvas.create_arc(380, 460, 400, 480, start=270, extent=90, width=3, style="arc")
        canvas.create_text(300, 450, text="Hard", font="Arial 23")

    elif data.mode == "help":
        drawHelpPage(canvas, data)
    elif data.mode == "help2":
        drawHelp2Page(canvas, data)

    elif data.mode == "twoPlayerLayout":
        drawBoardSkeleton(canvas, data)
        # drawing posts
        if data.myPID == "PlayerA":
            for x in range(len(data.board)):
                for y in range(len(data.board[0])):
                    if x < 6:
                        data.board[x][y].reversedDraw(canvas)
                    else: 
                    # hiding opponent's layout
                        data.board[x][y].reversedDrawDark(canvas)
        else:
            for x in range(len(data.board)):
                for y in range(len(data.board[0])):
                    if x >= 6:
                        data.board[x][y].draw(canvas)
                    else:
                    # hiding opponent's layout
                        data.board[x][y].drawDark(canvas)
        
        canvas.create_text(175, 420, text="Press \"H\" for help", font="Arial 15")

        if data.otherPlayerOnline:
            canvas.create_text(175, 380, text="To rearrange layout,", font="Arial 15")
            canvas.create_text(175, 400, text="select pieces to switch", font="Arial 15")
            if not data.selfPlayerReady:
                #canvas.create_rectangle(385, 380, 465, 420, width=2)
                canvas.create_line(390, 380, 460, 380, width=2)
                canvas.create_line(390, 420, 460, 420, width=2)
                canvas.create_line(385, 385, 385, 415, width=2)
                canvas.create_line(465, 385, 465, 415, width=2)
                canvas.create_arc(385, 380, 395, 390, start=90, extent=90, style="arc", width=2)
                canvas.create_arc(455, 380, 465, 390, start=0, extent=90, style="arc", width=2)
                canvas.create_arc(385, 410, 395, 420, start=180, extent=90, style="arc", width=2)
                canvas.create_arc(455, 410, 465, 420, start=270, extent=90, style="arc", width=2)
                canvas.create_text(425, 400, text="READY", font="Arial 20")
            else:
                canvas.create_text(425, 390, text="Waiting for the other", font="Arial 15")
                canvas.create_text(425, 410, text="player to complete layout...", font="Arial 15")
        else:
            canvas.create_text(425, 390, text="Waiting for the other", font="Arial 15")
            canvas.create_text(425, 410, text="player to get online...", font="Arial 15")

        if data.errorMsg != None:
            canvas.create_rectangle(0, 370, 600, 430, fill="red3")
            canvas.create_text(300, 400, text=data.errorMsg, font="Arial 20")

    elif data.mode == "onePlayerLayout":
        drawBoardSkeleton(canvas, data)
        for x in range(len(data.board)):
            for y in range(len(data.board[0])):
                if x < 6:
                    # hiding AI's layout
                    data.board[x][y].drawDark(canvas)
                else:
                    data.board[x][y].draw(canvas)

        canvas.create_text(175, 380, text="To rearrange layout,", font="Arial 15")
        canvas.create_text(175, 400, text="select pieces to switch", font="Arial 15")
        canvas.create_text(175, 420, text="Press \"H\" for help", font="Arial 15")
        #canvas.create_rectangle(385, 380, 465, 420, width=2)
        canvas.create_line(390, 380, 460, 380, width=2)
        canvas.create_line(390, 420, 460, 420, width=2)
        canvas.create_line(385, 385, 385, 415, width=2)
        canvas.create_line(465, 385, 465, 415, width=2)
        canvas.create_arc(385, 380, 395, 390, start=90, extent=90, style="arc", width=2)
        canvas.create_arc(455, 380, 465, 390, start=0, extent=90, style="arc", width=2)
        canvas.create_arc(385, 410, 395, 420, start=180, extent=90, style="arc", width=2)
        canvas.create_arc(455, 410, 465, 420, start=270, extent=90, style="arc", width=2)
        canvas.create_text(425, 400, text="START", font="Arial 20")

        if data.errorMsg != None:
            canvas.create_rectangle(0, 370, 600, 430, fill="red3")
            canvas.create_text(300, 400, text=data.errorMsg, font="Arial 20")

    elif data.mode == "twoPlayerGame":
        drawBoardSkeleton(canvas, data)
        # drawing posts
        if data.myPID == "PlayerA":
            for x in range(len(data.board)):
                for y in range(len(data.board[0])):
                    if data.darkMode:
                        # hide opponent's pieces
                        if data.board[x][y].piece != None and data.board[x][y].piece.side == "B":
                            # flag is revealed when Marshall is dead
                            if data.board[x][y].piece.order == 0 and not data.marB:
                                data.board[x][y].reversedDraw(canvas)
                            else:
                                data.board[x][y].reversedDrawDark(canvas)
                        else:
                            data.board[x][y].reversedDraw(canvas)
                    else:
                        data.board[x][y].reversedDraw(canvas)

        else:
            for x in range(len(data.board)):
                for y in range(len(data.board[0])):
                    if data.darkMode:
                        # hide opponent's pieces
                        if data.board[x][y].piece != None and data.board[x][y].piece.side == "A":
                            # flag is revealed when Marshall is dead
                            if data.board[x][y].piece.order == 0 and not data.marA:
                                data.board[x][y].draw(canvas)
                            else:
                                data.board[x][y].drawDark(canvas)
                        else:
                            data.board[x][y].draw(canvas)
                    else:
                        data.board[x][y].draw(canvas)

        if data.darkMode:
            canvas.create_text(175, 390, text="Press \"H\" for help", font="Arial 15")
            canvas.create_text(175, 410, text="Press \"S\" to restart game", font="Arial 15")
        else:
            canvas.create_text(175, 380, text="Press \"A\" for AI-suggested move", font="Arial 15")
            canvas.create_text(175, 400, text="Press \"H\" for help", font="Arial 15")
            canvas.create_text(175, 420, text="Press \"S\" to restart game", font="Arial 15")

        if data.timer != None: 
            # display move
            canvas.create_text(425, 390, text="Making move...", font="Arial 15")
        elif data.turn == "B":
            canvas.create_text(425, 390, text="Blue Player's Turn", font="Arial 15")
            canvas.create_text(425, 410, text="Time remaining: "+str(data.countdown), font="Arial 15")
        else:
            canvas.create_text(425, 390, text="Orange Player's Turn", font="Arial 15")
            canvas.create_text(425, 410, text="Time remaining: "+str(data.countdown), font="Arial 15")
            
        if data.winner != None:
            # displaying game-over message
            canvas.create_rectangle(0, 370, 600, 430, fill="red3")
            if (data.winner == "A" and data.myPID == "PlayerA") or (data.winner == "B" and data.myPID == "PlayerB"):
                canvas.create_text(300, 400, text="You win! Press \"S\" to restart", font="Arial 28")
            else:
                canvas.create_text(300, 400, text="You lose! Press \"S\" to restart", font="Arial 28")

    elif data.mode == "onePlayerGame":
        drawBoard(canvas, data)
        canvas.create_text(175, 390, text="Press \"H\" for help", font="Arial 15")
        canvas.create_text(175, 410, text="Press \"S\" to restart game", font="Arial 15")

        if data.turn == "B":
            canvas.create_text(425, 390, text="Your Turn", font="Arial 15")
            canvas.create_text(425, 410, text="Time remaining: "+str(data.countdown), font="Arial 15")
        else:
            canvas.create_text(425, 390, text="AI Player's Turn", font="Arial 15")

        if data.winner != None:
            # display game-over message
            canvas.create_rectangle(0, 370, 600, 430, fill="red3")
            if data.winner == "A":
                canvas.create_text(300, 400, text="You lose! Press \"S\" to restart", font="Arial 28")
            else:
                canvas.create_text(300, 400, text="You win! Press \"S\" to restart", font="Arial 28")


def drawStartPage(canvas, data):
    canvas.create_text(300, 180, text="Land Battle Chess", font="Copperplate 50")
    canvas.create_text(300, 240, text="Carnegie Mellon University", font="Arial 18")
    canvas.create_text(300, 270, text="15-112 Term Project", font="Arial 18")
    canvas.create_text(300, 300, text="by Yiwen (Victor) Song", font="Arial 18")

    #canvas.create_rectangle(200, 340, 400, 400, width=3)
    canvas.create_line(210, 340, 390, 340, width=3)
    canvas.create_line(210, 400, 390, 400, width=3)
    canvas.create_line(200, 350, 200, 390, width=3)
    canvas.create_line(400, 350, 400, 390, width=3)
    canvas.create_arc(200, 340, 220, 360, start=90, extent=90, width=3, style="arc")
    canvas.create_arc(380, 340, 400, 360, start=0, extent=90, width=3, style="arc")
    canvas.create_arc(200, 380, 220, 400, start=180, extent=90, width=3, style="arc")
    canvas.create_arc(380, 380, 400, 400, start=270, extent=90, width=3, style="arc")
    canvas.create_text(300, 370, text="Play singleplayer", font="Arial 23")

    #canvas.create_rectangle(200, 420, 400, 480, width=3)
    canvas.create_line(210, 420, 390, 420, width=3)
    canvas.create_line(210, 480, 390, 480, width=3)
    canvas.create_line(200, 430, 200, 470, width=3)
    canvas.create_line(400, 430, 400, 470, width=3)
    canvas.create_arc(200, 420, 220, 440, start=90, extent=90, width=3, style="arc")
    canvas.create_arc(380, 420, 400, 440, start=0, extent=90, width=3, style="arc")
    canvas.create_arc(200, 460, 220, 480, start=180, extent=90, width=3, style="arc")
    canvas.create_arc(380, 460, 400, 480, start=270, extent=90, width=3, style="arc")
    canvas.create_text(300, 450, text="Play multiplayer", font="Arial 23")

    #canvas.create_rectangle(200, 500, 400, 580, width=3)
    canvas.create_line(210, 500, 390, 500, width=3)
    canvas.create_line(210, 580, 390, 580, width=3)
    canvas.create_line(200, 510, 200, 570, width=3)
    canvas.create_line(400, 510, 400, 570, width=3)
    canvas.create_arc(200, 500, 220, 520, start=90, extent=90, width=3, style="arc")
    canvas.create_arc(380, 500, 400, 520, start=0, extent=90, width=3, style="arc")
    canvas.create_arc(200, 560, 220, 580, start=180, extent=90, width=3, style="arc")
    canvas.create_arc(380, 560, 400, 580, start=270, extent=90, width=3, style="arc")
    canvas.create_text(300, 525, text="Play multiplayer", font="Arial 23")
    canvas.create_text(300, 555, text="(Dark Mode)", font="Arial 23")

    canvas.create_text(300, 640, text="Press \"H\" for game instructions", font="Arial 23")

def drawHelpPage(canvas, data):
    canvas.create_text(300, 60, text="Help Manual", font="Copperplate 35")
    canvas.create_text(50, 100, text="Welcome to the Land Battle Chess game! The following introduction", anchor="w", font="Arial 15")
    canvas.create_text(50, 120, text="is partly derived from https://en.wikipedia.org/wiki/Luzhanqi", anchor="w", font="Arial 15")
    canvas.create_text(50, 150, text="The aim of the game is to capture the opponent flag through penetrating", anchor="w", font="Arial 15")
    canvas.create_text(50, 170, text="the defenses. Each player arranges the layout of their pieces prior to the game.", anchor="w", font="Arial 15")
    canvas.create_text(50, 200, text="There are 3 kinds of stations: Posts, Camps, and Headquarters.", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 220, 100, 244, fill="PaleGreen3")
    canvas.create_text(120, 232, text="Post: a piece can move on or off and can be attacked on a post", anchor="w", font="Arial 15")
    canvas.create_oval(50, 260, 100, 300, fill="PaleGreen3")
    canvas.create_text(120, 280, text="Camp: a piece in a camp cannot be attacked", anchor="w", font="Arial 15")
    canvas.create_oval(75-25/2, 342-24, 75+25/2, 342, fill="black")
    canvas.create_oval(75-25/2, 342, 75+25/2, 342+24, fill="black")
    canvas.create_rectangle(50, 330, 100, 354, fill="PaleGreen3")
    canvas.create_text(120, 332, text="Headquarter: pieces may only move in but not out of a headquarter", anchor="w", font="Arial 15")
    canvas.create_text(120, 352, text="The Flag must be placed on one of the two headquarters of each side", anchor="w", font="Arial 15")
    canvas.create_text(50, 400, text="Posts/Camps/Headquarters are connected by either a Road or a Railroad.", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 430, 100, 454, fill="PaleGreen3")
    canvas.create_rectangle(50, 490, 100, 514, fill="PaleGreen3")
    canvas.create_line(75, 454, 75, 490)
    canvas.create_text(120, 462, text="Road: marked as thin lines on the board", anchor="w", font="Arial 15")
    canvas.create_text(120, 482, text="A piece can only travel one space across a road in one move", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 530, 100, 554, fill="PaleGreen3")
    canvas.create_rectangle(50, 590, 100, 614, fill="PaleGreen3")
    canvas.create_line(75, 554, 75, 590, width=3)
    canvas.create_text(120, 552, text="Railroad: marked as thick lines on the board", anchor="w", font="Arial 15")
    canvas.create_text(120, 572, text="A piece can travel multiple spaces along a railroad in a straight line", anchor="w", font="Arial 15")
    canvas.create_text(120, 592, text="as long as its path is not obstructed by another piece", anchor="w", font="Arial 15")
    canvas.create_text(50, 660, text="Press \"N\" to see next page about the different pieces.", anchor="w", font="Arial 15")
    canvas.create_text(50, 690, text="Press \"R\" to return to game", anchor="w", font="Arial 15")

def drawHelp2Page(canvas, data):
    canvas.create_text(300, 60, text="Help Manual (cont'd)", font="Copperplate 35")
    canvas.create_rectangle(50, 90, 100, 114, fill="deep sky blue")
    canvas.create_text(75, 102, text="Mar10")
    canvas.create_text(120, 102, text="Marshal * 1: order 10, highest order piece. In Dark Mode,", anchor="w", font="Arial 15")
    canvas.create_text(205, 122, text="the flag is revealed when the Marshall is dead", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 140, 100, 164, fill="deep sky blue")
    canvas.create_text(75, 152, text="Gen9")
    canvas.create_text(120, 152, text="General * 2: order 9", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 180, 100, 204, fill="deep sky blue")
    canvas.create_text(75, 192, text="MGen8")
    canvas.create_text(120, 192, text="Major General * 2: order 8", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 220, 100, 244, fill="deep sky blue")
    canvas.create_text(75, 232, text="BGen7")
    canvas.create_text(120, 232, text="Brigadier General * 2: order 7", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 260, 100, 284, fill="deep sky blue")
    canvas.create_text(75, 272, text="Col6")
    canvas.create_text(120, 272, text="Colonel * 2: order 6", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 300, 100, 324, fill="deep sky blue")
    canvas.create_text(75, 312, text="Maj5")
    canvas.create_text(120, 312, text="Major * 2: order 5", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 340, 100, 364, fill="deep sky blue")
    canvas.create_text(75, 352, text="Capt4")
    canvas.create_text(120, 352, text="Captain * 3: order 4", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 380, 100, 404, fill="deep sky blue")
    canvas.create_text(75, 392, text="Lt3")
    canvas.create_text(120, 392, text="Lieutenant * 3: order 3", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 420, 100, 444, fill="deep sky blue")
    canvas.create_text(75, 432, text="Spr2")
    canvas.create_text(120, 432, text="Sapper * 3: order 2, can turn corners when travelling along Railroad", anchor="w", font="Arial 15")
    canvas.create_text(200, 450, text="and can capture landmines", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 470, 100, 494, fill="deep sky blue")
    canvas.create_text(75, 482, text="Bomb")
    canvas.create_text(120, 482, text="Bomb * 2: when a bomb comes in contact with an enemy piece,", anchor="w", font="Arial 15")
    canvas.create_text(190, 500, text="both pieces are removed from the board; ", anchor="w", font="Arial 15")
    canvas.create_text(190, 518, text="bombs cannot initially be placed on the first rank", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 540, 100, 564, fill="deep sky blue")
    canvas.create_text(75, 552, text="LMN")
    canvas.create_text(120, 552, text="Landmine * 3: immune to any attack except when captured by a", anchor="w", font="Arial 15")
    canvas.create_text(210, 570, text="Sapper or co-destroyed by a bomb; landmines can", anchor="w", font="Arial 15")
    canvas.create_text(210, 588, text="only be placed on the last two ranks and cannot move", anchor="w", font="Arial 15")
    canvas.create_rectangle(50, 610, 100, 634, fill="deep sky blue")
    canvas.create_text(75, 622, text="Flag1")
    canvas.create_text(120, 622, text="Flag * 1: can be captured by any enemy piece, which ends the game;", anchor="w", font="Arial 15")
    canvas.create_text(180, 640, text="the Flag must be placed at a headquarter and cannot move", anchor="w", font="Arial 15")
    canvas.create_text(50, 690, text="Press \"R\" to return to game", anchor="w", font="Arial 15")


def drawBoard(canvas, data):
    drawBoardSkeleton(canvas, data)
    # drawing posts
    for x in range(len(data.board)):
        for y in range(len(data.board[0])):
            data.board[x][y].draw(canvas)

def drawBoardSkeleton(canvas, data):
    # margin = 50
    # drawing railroads
    canvas.create_line(50, 110, 50, 690, width=3)
    canvas.create_line(50, 110, 550, 110, width=3)
    canvas.create_line(50, 690, 550, 690, width=3)
    canvas.create_line(550, 110, 550, 690, width=3)
    canvas.create_line(50, 350, 550, 350, width=3)
    canvas.create_line(50, 450, 550, 450, width=3)
    canvas.create_line(300, 350, 300, 450, width=3)
    # drawing roads
    for i in range(50, 400, 60):
        canvas.create_line(50, i, 550, i)
    for i in range(750, 500, -60):
        canvas.create_line(50, i, 550, i)
    for i in range(50, 600, 250):
        canvas.create_line(i, 50, i, 750)
    canvas.create_line(175, 50, 175, 350)
    canvas.create_line(425, 50, 425, 350)
    canvas.create_line(175, 450, 175, 750)
    canvas.create_line(425, 450, 425, 750)
    canvas.create_line(50, 110, 550, 350)
    canvas.create_line(300, 110, 550, 230)
    canvas.create_line(50, 230, 300, 350)
    canvas.create_line(50, 350, 550, 110)
    canvas.create_line(50, 230, 300, 110)
    canvas.create_line(300, 350, 550, 230)
    canvas.create_line(50, 450, 550, 690)
    canvas.create_line(300, 450, 550, 570)
    canvas.create_line(50, 570, 300, 690)
    canvas.create_line(50, 570, 300, 450)
    canvas.create_line(50, 690, 550, 450)
    canvas.create_line(300, 690, 550, 570)


#################################################################
# the run function is derived from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#starter-code
# with modifications for Socket module

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(600, 800, serverMsg, server)




