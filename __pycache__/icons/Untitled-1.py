from turtle import *
import colorsys

pensize(2)
speed(0)
bgcolor("white")
h = 0
for i in range(15):
    for j in range(18):
        c = colorsys.hsv_to_rgb(h, 1, 1)
        color(c)
        h += 0.0037
        rt(90)
        circle(150 - j*6, 90)
        lt(90)
        circle(150 - j*6, 90)
        rt(180)
    circle(40, 24)
done()