from PIL import Image, ImageDraw
# Import the pygame library and initialise the game engine
import pygame
pygame.init()

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def lerp(a : Vec2, b : Vec2, t):
    return Vec2(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t)
    
class Point:
    def __init__(self, pos : Vec2, active):
        self.pos = pos
        self.active = active

class Square:
    def __init__(self, points, value = 0, M = 0.5, N = 0.5, O = 0.5, P = 0.5):
        self.points = points
        self.value = value
        self.M = lerp(points[0].pos, points[1].pos, M)
        self.N = lerp(points[1].pos, points[2].pos, N)
        self.O = lerp(points[2].pos, points[3].pos, O)
        self.P = lerp(points[3].pos, points[0].pos, P)
        
class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

''' Config '''
size = (400, 400)   #size of the image
resolution = 35     #the resolution of the metaballs
circles = [Circle(Vec2(70, 150), 50),
           Circle(Vec2(160, 150), 30),
           Circle(Vec2(155, 225), 20),
           Circle(Vec2(60, 60), 20),
           Circle(Vec2(120, 50), 20)]        #the array of circles
renderPoints = False
renderGrid = False
renderCircles = False
metaColor = (220, 220, 220)
thickness = 1
''' Config '''

img = Image.new('RGB', size, color = (2, 2, 2))
d = ImageDraw.Draw(img)

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 220, 220, 220)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

# Open a new window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Metablob")

def getPointIndex(index : Vec2):
    return index.y * (resolution + 1) + index.x

def renderPoint(point : Point):
    outlineColor = (150, 150, 150) if (point.active == False or point.active < 1) else (0, 250, 0)
    fillColor = (100, 100, 100) if (point.active == False or point.active < 1) else (0, 200, 0)
    d.ellipse([point.pos.x - 2, point.pos.y - 2, point.pos.x + 2, point.pos.y + 2], fillColor)
    d.line([point.pos.x - 2, point.pos.y - 1, point.pos.x - 2, point.pos.y + 1], outlineColor)
    d.line([point.pos.x - 1, point.pos.y - 2, point.pos.x + 1, point.pos.y - 2], outlineColor)
    d.line([point.pos.x + 2, point.pos.y - 1, point.pos.x + 2, point.pos.y + 1], outlineColor)
    d.line([point.pos.x - 1, point.pos.y + 2, point.pos.x + 1, point.pos.y + 2], outlineColor)
    
def renderSquare(square : Square):
    if renderGrid:
        d.polygon([square.points[0].pos.x, square.points[0].pos.y,
                   square.points[1].pos.x, square.points[1].pos.y,
                   square.points[2].pos.x, square.points[2].pos.y,
                   square.points[3].pos.x, square.points[3].pos.y],
                   None, (80, 80, 100))
    if (square.points[0].active < 1 and square.points[1].active < 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        d.line([square.O.x, square.O.y, square.P.x, square.P.y], metaColor)
    elif (square.points[0].active < 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        d.line([square.N.x, square.N.y, square.O.x, square.O.y], metaColor)
    elif (square.points[0].active < 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active >= 1):
        d.line([square.P.x, square.P.y, square.N.x, square.N.y], metaColor)
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active < 1):
        d.line([square.M.x, square.M.y, square.N.x, square.N.y], metaColor)
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        d.line([square.P.x, square.P.y, square.M.x, square.M.y], metaColor)
        d.line([square.O.x, square.O.y, square.N.x, square.N.y], metaColor)
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        d.line([square.M.x, square.M.y, square.O.x, square.O.y], metaColor)
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active >= 1 and square.points[3].active >= 1):
        d.line([square.P.x, square.P.y, square.M.x, square.M.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active < 1 and square.points[3].active < 1):
        d.line([square.P.x, square.P.y, square.M.x, square.M.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        d.line([square.M.x, square.M.y, square.O.x, square.O.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        d.line([square.M.x, square.M.y, square.N.x, square.N.y], metaColor)
        d.line([square.P.x, square.P.y, square.O.x, square.O.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active >= 1):
        d.line([square.M.x, square.M.y, square.N.x, square.N.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active < 1):
        d.line([square.P.x, square.P.y, square.N.x, square.N.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        d.line([square.O.x, square.O.y, square.N.x, square.N.y], metaColor)
    elif (square.points[0].active >= 1 and square.points[1].active >= 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        d.line([square.P.x, square.P.y, square.O.x, square.O.y], metaColor)
               
def renderCircle(circle : Circle):
    if renderCircles:
        d.ellipse([circle.pos.x - circle.radius, circle.pos.y - circle.radius,
                   circle.pos.x + circle.radius, circle.pos.y + circle.radius],
                   None, (0, 150, 0))
    
def drawPoint(point : Point):
    outlineColor = (150, 150, 150) if (point.active == False or point.active < 1) else (0, 250, 0)
    fillColor = (100, 100, 100) if (point.active == False or point.active < 1) else (0, 200, 0)
    pygame.draw.line(screen, outlineColor, [point.pos.x - 2, point.pos.y - 1], [point.pos.x - 2, point.pos.y + 1])
    pygame.draw.line(screen, outlineColor, [point.pos.x - 1, point.pos.y - 2], [point.pos.x + 1, point.pos.y - 2])
    pygame.draw.line(screen, outlineColor, [point.pos.x + 2, point.pos.y - 1], [point.pos.x + 2, point.pos.y + 1])
    pygame.draw.line(screen, outlineColor, [point.pos.x - 1, point.pos.y + 2], [point.pos.x + 1, point.pos.y + 2])
    
def drawSquare(square : Square):
    if renderGrid:
        pygame.draw.polygon(screen, (80, 80, 100),
                            [(square.points[0].pos.x, square.points[0].pos.y),
                             (square.points[1].pos.x, square.points[1].pos.y),
                             (square.points[2].pos.x, square.points[2].pos.y),
                             (square.points[3].pos.x, square.points[3].pos.y)], 1)
                             
    if (square.points[0].active < 1 and square.points[1].active < 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.O.x, square.O.y], [square.P.x, square.P.y])
    elif (square.points[0].active < 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.N.x, square.N.y], [square.O.x, square.O.y])
    elif (square.points[0].active < 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.N.x, square.N.y])
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.M.x, square.M.y], [square.N.x, square.N.y])
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.M.x, square.M.y])
        pygame.draw.line(screen, metaColor, [square.O.x, square.O.y], [square.N.x, square.N.y])
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.M.x, square.M.y], [square.O.x, square.O.y])
    elif (square.points[0].active < 1 and square.points[1].active >= 1 and square.points[2].active >= 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.M.x, square.M.y])
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active < 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.M.x, square.M.y])
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.M.x, square.M.y], [square.O.x, square.O.y])
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.M.x, square.M.y], [square.N.x, square.N.y])
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.O.x, square.O.y])
    elif (square.points[0].active >= 1 and square.points[1].active < 1 and square.points[2].active >= 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.M.x, square.M.y], [square.N.x, square.N.y])
    elif (square.points[0].active >= 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.N.x, square.N.y])
    elif (square.points[0].active >= 1 and square.points[1].active >= 1 and square.points[2].active < 1 and square.points[3].active >= 1):
        pygame.draw.line(screen, metaColor, [square.O.x, square.O.y], [square.N.x, square.N.y])
    elif (square.points[0].active >= 1 and square.points[1].active >= 1 and square.points[2].active >= 1 and square.points[3].active < 1):
        pygame.draw.line(screen, metaColor, [square.P.x, square.P.y], [square.O.x, square.O.y])
               
def drawCircle(circle : Circle):
    if renderCircles:
        pygame.draw.circle(screen, (0, 150, 0), [circle.pos.x, circle.pos.y], circle.radius, 1 if circle.radius > 1 else 0)

def pointFunc(point, circle):
    dist = ((point.pos.x - circle.pos.x)**2 + (point.pos.y - circle.pos.y)**2)
    return (circle.radius**2) / dist if dist != 0 else ((circle.radius**2) * 2)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
mousePressed = False
creatingCircle = False

circlesInitialPositions = []
pressedCircles = []
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
 
    smoothness = 0.4
    # --- Game logic should go here
    mousePos = pygame.mouse.get_pos()
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousePressed = True
                for circle in circles:
                    if ((mousePos[0] - circle.pos.x)**2 + (mousePos[1] - circle.pos.y)**2) <= circle.radius**2:
                        pressedCircles.append(circles.index(circle))
                        circlesInitialPositions.append(circle.pos)
            mouseInitialPosition = mousePos
            if event.button == 3:
                if mousePressed:
                    for i in pressedCircles:
                        circles.remove(circles[i])
                        mousePressed = False
                else:
                    creatingCircle = True
                    newCircleIndex = len(circles)
                    circles.append(Circle(Vec2(mouseInitialPosition[0]-10, mouseInitialPosition[1]), 5))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mousePressed = False
                circlesInitialPositions = []
                pressedCircles = []
            if event.button == 3:
                creatingCircle = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                d.rectangle((0, 0, size[0], size[1]), (2, 2, 2))
                
                for square in squares:
                    renderSquare(square)
                    
                if renderPoints:
                    for point in points:
                        renderPoint(point)
                    
                for circle in circles:
                    renderCircle(circle)
                img.save("metaball.png")
            if event.key == pygame.K_g:
                renderGrid = not renderGrid
            if event.key == pygame.K_c:
                renderCircles = not renderCircles
            if event.key == pygame.K_p:
                renderPoints = not renderPoints
            if event.key == pygame.K_UP:
                resolution += 1
            if event.key == pygame.K_DOWN:
                resolution -= 1
            if event.key == pygame.K_LEFT:
                thickness -= 0.05
            if event.key == pygame.K_RIGHT:
                thickness += 0.05
    if mousePressed:
        for i in pressedCircles:
            circles[i].pos = Vec2(int(circles[i].pos.x + (circlesInitialPositions[pressedCircles.index(i)].x + mousePos[0] -  mouseInitialPosition[0] - circles[i].pos.x) * smoothness),
                                  int(circles[i].pos.y + (circlesInitialPositions[pressedCircles.index(i)].y + mousePos[1] -  mouseInitialPosition[1] - circles[i].pos.y) * smoothness))
    if creatingCircle:
        circles[newCircleIndex].radius = int(((((mouseInitialPosition[0]-10) - mousePos[0])**2 + (mouseInitialPosition[1] - mousePos[1])**2))**0.5)
    
    points = []
    squares = []
    for y in range(resolution + 1):
        for x in range(resolution + 1):
            point = Point(Vec2((size[0] / resolution) * x, (size[1] / resolution) * y), 0)
            points.append(point)
            
    for y in range(resolution):
        for x in range(resolution):
            square = Square([points[getPointIndex(Vec2(x, y))],
                             points[getPointIndex(Vec2(x + 1, y))],
                             points[getPointIndex(Vec2(x + 1, y + 1))],
                             points[getPointIndex(Vec2(x, y + 1))]])
            squares.append(square)
            
    for point in points:
        point.active = 0
        for circle in circles:
            point.active += pointFunc(point, circle)
        point.active *= thickness
            
    for square in squares:
        mxdiff = (square.points[1].active - square.points[0].active)
        nydiff = (square.points[2].active - square.points[1].active)
        oxdiff = (square.points[3].active - square.points[2].active)
        pydiff = (square.points[0].active - square.points[3].active)
        mx = square.points[0].pos.x + (square.points[1].pos.x - square.points[0].pos.x) * ((1 - square.points[0].active) / (mxdiff if mxdiff != 0 else 0.001))
        ny = square.points[1].pos.y + (square.points[2].pos.y - square.points[1].pos.y) * ((1 - square.points[1].active) / (nydiff if nydiff != 0 else 0.001))
        ox = square.points[2].pos.x + (square.points[3].pos.x - square.points[2].pos.x) * ((1 - square.points[2].active) / (oxdiff if oxdiff != 0 else 0.001))
        py = square.points[3].pos.y + (square.points[0].pos.y - square.points[3].pos.y) * ((1 - square.points[3].active) / (pydiff if pydiff != 0 else 0.001))
        square.M = Vec2(mx, square.M.y)
        square.N = Vec2(square.N.x, ny)
        square.O = Vec2(ox, square.O.y)
        square.P = Vec2(square.P.x, py)
    # --- Drawing code should go here
    screen.fill(BLACK)
            
    for square in squares:
        drawSquare(square)
        
    if renderPoints:
        for point in points:
            drawPoint(point)
        
    for circle in circles:
        drawCircle(circle)
 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()