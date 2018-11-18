class Pawn():
	def __init__(self, order, loc):
		self.order = order

	def draw():
		pass


class Bomb(Pawn):
	def __init__(self):
		pass

class Lmn(Pawn):
	pass

class Station():
	def __init__(self, x, y, w=10, h=5): # x, y are center coordinates
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def draw(self, canvas):
		canvas.create_rectangle(self.x-self.w, self.y-self.h, self.x+self.w, self.y+self.h)

class Camp(Station):
	def draw(self, canvas):
		canvas.create_oral(self.x-self.w, self.y-self.h, self.x+self.w, self.y+self.w)

class BaseCamp(Station):
	def draw(self, canvas):
		canvas.create_oval(self.x-self.w/2, self.y-2*self.h, self.x+self.w/2, self.y+2*self.h, fill="black")
		canvas.create_rectangle(self.x-self.w, self.y-self.h, self.x+self.w, self.y+self.h, fill="white")

def hit(p1, p2):
	if p1.order == 10 or p2.order == 10:
		return None
	elif p1.order == 11:
		return p1
	elif p2.order == 11:
		return p2
	elif p1.order == p2.order:
		return None
	elif p1.order > p2.order:
		return p1
	else:
		return p2

def drawBoard(canvas, data):
	# margin = 50
	canvas.create_line(50, 110, 50, 690, width=3)
	canvas.create_line(50, 110, 550, 110, width=3)
	canvas.create_line(50, 690, 550, 690, width=3)
	canvas.create_line(550, 110, 550, 690, width=3)
	canvas.create_line(50, 350, 550, 350, width=3)
	canvas.create_line(50, 450, 550, 450, width=3)
	canvas.create_line(300, 350, 300, 450, width=3)
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
	




#### Graphics Functions ####

from tkinter import *

def init(data):
    data.countdown = 20
    data.isPaused = False
    data.board = [[None] * 5] * 12
    data.mode = "start"
    data.lastMode = data.mode


def mousePressed(event, data):
    if data.mode == "start":
    	if 250 < event.x < 350 and 370 < event.y < 430:
    		data.mode = "game"

def keyPressed(event, data):
    if event.char == "h":
    	if data.mode != "help":
    		data.lastMode = data.mode
    		data.mode = "help"
    	else:
    		data.mode = data.lastMode



def timerFired(data):
    data.countdown -= 1
    if data.countdown == 0:
    	TODO: time is up



def redrawAll(canvas, data):
	if data.mode == "start":
		canvas.create_rectangle(250, 370, 350, 430)
		canvas.create_text(300, 400, text="Play", font="Times 28 bold")
	elif data.mode == "help":
		drawHelpPage(canvas, data)
	elif data.mode == "game":
		drawBoard(canvas, data)
		

def drawHelpPage(canvas, data):
	canvas.create_text(300, 50, text="Help Manual", font="Times 28 bold")

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
