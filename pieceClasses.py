
######## This file contains the classes of all key components of the chess board
######## including all the building blocks of the board and all types of game pieces

# This dictionary maps the coordinate of a post to its x and y location on canvas
getCoord = {}
for x in range(5):
    for y in range(12):
            if y < 6:
                getCoord[(y, x)] = (50 + 125 * x, 50 + 60 * y)
            else:
                getCoord[(y, x)] = (50 + 125 * x, 450 + 60 * (y - 6))

# This is a reversed dictionary for multiplayer viewing (for PlayerA)
getReversedCoord = {}
for x in range(5):
    for y in range(12):
            if y < 6:
                getReversedCoord[(11-y, 4-x)] = (50 + 125 * x, 50 + 60 * y)
            else:
                getReversedCoord[(11-y, 4-x)] = (50 + 125 * x, 450 + 60 * (y - 6))

# get the coordinate of a post given its location on canvas
def getLocation(x, y):
    for (i, j) in getCoord:
        (a, b) = getCoord[(i, j)]
        if a - 25 < x < a + 25 and b - 12 < y < b + 12:
            return (i, j)


class Post():
    def __init__(self, x, y, piece=None):  # x, y are center coordinates
        self.x, self.y = getCoord[(x, y)]
        self.reversedX, self.reversedY = getReversedCoord[(x, y)]
        self.w = 25
        self.h = 12
        self.piece = piece
        self.selected = False
        self.highlighted = False

    def select(self):
        self.selected = not self.selected

    def highlight(self):
        self.highlighted = not self.highlighted

    # drawing the Post with the piece
    def draw(self, canvas): 
        self.drawSkeleton(canvas)
        if self.piece != None:
            if self.highlighted or self.selected:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color, width=0)
            else:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color)
            canvas.create_text(self.x, self.y, text=self.piece.name)

    # drawing the Post and the piece in Dark Mode
    def drawDark(self, canvas):
        self.drawSkeleton(canvas)
        if self.piece != None:
            if self.highlighted or self.selected:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color, width=0)
            else:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color)

    # drawing the Post without the piece
    def drawSkeleton(self, canvas):
        if self.highlighted:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="PaleGreen3", outline="lawn green", width=4)
        elif self.selected:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="PaleGreen3", outline="red3", width=4)
        else:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill="PaleGreen3")
    
    # drawing the Post with the piece in reversed position 
    def reversedDraw(self, canvas):
        self.reversedDrawSkeleton(canvas)
        if self.piece != None:
            if self.highlighted or self.selected:
                canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                        self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color, width=0)
            else:
                canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                        self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color)
            canvas.create_text(self.reversedX, self.reversedY, text=self.piece.name)

    # drawing the Post and the piece in reversed position in Dark Mode
    def reversedDrawDark(self, canvas):
        self.reversedDrawSkeleton(canvas)
        if self.piece != None:
            if self.highlighted or self.selected:
                canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                        self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color, width=0)
            else:
                canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                        self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color)

    # drawing the Post without the piece in reversed position
    def reversedDrawSkeleton(self, canvas):
        if self.highlighted:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h, self.reversedX +
                                    self.w, self.reversedY + self.h, fill="PaleGreen3", outline="lawn green", width=4)
        elif self.selected:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h, self.reversedX +
                                    self.w, self.reversedY + self.h, fill="PaleGreen3", outline="red3", width=4)
        else:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                    self.reversedX + self.w, self.reversedY + self.h, fill="PaleGreen3")



class Camp(Post):
    # Camps inherit the __init__ function from Post, and the drawing functions behave similarly
    def draw(self, canvas):
        self.drawSkeleton(canvas)
        if self.piece != None:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill=self.piece.color)
            canvas.create_text(self.x, self.y, text=self.piece.name)

    def drawDark(self, canvas):
        self.drawSkeleton(canvas)
        if self.piece != None:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill=self.piece.color)

    def drawSkeleton(self, canvas):
        if self.highlighted:
            canvas.create_oval(self.x - self.w, self.y - self.w + 7, self.x +
                               self.w, self.y + self.w - 7, outline="lawn green", fill="PaleGreen3", width=3)
        elif self.selected:
            canvas.create_oval(self.x - self.w, self.y - self.w + 7, self.x +
                               self.w, self.y + self.w - 7, outline="red3", fill="PaleGreen3", width=3)
        else:
            canvas.create_oval(self.x - self.w, self.y - self.w + 7,
                               self.x + self.w, self.y + self.w - 7, fill="PaleGreen3")

    def reversedDraw(self, canvas):
        self.reversedDrawSkeleton(canvas)
        if self.piece != None:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                    self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color)
            canvas.create_text(self.reversedX, self.reversedY, text=self.piece.name)

    def reversedDrawDark(self, canvas):
        self.reversedDrawSkeleton(canvas)
        if self.piece != None:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                    self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color)

    def reversedDrawSkeleton(self, canvas):
        if self.highlighted:
            canvas.create_oval(self.reversedX - self.w, self.reversedY - self.w + 7, self.reversedX +
                               self.w, self.reversedY + self.w - 7, outline="lawn green", fill="PaleGreen3", width=3)
        elif self.selected:
            canvas.create_oval(self.reversedX - self.w, self.reversedY - self.w + 7, self.reversedX +
                               self.w, self.reversedY + self.w - 7, outline="red3", fill="PaleGreen3", width=3)
        else:
            canvas.create_oval(self.reversedX - self.w, self.reversedY - self.w + 7,
                               self.reversedX + self.w, self.reversedY + self.w - 7, fill="PaleGreen3")

class Headquarters(Post):
    # Headquarters inherit the __init__ function from Post, and the drawing functions behave similarly
    def draw(self, canvas):
        self.drawSkeleton(canvas)
        if self.piece != None:
            if self.highlighted or self.selected:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color, width=0)
            else:
                canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                        self.x + self.w, self.y + self.h, fill=self.piece.color)
            canvas.create_text(self.x, self.y, text=self.piece.name)

    def drawSkeleton(self, canvas):
        canvas.create_oval(self.x - self.w / 2, self.y - 2 * self.h,
                           self.x + self.w / 2, self.y, fill="black")
        canvas.create_oval(self.x - self.w / 2, self.y, self.x +
                           self.w / 2, self.y + 2 * self.h, fill="black")
        if self.highlighted:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="PaleGreen3", outline="lawn green", width=3)
        elif self.selected:
            canvas.create_rectangle(self.x - self.w, self.y - self.h, self.x +
                                    self.w, self.y + self.h, fill="PaleGreen3", outline="red3", width=3)
        else:
            canvas.create_rectangle(self.x - self.w, self.y - self.h,
                                    self.x + self.w, self.y + self.h, fill="PaleGreen3")

    def reversedDraw(self, canvas):
        self.reversedDrawSkeleton(canvas)
        if self.piece != None:
            if self.highlighted or self.selected:
                canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                        self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color, width=0)
            else:
                canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                        self.reversedX + self.w, self.reversedY + self.h, fill=self.piece.color)
            canvas.create_text(self.reversedX, self.reversedY, text=self.piece.name)

    def reversedDrawSkeleton(self, canvas):
        canvas.create_oval(self.reversedX - self.w / 2, self.reversedY - 2 * self.h,
                           self.reversedX + self.w / 2, self.reversedY, fill="black")
        canvas.create_oval(self.reversedX - self.w / 2, self.reversedY, self.reversedX +
                           self.w / 2, self.reversedY + 2 * self.h, fill="black")
        if self.highlighted:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h, self.reversedX +
                                    self.w, self.reversedY + self.h, fill="PaleGreen3", outline="lawn green", width=3)
        elif self.selected:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h, self.reversedX +
                                    self.w, self.reversedY + self.h, fill="PaleGreen3", outline="red3", width=3)
        else:
            canvas.create_rectangle(self.reversedX - self.w, self.reversedY - self.h,
                                    self.reversedX + self.w, self.reversedY + self.h, fill="PaleGreen3")


#### classes of different pieces

class Mar():
    def __init__(self, side):
        self.order = 9
        self.value = 50
        self.name = "Mar10"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Gen():
    def __init__(self, side):
        self.order = 8
        self.value = 40
        self.name = "Gen9"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class MGen():
    def __init__(self, side):
        self.order = 7
        self.value = 25
        self.name = "MGen8"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class BGen():
    def __init__(self, side):
        self.order = 6
        self.value = 15
        self.name = "BGen7"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Col():
    def __init__(self, side):
        self.order = 5
        self.value = 8
        self.name = "Col6"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Maj():
    def __init__(self, side):
        self.order = 4
        self.value = 5
        self.name = "Maj5"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Capt():
    def __init__(self, side):
        self.order = 3
        self.value = 2
        self.name = "Capt4"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Lt():
    def __init__(self, side):
        self.order = 2
        self.value = 1
        self.name = "Lt3"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Spr():
    def __init__(self, side):
        self.order = 1
        self.value = 10
        self.name = "Spr2"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Bomb():
    # Bombs do not have fixed values
    # their values are calculated as 1/3 of the opponent's most valuable piece (excluding the Flag)
    def __init__(self, side):
        self.order = None
        self.name = "Bomb"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class LMN():
    def __init__(self, side):
        self.order = 10
        self.value = 70
        self.name = "LMN"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"

class Flag():
    def __init__(self, side):
        self.order = 0
        self.value = 2000
        self.name = "Flag1"
        self.side = side
        if self.side == "A":
            self.color = "orange"
        elif self.side == "B":
            self.color = "deep sky blue"








