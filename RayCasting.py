import pygame as pg
from math import *

# initialization
pg.init()
s = pg.display.set_mode((500,500))
#checking if right mouse button is held - used to create rectangles
right_held = False

# Vector class
class Vector:
    def __init__(self, origin, magnitude, angle):
        # Angle of the vector in radians
        self.angle = angle / 360 * pi * 2
        self.magnitude = magnitude
        # (x,y) of the end point of the vector
        x = int(magnitude * cos(self.angle)) + origin[0]
        y = int(magnitude * sin(self.angle)) + origin[1]
        self.origin = origin
        # end point of vector
        self.comps = (x,y)
        # checking if the vector is parallel to the y axis so there isn't division by 0
        if self.origin[0] == self.comps[0]:
            self.slope = inf
        else:
            # calculating the slope of the line
            self.slope = (self.comps[1]-self.origin[1]) / (self.comps[0]-self.origin[0])
        # offset of the line relative to the y axis
        self.offset = self.origin[1] - self.origin[0] * self.slope
    
    # passing through points of the line to check if it collides with any rectangle
    def check_collide(self, obsts):
        # if the line is parallel to the y axis it passes through rectangles
        # so instead of going through the points with the x coordinate it uses the y coordinate
        if self.slope == inf:
            for y in range(self.origin[1], self.comps[1], 1 if self.comps[1] >= self.origin[0] else -1):
                point = (self.origin[0], y)
                if pg.Rect(point, (0, 0)).collidelist(obsts) > -1:
                    self.comps = point
                    return point
        # checking collisions of lines that are close to being parallel to the y axis to avoid leaking through rectangles
        elif abs(self.slope) > 3:
            for y in range(self.origin[1], self.comps[1], 1 if self.comps[1] >= self.origin[0] else -1):
                point = (((y-self.offset)/self.slope), y)
                if pg.Rect(point, (0, 0)).collidelist(obsts) > -1:
                    self.comps = point
                    return point
        # for all other lines: going through all x coordinates from the origin to the
        # end point and calculating the point for each one to check for collisions
        else:
            for x in range(self.origin[0], self.comps[0], 1 if self.comps[0] >= self.origin[0] else -1):
                point = (x, self.slope*x+self.offset)
                if pg.Rect(point, (0,0)).collidelist(obsts) > -1:
                    self.comps = point
                    return point

    def display(self, screen, color):
        pg.draw.line(screen, color, self.origin, self.comps)

obsts = []

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    s.fill(0)

    mouse = pg.mouse.get_pressed()
    if mouse[0]:
        m_pos = pg.mouse.get_pos()
        for i in range(360):
            # if (i < -135 and i > 135) or (i > -45 and i < 45):
            #     v = Vector(m_pos, 750, i, True)
            # else:
            v = Vector(m_pos, sqrt(s.get_height()**2 + s.get_width()**2), i)
            v.check_collide(obsts)
            v.display(s, (255,255,255))
    if mouse[2] and not right_held:
        right_held = True
        new_rect = pg.Rect(pg.mouse.get_pos(), (0,0))
    elif mouse[2] and right_held:
        new_rect.width = pg.mouse.get_pos()[0] - new_rect.x
        new_rect.height = pg.mouse.get_pos()[1] - new_rect.y
        pg.draw.rect(s, (255,0,0), new_rect)
    elif not mouse[2] and right_held:
        right_held = False
        if new_rect.width < 0:
            new_rect.x = new_rect.x + new_rect.width
            new_rect.width = abs(new_rect.width)
        if new_rect.height < 0:
            new_rect.y = new_rect.y + new_rect.height
            new_rect.height = abs(new_rect.height)
        obsts.append(new_rect)

    if mouse[1]:
        for r in obsts:
            if r.collidepoint(pg.mouse.get_pos()):
                obsts.remove(r)

    if not mouse[0]:
        for r in obsts:
            pg.draw.rect(s, (255, 0, 0), r)

    pg.display.flip()
