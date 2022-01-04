import sys
from PIL import Image, ImageDraw
from numpy import asarray

def addVertical(image, size, pixelPoints):
    lines = []
    pixState =  [[1 for i in range(size[1])] for j in range(size[0])]
    for x in range(size[0]):
        for lineNum in range(pixelPoints):
            actLine = None
            for y in range(size[1]):
                if image.getpixel((x,y)) < 255 - pixState[x][y] * 255/(pixelPoints+1):
                    pixState[x][y]+=1
                    if actLine:
                        actLine[1][1] = (y+1)*pixelPoints
                    else:
                        actLine = [[x*pixelPoints+lineNum, y*pixelPoints],[x*pixelPoints+lineNum, (y+1)*pixelPoints]]
                else:
                    if actLine:
                        lines.append(actLine)
                        actLine = None
            if actLine:
                lines.append(actLine)
    return lines

def addHorizontal(image, size, pixelPoints):
    lines = []
    pixState =  [[1 for i in range(size[1])] for j in range(size[0])]
    for y in range(size[1]):
        for lineNum in range(pixelPoints):
            actLine = None
            for x in range(size[0]):
                if image.getpixel((x,y)) < 255 - pixState[x][y] * 255/(pixelPoints+1) + 255/(pixelPoints+1)/2:
                    pixState[x][y]+=1
                    if actLine:
                        actLine[1][0] = (x+1)*pixelPoints
                    else:
                        actLine = [[x*pixelPoints, y*pixelPoints+lineNum],[(x+1)*pixelPoints, y*pixelPoints+lineNum]]
                else:
                    if actLine:
                        lines.append(actLine)
                        actLine = None
            if actLine:
                lines.append(actLine)
    return lines


#TODO add PROG EVERYWHERE and KOLEJNOŚĆ
def addDiagonal(image, size, pixelPoints, width, height, backSlash=False):
    lines = []
    pixState = [[1 for i in range(size[1])] for j in range(size[0])]
    for line in range((width+height)//2):
        lastPix = None
        actLine = None
        pixs = []

        for x in range(max(line*2-height+1, 0), min(line*2+1, width)):
            y = line*2-x
            if backSlash:
                y = height-1-line*2+x

            actPix = (min(x//pixelPoints, image.size[0]-1), min(y//pixelPoints, image.size[1]-1))

            PROG = 255/(pixelPoints+1)*3/4
            if backSlash:
                PROG = 255/(pixelPoints+1)/4

            if image.getpixel((actPix[0],actPix[1])) < 255 - pixState[actPix[0]][actPix[1]] * 255/(pixelPoints+1) + PROG:
                if actPix != lastPix:
                    if lastPix:
                        pixState[lastPix[0]][lastPix[1]] += 1
                    pixs.append(actPix)

                if actLine:
                    actLine[1] = [x,y]
                else:
                    actLine = [[x,y],[x,y]]
            else:
                if actLine:
                    lines.append(actLine)
                    actLine = None
            
            lastPix = actPix
        if lastPix:
            pixState[lastPix[0]][lastPix[1]] += 1
        if actLine:
            lines.append(actLine)
    return lines

def convertImgToLines(filename, width=590, height=840, pixelPoints=5, rotate=False):
    org_image = Image.open(filename).convert('L')
    if rotate:
        org_image = org_image.rotate(90, expand=True)
    size = (width//pixelPoints, height//pixelPoints)
    org_image.thumbnail(size, Image.ANTIALIAS) #resize


    image = Image.new(org_image.mode, size, (100))
    image.paste(org_image, ((size[0]-org_image.size[0])//2, (size[1]-org_image.size[1])//2))

    lines = []

    #vertical lines
    lines.extend(addVertical(image, size, pixelPoints))

    #horizontal lines
    lines.extend(addHorizontal(image,size,pixelPoints))

    #diagonal TL-BR
    lines.extend(addDiagonal(image, size, pixelPoints, width, height))

    #diagonal TR-BL
    lines.extend(addDiagonal(image,size,pixelPoints, width, height, backSlash=True))

    return lines
