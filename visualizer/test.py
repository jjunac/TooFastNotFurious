import random
import time
import turtle

screen = turtle.Screen()

turtlepower = []

turtle.tracer(0, 0)
image = "../resources/testRoad.png"
screen.addshape(image)
for i in range(1000):
    t = turtle.Turtle()
    t.shape(image)
    t.goto(random.random() * 500, random.random() * 1000)
    turtlepower.append(t)

for i in range(1000):
    turtle.stamp()

turtle.update()

time.sleep(3)
