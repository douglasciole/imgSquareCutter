#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# sudo pip install pillow
import time
from PIL import Image
import os


start_time = time.time()
targetFile = "input.png"
outputDir = "./output/"


im = Image.open(targetFile, 'r')
im = im.convert('RGBA')
pix = im.load()  # Gets the color of the parent to be able to identify smaller sprites inside.
parentColor = pix[0, 0]

width, height = im.size

class Coordinate:
    """
    Each coordinate is a square with x, y, width and height to make the cut.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def valid(self, c):
        """
        Verify if the coordinate overlap any of the stored squares.
        :param c: List with two indexes. [x, y]
        :return: False if overlaps. True if valid new Coordinate.
        """
        if self.x <= c[0] and (self.x + self.width) >= c[0] and self.y <= c[1] and (self.y + self.height) >= c[1]:
            return False
        return True

    def echo(self):
        """
        Debug method.
        """
        print(self.x, self.y, self.width, self.height)


class Cutter:
    def __init__(self):
        self.list = []

    def add(self, c):
        self.list.append(c)

    def isValid(self, c):
        for i in self.list:
            if (i.valid(c) == False):
                return False
        return True

    def echo(self):
        """
        Debug method.
        """
        for i in self.list:
            i.echo()

    def cutAllSprities(self):
        """
        Generates all image files with alpha transparency inside the output directory.
        """
        if (os.path.isdir(outputDir) == False):
            os.mkdir(outputDir)

        for i in self.list:
            fImg = im.crop((
                i.x,
                i.y,
                im.size[0] - (im.size[0] - (i.width + i.x)),
                im.size[0] - (im.size[0] - (i.height + i.y))
            ))
            fImg = fImg.convert('RGBA')
            pixdata = fImg.load()
            r, g, b, a = pixdata[0, 0]

            for y in range(fImg.size[1]):
                for x in range(fImg.size[0]):
                    if pixdata[x, y] == (r, g, b, a):
                        pixdata[x, y] = (r, g, b, 0)

            fImg.save(outputDir+str(i.x)+"."+str(i.y)+".png", "PNG")


cutter = Cutter()
counter = 0  # Debug

for h in range(height):
    for w in range(width):

        if pix[w, h] != parentColor and cutter.isValid([w, h]):
            initial_coord_w = w
            wSize = 0
            initial_coord_h = h
            hSize = 0

            wLength = w

            while True:
                wLength += 1
                if pix[wLength, h] == parentColor:
                    wSize = wLength - w - 1

                    hLength = h

                    while True:
                        hLength += 1
                        if pix[w, hLength] == parentColor:
                            hSize = hLength - h - 1
                            break

                    break

            # Add a valid new Coordinate to list of squares to be cutted by the application.
            cutter.add(Coordinate(initial_coord_w, initial_coord_h, wSize, hSize))

            counter += 1  # Debug
            print("add(" + str(counter) + "): ",initial_coord_w, initial_coord_h, wSize, hSize)  # Debug

print("Done!")
cutter.cutAllSprities()  # Runs the cutting process.

# Prints how long it took to execute the whole process.
print("--- %s seconds ---" % (time.time() - start_time))
