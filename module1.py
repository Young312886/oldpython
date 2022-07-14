import turtle
import random

def function1():
    print('됬다')


def turtle(swidth, sheight):
    turtle_list = []
    a = turtle.getshapes()
    turtle.setup(width = swidth +50, height = sheight +50)
    turtle.screensize(swidth, sheight)

    for i in range(10) :
        k = random.randrange(0,7)
        x= random.randrange(-(swidth/2),(swidth/2),1)
        y = random.randrange(-(swidth/2),(swidth/2),1)
        r,g,b = random.random(),random.random(),random.random()
        turtle_list.append([r,g,b,x,y,a[k]])
        print(turtle_list)

    for j in range(10):
        myTurtle = turtle.Turtle()
        myTurtle.shape(turtle_list[j][5])
        myTurtle.color(turtle_list[j][0],turtle_list[j][1],turtle_list[j][2])
        myTurtle.pencolor(turtle_list[j][0],turtle_list[j][1],turtle_list[j][2])
        myTurtle.goto(turtle_list[j][3],turtle_list[j][4])
    turtle.done()
    return turtle_list