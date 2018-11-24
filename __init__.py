from pieceClasses import *

getCoord = {}  # This dictionary maps the coordinate of a post to its x and y location on canvas
for x in range(5):
    for y in range(12):
            if y < 6:
                getCoord[(y, x)] = (50 + 125 * x, 50 + 60 * y)
            else:
                getCoord[(y, x)] = (50 + 125 * x, 450 + 60 * (y - 6))

def getLocation(x, y):
    for (i, j) in getCoord:
        (a, b) = getCoord[(i, j)]
        if a - 25 < x < a + 25 and b - 12 < y < b + 12:
            return (i, j)


class Post():
    def __init__(self, x, y, piece=None):  # x, y are center coordinates
        self.x, self.y = getCoord[x, y]
        self.w = 25
        self.h = 12
        self.piece = piece
        self.selected = False
        self.highlighted = False

    def select(self):
        self.selected = not self.selected

    def highlight(self):
        self.highlighted = not self.highlighted

    def draw(self, canvas):
        if self.highlighted:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="white", outline="lime green", width=3)
        elif self.selected:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="white", outline="red3", width=3)
        else:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill="white")
        if self.piece != None:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill=self.piece.color)
            canvas.create_text(self.x, self.y, text=self.piece.name)


class Camp(Post):
    def draw(self, canvas):
        if self.highlighted:
            canvas.create_oval(self.x - self.w, self.y - self.w + 5, self.x +
                               self.w, self.y + self.w - 5, fill="white", outline="lime green", width=3)
        elif self.selected:
            canvas.create_oval(self.x - self.w, self.y - self.w + 5, self.x +
                               self.w, self.y + self.w - 5, fill="white", outline="red3", width=3)
        else:
            canvas.create_oval(self.x - self.w, self.y - self.w + 5,
                               self.x + self.w, self.y + self.w - 5, fill="white")
        if self.piece != None:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill=self.piece.color)
            canvas.create_text(self.x, self.y, text=self.piece.name)


class Headquarters(Post):
    def draw(self, canvas):
        if self.highlighted:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="white", outline="lime green", width=3)
        elif self.selected:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="white", outline="red3", width=3)
        else:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill="white")
        canvas.create_oval(self.x - self.w / 2, self.y - 2 * self.h,
                           self.x + self.w / 2, self.y, fill="black")
        canvas.create_oval(self.x - self.w / 2, self.y, self.x +
                           self.w / 2, self.y + 2 * self.h, fill="black")
        if self.piece != None:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color)
                canvas.create_text(self.x, self.y, text=self.piece.name)




railroadPosts = set()
for i in range(1, 11):
    railroadPosts.add((i, 0))
    railroadPosts.add((i, 4))
for i in range(0, 5):
    railroadPosts.add((1, i))
    railroadPosts.add((5, i))
    railroadPosts.add((6, i))
    railroadPosts.add((10, i))

def isValid(data):
    (a, b) = data.firstSelect
    valid = set()
    if data.board[a][b].piece.order == 10 or isinstance(data.board[a][b], Headquarters): # landmines and pieces in headquarters cannot move
        return valid
    # searching adjacent moves
    for (c, d) in [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]:
        if 0 <= c <= 11 and 0 <= d <= 4 and (data.board[c][d].piece == None or \
        (data.board[c][d].piece.side != data.board[a][b].piece.side and \
        not isinstance(data.board[c][d], Camp))): # pieces in camps are protected from attack
            valid.add((c, d))
    for (c, d) in [(a-1, b-1), (a-1, b+1), (a+1, b-1), (a+1, b+1)]:
        if 0 <= c <= 11 and 0 <= d <= 4 and isinstance(data.board[c][d], Camp) and data.board[c][d].piece == None:
            valid.add((c, d))
    if isinstance(data.board[a][b], Camp):
        for (c, d) in [(a-1, b-1), (a-1, b+1), (a+1, b-1), (a+1, b+1)]:
            if 0 <= c <= 11 and 0 <= d <= 4:
                if data.board[c][d].piece == None or \
                (data.board[c][d].piece.side != data.board[a][b].piece.side and not isinstance(data.board[c][d], Camp)):
                    valid.add((c, d))
    if (a, b) in [(5, 1), (6, 1), (5, 3), (6, 3)]:
        valid.discard((5, 1))
        valid.discard((6, 1))
        valid.discard((5, 3))
        valid.discard((6, 3))

    if (a, b) in railroadPosts:
        if data.board[a][b].piece.order == 1: # finding railroad path for Sappers
            lst = []
            if (a, b) in [(5, 1), (5, 3), (6, 1), (6, 3)]:
                lst = findSprPaths(a, b-1, a, b, data, lst) + findSprPaths(a, b+1, a, b, data, lst)
            else:
                lst = findSprPaths(a-1, b, a, b, data, lst) + findSprPaths(a+1, b, a, b, data, lst) + findSprPaths(a, b-1, a, b, data, lst) + findSprPaths(a, b+1, a, b, data, lst)
            for (i, j) in lst:
                valid.add((i, j))
        else: # finding railroad path for regular pieces
            if (b == 0 or b == 4) and 1 <= a <= 10:
                (c, d) = (a, b)
                c += 1
                while (1 <= c <= 10 and data.board[c][d].piece == None):
                    c += 1
                    if c <= 10 and (data.board[c][d].piece == None or data.board[c][d].piece.side != data.board[a][b].piece.side):
                        valid.add((c, d))
                (c, d) = (a, b)
                c -= 1
                while (1 <= c <= 10 and data.board[c][d].piece == None):
                    c -= 1
                    if c >= 1 and (data.board[c][d].piece == None or data.board[c][d].piece.side != data.board[a][b].piece.side):
                        valid.add((c, d))
            if a == 5 or a == 6:
                (c, d) = (a, b)
                d += 1
                while (0 <= d <= 4 and data.board[c][d].piece == None):
                    d += 1
                    if d <= 4 and (data.board[c][d].piece == None or data.board[c][d].piece.side != data.board[a][b].piece.side):
                        valid.add((c, d))
                (c, d) = (a, b)
                d -= 1
                while (0 <= d <= 4 and data.board[c][d].piece == None):
                    d -= 1
                    if d >= 0 and (data.board[c][d].piece == None or data.board[c][d].piece.side != data.board[a][b].piece.side):
                        valid.add((c, d))
    valid.discard((a, b))
    return valid

def findSprPaths(a, b, i, j, data, lst): # finding railroad path for Sappers
    if (a, b) not in railroadPosts:
        return []
    elif (a, b) in lst:
        return []
    elif data.board[a][b].piece != None:
        if data.board[a][b].piece.side != data.board[i][j].piece.side:
            return [(a, b)]
        else:
            return []
    elif (a, b) in [(5, 1), (5, 3), (6, 1), (6, 3)]:
        lst.append((a, b))
        return [(a, b)] + findSprPaths(a, b-1, i, j, data, lst) + findSprPaths(a, b+1, i, j, data, lst)
    else:
        lst.append((a, b))
        return [(a, b)] + findSprPaths(a-1, b, i, j, data, lst) + findSprPaths(a+1, b, i, j, data, lst) + findSprPaths(a, b-1, i, j, data, lst) + findSprPaths(a, b+1, i, j, data, lst)





def drawBoard(canvas, data):
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
    # drawing posts
    for x in range(len(data.board)):
        for y in range(len(data.board[0])):
            data.board[x][y].draw(canvas)


#### Graphics Functions ####

from tkinter import *


def init(data):
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
    data.isOver = False


def mousePressed(event, data):
    if data.mode == "start":
        if 250 < event.x < 350 and 370 < event.y < 430:
            data.mode = "layout"
    elif data.mode == "layout":
        if 385 < event.x < 465 and 380 < event.y < 420:
            data.selectCount = 0
            data.firstSelect = None
            data.mode = "game"
        if getLocation(event.x, event.y) != None:
            (i, j) = getLocation(event.x, event.y)
            if type(data.board[i][j]) == Camp:
                return None
            data.selectCount += 1
            data.board[i][j].select()
            if data.selectCount == 1:
                data.firstSelect = (i, j)
            elif data.selectCount == 2:
                data.selectCount = 0
                data.secondSelect = (i, j)
                (a, b) = data.firstSelect
                (c, d) = data.secondSelect
                data.board[a][b].select()
                data.board[c][d].select()
                # pieces must stay within their own side
                if data.board[a][b].piece.side != data.board[c][d].piece.side:
                    return None
                # flags must remain in headquarters
                if ((a, b) == (0, 1) or (a, b) == (0, 3)) and data.board[a][b].piece.order == 0 and ((c, d) != (0, 1) and (c, d) != (0, 3)):
                    return None
                if ((a, b) == (11, 1) or (a, b) == (11, 3)) and data.board[a][b].piece.order == 0 and ((c, d) != (11, 1) and (c, d) != (11, 3)):
                    return None
                if ((c, d) == (0, 1) or (c, d) == (0, 3)) and data.board[c][d].piece.order == 0 and ((a, b) != (0, 1) and (a, b) != (0, 3)):
                    return None
                if ((c, d) == (11, 1) or (c, d) == (11, 3)) and data.board[c][d].piece.order == 0 and ((a, b) != (11, 1) and (a, b) != (11, 3)):
                    return None
                # bombs cannot be in the front row
                if data.board[a][b].piece.order == None and (c == 5 or c == 6):
                    return None
                if data.board[c][d].piece.order == None and (a == 5 or a == 6):
                    return None
                # landmines must remain at the last two rows
                if data.board[a][b].piece.order == 10 and (c in [2, 3, 4, 5, 6, 7, 8, 9]):
                    return None
                if data.board[c][d].piece.order == 10 and (a in [2, 3, 4, 5, 6, 7, 8, 9]):
                    return None
                data.board[a][b].piece, data.board[c][d].piece = data.board[c][d].piece, data.board[a][b].piece
    elif data.mode == "game":
        if getLocation(event.x, event.y) == None:
            data.selectCount = 0
            if data.firstSelect != None:
                for (a, b) in isValid(data):
                    data.board[a][b].highlight()
                (i, j) = data.firstSelect
                data.firstSelect = None
                data.board[i][j].select()
        else:
            (i, j) = getLocation(event.x, event.y)
            if data.selectCount == 0 and data.board[i][j].piece != None and data.board[i][j].piece.side == data.turn:
                data.selectCount += 1
                data.board[i][j].select()
                data.firstSelect = (i, j)
                for (a, b) in isValid(data):
                    data.board[a][b].highlight()
            elif data.selectCount == 1:
                if (i, j) in isValid(data):
                    (a, b) = data.firstSelect
                    if data.board[i][j].piece == None:
                        data.board[i][j].piece = data.board[a][b].piece
                        data.board[a][b].piece = None
                    else: # two pieces contact
                        contact(a, b, i, j, data)
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


def contact(a, b, i, j, data):
    if data.board[a][b].piece.order == 0 or data.board[i][j].piece.order == 0:
        data.isOver = True
    if data.board[a][b].piece.order == None or data.board[i][j].piece.order == None or \
    data.board[a][b].piece.order == data.board[i][j].piece.order:
        data.board[a][b].piece = None
        data.board[i][j].piece = None
        print("both destroyed")
    elif data.board[a][b].piece.order > data.board[i][j].piece.order:
        data.board[i][j].piece = data.board[a][b].piece
        data.board[a][b].piece = None
        print("capture")
    else:
        data.board[a][b].piece = None
        print("defeated")


def keyPressed(event, data):
    if event.char == "h":
        if data.mode != "help":
            data.lastMode = data.mode
            data.mode = "help"
        else:
            data.mode = data.lastMode
    elif event.char == "s" and data.isOver:
        init(data)



def timerFired(data):
    if data.mode == "game":
        data.countdown -= 1
        if data.countdown <= 0:
            data.countdown = 0 
            # TODO: time is up


def redrawAll(canvas, data):
    if data.mode == "start":
        canvas.create_rectangle(250, 370, 350, 430, outline="red3", width=3)
        canvas.create_text(300, 400, text="PLAY", font="Arial 28")
    elif data.mode == "help":
        drawHelpPage(canvas, data)
    elif data.mode == "layout":
        drawBoard(canvas, data)
        canvas.create_text(175, 400, text="Press \"H\" for help")
        canvas.create_rectangle(385, 380, 465, 420, outline="red3", width=3)
        canvas.create_text(425, 400, text="START", font="Arial 20")
    elif data.mode == "game":
        drawBoard(canvas, data)
        canvas.create_text(175, 400, text="Press \"H\" for help")
        canvas.create_text(425, 400, text="Time remaining: "+str(data.countdown))
        if data.isOver:
            canvas.create_rectangle(0, 370, 600, 430, fill="red3")
            canvas.create_text(300, 400, text="Game Over! Press \"s\" to restart", font="Arial 28")

def drawHelpPage(canvas, data):
    canvas.create_text(300, 50, text="Help Manual", font="Arial 28 bold")



#################################################################
# the run function is copied from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#starter-code

def run(width, height):
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

run(600, 800)
