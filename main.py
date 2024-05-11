import tkinter as tk
from Risk import Generation
from Risk import neighbors
from Risk import finalGen
# generates a board form the risk.py
n = 200
board = finalGen(n)
root = tk.Tk()
root.title("risk")

# this set the size of the square make it what ever
square_size = 5

# random tk stuff (did not steal from there webstie)
canvas = tk.Canvas(root, width=len(board[0])*square_size, height=len(board)*square_size)
canvas.pack()

# goes through the board
for y, row in enumerate(board):
    for x, value in enumerate(row):
        if value == " ":
            if neighbors(board,"water",x,y,n) == 1:
                if y > (n*3//5)*(1/4) and y < (n*3//5)*(3/4):
                    color = "#F6F693"
                else:
                    color = "#414040"
            elif neighbors(board,"water",x,y,n) == 2 or neighbors(board,"water",x,y,n) == 3:
                color = "#0e80c7"
            else:
                color = "#003186"
        elif value == '#':
            color = '#013220'
        elif value == '!' or value == '!!':
            color = '#FFFFFF'
        elif value == 'I':
            color = '#7390B5'
        elif value == '&':
            color = '#C2823A'
        elif value == '@':
            color = '#e3e100'
        elif value == '0' or value == '%':
            color = '#027D00'
        canvas.create_rectangle(x*square_size, y*square_size, (x+1)*square_size, (y+1)*square_size, fill=color)

root.mainloop()
