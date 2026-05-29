import turtle

class Entity:
    def __init__(self, col, row, color, shape="circle"):
        self.col = col
        self.row = row

        self.t = turtle.Turtle()
        self.t.shape(shape)
        self.t.color(color)
        self.t.penup()
        self.t.shapesize(0.7)
        self.t.speed(0)

    @property
    def pos(self):
        return self.col, self.row

    def teleport(self, maze):
        x, y = maze.cell(self.col, self.row).center()
        self.t.goto(x, y)