from tkinter import *
import random
from PIL import ImageTk, Image

####################################
# customize these functions
####################################

def init(data): # initializes splash screen
    data.mode = "splash"
    data.difficulty = "Easy"
    #initialize background image(s)
    initImages(data)
    data.textSize = 40
    data.count = 0
    # create buttons — code adapted from button-demo3
    # http://www.cs.cmu.edu/~112/notes/notes-tkinter-demos.html
    #appear third down page
    data.buttonFrame = Frame(data.root, pady=data.height/3, bg="white")
    buttonFrame = data.buttonFrame
    buttonImage = PhotoImage(file="titlebutton.gif")
    data.btitle = Button(buttonFrame, image=buttonImage, width=400, height=50,
    bg="black")
    data.btitle.image = buttonImage # save img from garbage collector (needed!)
    data.btitle.grid(row=0, column=1)
    buttonImage = PhotoImage(file="button.gif")
    data.b1 = Button(buttonFrame, image=buttonImage, width=200, height=50,
                bg="black", command=lambda:onButton(data,1))
    data.b1.image = buttonImage # save image from garbage collector (needed!)
    data.b1.grid(row=3,column=1)
    buttonImage = PhotoImage(file="button2.gif")
    data.b2 = Button(buttonFrame, image=buttonImage, width=200, height=50,
                bg="black", command=lambda:onButton(data,2))
    data.b2.image = buttonImage # save image from garbage collector (needed!)
    data.b2.grid(row=4,column=1)
    
    buttonImage = PhotoImage(file="button3.gif")
    data.b3 = Button(buttonFrame, image=buttonImage, width=200, height=50,
                bg="black", command=lambda:onButton(data,3))
    data.b3.image = buttonImage # save image from garbage collector (needed!)
    data.b3.grid(row=5,column=1)
    data.buttonFrame.lower()
    data.buttonFrame.pack()
    
def initImages(data):
    #partially adapted from https://abhgog.gitbooks.io/pil/content/
    #image from https://s-media-cache-ak0.pinimg.com/originals/a6/bf/1c/a6bf1ca75ad990e12c886616b5adfa02.gif
    bg = Image.open("background.gif")
    data.bg_tk = ImageTk.PhotoImage(bg)
    animatedbg1 = Image.open("animated.gif")
    animatedbg2 = Image.open("animated2.gif")
    animatedbg3 = Image.open("animated3.gif")
    animatedbg4 = Image.open("animated4.gif")
    animatedbg1_tk = ImageTk.PhotoImage(animatedbg1)
    animatedbg2_tk = ImageTk.PhotoImage(animatedbg1)
    animatedbg3_tk = ImageTk.PhotoImage(animatedbg2)
    animatedbg4_tk = ImageTk.PhotoImage(animatedbg2)
    animatedbg5_tk = ImageTk.PhotoImage(animatedbg3)
    animatedbg6_tk = ImageTk.PhotoImage(animatedbg3)
    animatedbg7_tk = ImageTk.PhotoImage(animatedbg4)
    animatedbg8_tk = ImageTk.PhotoImage(animatedbg4)
    data.animated = [animatedbg1_tk, animatedbg2_tk, animatedbg3_tk,
    animatedbg4_tk, animatedbg5_tk, animatedbg6_tk,
    animatedbg7_tk, animatedbg8_tk]
    title = Image.open("titlebutton.gif")
    data.title_tk = ImageTk.PhotoImage(title)

def initGame(data):
    # some code adapted from events-example3.py
    # http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-animations.html
    data.mode = "game"
    # #initialize background image
    # bg = Image.open("background.gif")
    # data.bg_tk = ImageTk.PhotoImage(bg)
    data.enemies = [ ]
    data.obstacles = [ ]
    data.obstacleSizes = [20, 40, 60]
    data.squareLeft = data.width/2
    data.squareTop = data.height-50
    data.squareFill = "red"
    data.squareSize = 25
    data.circleCenters = [ ]
    data.laserCenters = [ ]
    data.numLasers = len(data.laserCenters)
    data.laserLength = 10
    data.laserDirections = [ ]
    data.headingRight = True
    data.headingDown = True
    data.isPaused = False
    data.timerDelay = 50
    if data.difficulty == "Easy":
        data.moveSpeedCircle = -1
        data.moveSpeed = 10
        data.laserSpeed = 5
        data.obstaclesLeft = 3 #also a way to check if game has started
        data.maxEnemies = 3
    elif data.difficulty == "Hard":
        data.moveSpeedCircle = +1
        data.moveSpeed = 10
        data.laserSpeed = 5
        data.obstaclesLeft = 2 #also a way to check if game has started
        data.maxEnemies = 4
    data.score = 0
    data.direction = "up"
    data.powerups = ["moveThroughObstacles", "obstaclePiercingLaser",
    "increaseSpeed", "decoy"]
    data.oldPowerupName = random.choice(data.powerups) #choose which powerup
    data.powerupName = ""
    spawnPowerup(data)
    
def initHelp(data):
    # some code adapted from events-example3.py
    # http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-animations.html
    data.mode = "help"
    data.textMax = False
    
def initSettings(data):
    data.mode = "settings"
    data.textMax = False
    
class Enemy(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius, 
                                self.x + self.radius, self.y + self.radius, 
                                    fill = self.color)
    
    def move(self, data):
        if data.powerupName != "decoy":
            if self.y <= (data.squareTop): #enemy above user
                self.y += (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.y -= (self.moveSpeed+data.moveSpeedCircle)
            if self.y >= (data.squareTop+data.squareSize): #enemy below user
                self.y -= (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.y += (self.moveSpeed+data.moveSpeedCircle)
            if self.x <= (data.squareLeft): #enemy left of user
                self.x += (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.x -= (self.moveSpeed+data.moveSpeedCircle)
            if self.x >= (data.squareLeft+data.squareSize): #enemy right of user
                self.x -= (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.x += (self.moveSpeed+data.moveSpeedCircle)
        
        else: #if there is a decoy, they go after it instead
            if self.y <= (data.decoyY): #enemy above user
                self.y += (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.y -= (self.moveSpeed+data.moveSpeedCircle)
            if self.y >= (data.decoyY): #enemy below user
                self.y -= (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.y += (self.moveSpeed+data.moveSpeedCircle)
            if self.x <= (data.decoyX): #enemy left of user
                self.x += (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.x -= (self.moveSpeed+data.moveSpeedCircle)
            if self.x >= (data.decoyX): #enemy right of user
                self.x -= (self.moveSpeed+data.moveSpeedCircle)
                #check legality, then undo if illegal
                if checkEnemyCoordsForMove(data, self.x, self.y,
                self.radius) == False:
                    self.x += (self.moveSpeed+data.moveSpeedCircle)

class smallCircle(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 13
        self.moveSpeed = 4
        self.color = "cyan"
        self.health = 1
        
class bigCircle(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 17
        self.moveSpeed = 3
        self.color = "blue"
        self.health = 2
        
class biggerCircle(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.moveSpeed = 3
        self.color = "purple"
        self.health = 3
        
class Obstacle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        sizes = [20, 30, 50]
        self.size = random.choice(sizes)
    
    def draw(self, canvas):
        x0 = (self.x-(self.size/2))
        x1 = (self.x+(self.size/2))
        y0 = (self.y-(self.size/2))
        y1 = (self.y+(self.size/2))
        canvas.create_rectangle(x0, y0, x1, y1, fill="gray")

class powerup(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sideLength = 5
        self.color = "yellow"
    
    def draw(self, canvas):
        x0 = self.x - self.sideLength
        y0 = self.y - self.sideLength
        x1 = self.x + self.sideLength
        y1 = self.y + self.sideLength
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

def mousePressed(event, data):
    if data.mode == "game":
        obstacleX = event.x
        obstacleY = event.y
        if checkObstacleCoords(data, obstacleX, obstacleY) == True and (
        data.obstaclesLeft > 0):
            data.obstacles.append(Obstacle(obstacleX, obstacleY))
            data.obstaclesLeft -= 1

def spawnEnemies(data):
    margin = max(data.obstacleSizes)
    tempX = random.randint(margin, data.width-margin)
    tempY = random.randint(margin, data.height-margin)
    (enemyX, enemyY) = checkEnemyCoords(data, tempX, tempY)
    x = random.randint(0,9) #just to choose which type of enemy to spawn
    if x <= 5:
        data.enemies.append(smallCircle(enemyX, enemyY)) # 60% chance
    elif x > 5 and x <= 8:
        data.enemies.append(bigCircle(enemyX, enemyY)) # 30% chance
    elif x == 9:
        data.enemies.append(biggerCircle(enemyX, enemyY)) # 10% chance
    
def spawnPowerup(data):
    margin = max(data.obstacleSizes)
    tempX = random.randint(margin, data.width-margin)
    tempY = random.randint(margin, data.height-margin)
    (powerupX, powerupY) = checkEnemyCoords(data, tempX, tempY)
    data.powerup = powerup(powerupX, powerupY)
    
def spawnDecoy(data):
    margin = max(data.obstacleSizes)
    tempX = random.randint(margin, data.width-margin)
    tempY = random.randint(margin, data.height-margin)
    (data.decoyX, data.decoyY) = checkEnemyCoords(data, tempX, tempY)
    
def checkEnemyCoords(data, enemyX, enemyY):
    margin = max(data.obstacleSizes)
    #if no obstacles/enemes have been placed previously, automatically legal
    if len(data.obstacles) == 0 and len(data.enemies) == 0:
        return (enemyX, enemyY)
    #check that no obstacle is at that position
    if len(data.obstacles) != 0:
        for obstacle in data.obstacles:
            #if obstacle already at that location, find a new suitable location
            if (abs(obstacle.x - enemyX) < (margin)) and (
            abs(obstacle.y - enemyY) < (margin)):
                tempX = random.randint(margin, data.width-margin)
                tempY = random.randint(margin, data.height-margin)
                #recursive call, keep trying til we get pair of coords that work
                return checkEnemyCoords(data, tempX, tempY)
    #check that no enemy is at that position
    if len(data.enemies) != 0:
        for enemy in data.enemies:
            if (abs(enemy.x - enemyX) < (margin)) and (
            abs(enemy.y - enemyY) < (margin)):
                tempX = random.randint(margin, data.width-margin)
                tempY = random.randint(margin, data.height-margin)
                #recursive call, keep trying til we get pair of coords that work
                return checkEnemyCoords(data, tempX, tempY)
    #check that it isn't too close to the player
    if (abs(data.squareTop-enemyY) < margin) or (abs(
    data.squareLeft-enemyX) < margin):
        tempX = random.randint(margin, data.width-margin)
        tempY = random.randint(margin, data.height-margin)
        #recursive call, keep trying til we get pair of coords that work
        return checkEnemyCoords(data, tempX, tempY)
    return (enemyX, enemyY) #if you get through all, your location is fine
    
def checkObstacleCoords(data, obstacleX, obstacleY):
    #checks legality of obstacle position and returns True/False
    margin = max(data.obstacleSizes)
    #if no obstacles/enemes have been placed previously, automatically legal
    if len(data.obstacles) == 0 and len(data.enemies) == 0:
        return True
    #check that no obstacle is at that position
    if len(data.obstacles) != 0:
        for obstacle in data.obstacles:
            #if obstacle already at that location, not legal
            if (abs(obstacle.x - obstacleX) < (margin)) and (
            abs(obstacle.y - obstacleY) < (margin)):
                return False
    #check that no enemy is at that position
    if len(data.enemies) != 0:
        for enemy in data.enemies:
            if (abs(enemy.x - obstacleX) < (margin)) and (
            abs(enemy.y - obstacleY) < (margin)):
                return False
    return True #if you get through it all, the location is fine
    
def checkEnemyCoordsForMove(data, enemyX, enemyY, radius):
    #checks legality - True/False
    margin = max(data.obstacleSizes) / 2
    # #if no obstacles have been placed previously, automatically legal
    # if len(data.obstacles) == 0:
    #     return True
    
    #check that no obstacle is at that position
    # if len(data.obstacles) != 0:
    for obstacle in data.obstacles:
        #if obstacle already at that location, not legal
        if (abs(obstacle.x - enemyX) < (margin)) and (
        abs(obstacle.y - enemyY) < (margin)):
            return False
    return True #if you get through it all, the location is fine
    
def checkPlayerCoordsForMove(data, x, y):
    #checks legality - True/False
    margin = max(data.obstacleSizes) / 2
    #if no obstacles have been placed previously, automatically legal
    if len(data.obstacles) == 0:
        return True
    #check that no obstacle is at that position
    if len(data.obstacles) != 0:
        for obstacle in data.obstacles:
            #if obstacle already at that location, not legal
            if (abs(obstacle.x - x) < (margin)) and (
            abs(obstacle.y - y) < (margin)):
                return False
    return True #if you get through it all, the location is fine
    
def checkLaserCoordsForMove(data, x, y):
    #checks legality - True/False
    margin = max(data.obstacleSizes) / 2
    #if no obstacles have been placed previously, automatically legal
    if len(data.obstacles) == 0:
        return True
    #check that no obstacle is at that position
    if len(data.obstacles) != 0:
        for obstacle in data.obstacles:
            #if obstacle already at that location, not legal
            if (abs(obstacle.x - x) < (margin)) and (
            abs(obstacle.y - y) < (margin)):
                return False
    return True #if you get through it all, the location is fine

def helpKeyPressed(event, data):
    if event.keysym == "s":
        data.mode == "settings"
        settingsButtonPressed(data)
    elif event.keysym == "Return":
        data.mode == "game"
        initGame(data)

def settingsKeyPressed(event, data):
    if event.keysym == "h":
        data.mode == "help"
        initHelp(data)
    elif event.keysym == "Return":
        data.mode == "game"
        initGame(data)
    elif event.keysym == "d":
        if data.difficulty == "Easy":
            data.difficulty = "Hard"
        elif data.difficulty == "Hard":
            data.difficulty = "Easy"
        
def gameOverKeyPressed(event, data):
    if event.keysym == "Return":
        data.mode == "game"
        initGame(data)
    elif event.keysym == "s":
        data.mode == "settings"
        settingsButtonPressed(data)

def keyPressed(event, data):
    if data.mode == "game":
        if (event.char == "p"):
            data.isPaused = not data.isPaused
        if (event.keysym == "Left"):
            data.direction = "left"
            if data.obstaclesLeft == 0:
                moveLeft(data)
        elif (event.keysym == "Right"):
            data.direction = "right"
            if data.obstaclesLeft == 0:
                moveRight(data)
        elif (event.keysym == "Up"):
            data.direction = "up"
            if data.obstaclesLeft == 0:
                moveUp(data)
        elif (event.keysym == "Down"):
            data.direction = "down"
            if data.obstaclesLeft == 0:
                moveDown(data)
        elif (event.keysym == "space"):
            if data.obstaclesLeft == 0:
                newLaser = (data.squareLeft+(data.squareSize/2),
                data.squareTop+(data.squareSize/2))
                data.laserCenters.append(newLaser)
                data.laserDirections.append(data.direction)
    elif data.mode == "help":
        helpKeyPressed(event, data)
    elif data.mode == "settings":
        settingsKeyPressed(event, data)
    elif data.mode == "gameOver":
        gameOverKeyPressed(event, data)
            

def onButton(data, buttonId):
    if data.mode == "splash":
        if (buttonId == 1): playGameButtonPressed(data)
        elif (buttonId == 2): helpButtonPressed(data)
        elif (buttonId == 3): settingsButtonPressed(data)
    if data.mode == "splash":
        if (buttonId == 4): pass
        elif (buttonId == 5): pass
        elif (buttonId == 6): pass

def playGameButtonPressed(data):
    data.mode = "game"
    initGame(data)
    data.b1.grid_forget()
    data.b2.grid_forget()
    data.b3.grid_forget()
    data.buttonFrame.pack_forget()

def helpButtonPressed(data):
    data.mode = "help"
    initHelp(data)
    data.b1.grid_remove()
    data.b2.grid_remove()
    data.b3.grid_remove()
    data.buttonFrame.pack_forget()
    
def settingsButtonPressed(data):
    data.mode = "settings"
    data.b1.grid_forget()
    data.b2.grid_forget()
    data.b3.grid_forget()
    data.buttonFrame.pack_forget()
    initSettings(data)
    
#partially adapted from both
#https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO and
#http://www.guru99.com/reading-and-writing-files-in-python.html#2
def readFile(path):
    with open(path, "rt") as f:
        return f.readlines()

#adapted from https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def writeFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)
        
def getHighScores():
    tempScores = readFile("highscores.txt")
    scores = []
    for score in tempScores:
        scores.append(score.strip())
    #want to show top 3 scores, if there are less then we pad list with 0s
    if len(scores) < 5:
        while len(scores) < 5:
            scores.append("0")
    #adapted this 'key=float' thing from https://stackoverflow.com/a/17474264
    #citing it just to be safe
    scores.sort(key=float, reverse=True)
    return scores

def moveLeft(data):
    data.squareLeft -= data.moveSpeed
    x = (data.squareLeft+(data.squareSize/2))
    y = (data.squareTop+(data.squareSize/2))
    if data.powerupName != "moveThroughObstacles":
        if checkPlayerCoordsForMove(data, x, y) == False:
            #undo if you ran into obstacle
            data.squareLeft += data.moveSpeed

def moveRight(data):
    data.squareLeft += data.moveSpeed
    x = (data.squareLeft+(data.squareSize/2))
    y = (data.squareTop+(data.squareSize/2))
    if data.powerupName != "moveThroughObstacles":
        if checkPlayerCoordsForMove(data, x, y) == False:
            #undo if you ran into obstacle
            data.squareLeft -= data.moveSpeed

def moveUp(data):
    data.squareTop -= data.moveSpeed
    x = (data.squareLeft+(data.squareSize/2))
    y = (data.squareTop+(data.squareSize/2))
    if data.powerupName != "moveThroughObstacles":
        if checkPlayerCoordsForMove(data, x, y) == False:
            #undo if you ran into obstacle
            data.squareTop += data.moveSpeed

def moveDown(data):
    data.squareTop += data.moveSpeed
    x = (data.squareLeft+(data.squareSize/2))
    y = (data.squareTop+(data.squareSize/2))
    if data.powerupName != "moveThroughObstacles":
        if checkPlayerCoordsForMove(data, x, y) == False:
            #undo if you ran into obstacle
            data.squareTop -= data.moveSpeed

def timerFired(data):
    if data.mode == "game": gameTimerFired(data)
    if data.mode == "help" or data.mode == "settings":
        helpAndSettingsTimerFired(data)
    if data.mode == "gameOver": return
        
def gameTimerFired(data):
    if data.mode == "game":
        if data.obstaclesLeft == 0:
            if len(data.enemies) < data.maxEnemies: #continuously create enemies
                spawnEnemies(data)
            for enemy in data.enemies: #continuously move enemies
                enemy.move(data)
            data.numLasers = len(data.laserCenters)
            i = 0
            while i < data.numLasers:
                cx, cy = data.laserCenters[i]
                #move all lasers that have been created
                if data.laserDirections[i] == "right":
                    cx += data.laserLength
                elif data.laserDirections[i] == "left":
                    cx -= data.laserLength
                elif data.laserDirections[i] == "up":
                    cy -= data.laserLength
                elif data.laserDirections[i] == "down":
                    cy += data.laserLength
                data.laserCenters[i] = (cx,cy)
                
                if data.powerupName != "obstaclePiercingLaser":
                    #if you do have the powerup, don't do the check
                    #effectively allowing lasers to go through barriers
                    if checkLaserCoordsForMove(data, cx, cy) == False:
                        #check if laser hit an obstacle, delete it if so
                        data.laserCenters.pop(i)
                        data.laserDirections.pop(i)
                        data.numLasers = len(data.laserCenters)
                
                if cx <= 0 or cx >= data.width or cy <= 0 or cy >= data.height:
                    #check if laser goes off screen, delete it if so
                    data.laserCenters.pop(i)
                    data.laserDirections.pop(i)
                    data.numLasers = len(data.laserCenters)
                
                for enemy in data.enemies:
                    #check for enemies getting hit
                    if (abs(cx-enemy.x) < enemy.radius) and (abs(cy-enemy.y) <
                    enemy.radius):
                        enemy.health -=1 #enemy health goes down when hit
                        #make laser disappear if it hits enemy
                        data.laserCenters.pop(i)
                        data.laserDirections.pop(i)
                        data.numLasers = len(data.laserCenters)
                        if enemy.health == 0: #kill enemies that have been hit
                            if type(enemy) == bigCircle:
                                data.score += 2
                            elif type(enemy) == smallCircle:
                                data.score += 1
                            elif type(enemy) == biggerCircle:
                                data.score += 3
                            data.enemies.remove(enemy)
                i += 1
            
            if data.powerupName == "decoy":
                for enemy in data.enemies:
                    #check for enemies catching decoy
                    if (abs(data.decoyX - enemy.x) < (data.squareSize)) and (
                    abs(data.decoyY - enemy.y) < (data.squareSize)):
                        data.powerupName = ""
                        
            for enemy in data.enemies:
                #check for enemies catching you
                playerX = (data.squareLeft+(data.squareSize/2))
                playerY = (data.squareTop+(data.squareSize/2))
                if (abs(playerX - enemy.x) < (data.squareSize)) and (
                abs(playerY - enemy.y) < (data.squareSize)):
                    print("game over")
                    writeFile("highscores.txt", str(data.score) + "\n")
                    data.mode = "gameOver"
                    return
                    
            #if powerup still exists, check if you're able to pick it up
            if data.oldPowerupName != "":
                if (abs(data.squareLeft-data.powerup.x) < data.squareSize) and (
            abs(data.squareTop-data.powerup.y) < data.squareSize):
                    data.powerupName = data.oldPowerupName
                    data.oldPowerupName = ""
                    if data.powerupName == "increaseSpeed":
                        data.moveSpeed += 5
                    if data.powerupName == "decoy":
                        spawnDecoy(data)
                
def helpAndSettingsTimerFired(data):
    if data.textMax == True:
        if data.textSize > 40:
            data.textSize -= 1
        else: data.textMax = False
    elif data.textMax == False:
        if data.textSize < 80:
            data.textSize += 1
        else: data.textMax = True
            
def drawSquare(canvas, data):
    # some code adapted from events-example3.py
    # http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-animations.html
    if data.mode == "game":
        canvas.create_rectangle(data.squareLeft,
                                data.squareTop,
                                data.squareLeft + data.squareSize,
                                data.squareTop + data.squareSize,
                                fill=data.squareFill)

def drawDecoy(canvas, data):
    # some code adapted from events-example3.py
    # http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-animations.html
    x0 = data.decoyX - (data.squareSize/2)
    x1 = data.decoyX + (data.squareSize/2)
    y0 = data.decoyY - (data.squareSize/2)
    y1 = data.decoyY + (data.squareSize/2)
    if data.mode == "game":
        canvas.create_rectangle(x0, y0, x1, y1, fill=data.squareFill)
        
def drawLaser(canvas, data):
    if data.mode == "game":
        for i in range(len(data.laserCenters)):
            (cx, cy) = data.laserCenters[i]
            if data.laserDirections[i] == "right":
                canvas.create_line(cx+data.laserLength, cy,
            cx+(2*data.laserLength), cy, fill="red")
            elif data.laserDirections[i] == "left":
                canvas.create_line(cx-data.laserLength, cy,
            cx-(2*data.laserLength), cy, fill="red")
            elif data.laserDirections[i] == "up":
                canvas.create_line(cx, cy-data.laserLength, cx,
            cy-(2*data.laserLength), fill="red")
            elif data.laserDirections[i] == "down":
                canvas.create_line(cx, cy+data.laserLength, cx,
            cy+(2*data.laserLength), fill="red")

def drawPowerup(canvas, data):
    if data.mode == "game":
        if data.oldPowerupName != "": #if you haven't picked it up already
            data.powerup.draw(canvas)

def drawText(canvas, data):
    if data.mode == "splash":
        canvas.create_image(0,0,anchor="nw",image=data.title_tk)

    if data.mode == "game":
        canvas.create_text(data.width/2,data.height/2,
    text="Score: %d" % (data.score), fill="white" )
        if data.powerupName == "":
            s = "None"
        else:
            s = data.powerupName
        canvas.create_text(data.width/2,data.height/2 + 15,
    text="Powerup: %s" % (s), fill="white")
        canvas.create_text(data.width/2,data.height/2 + 30,
    text="Obstacles left to place: %d" % (data.obstaclesLeft), fill="white")

    elif data.mode == "help":
        drawBackground(canvas, data)
        canvas.create_text(data.width/2, data.height/8,
        text="Instructions", fill="white",
        font="Helvetica %d bold" % (data.textSize))
        canvas.create_text(data.width/2, data.height/4,
        text="Use the arrow keys to move", fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+50, 
        text="Hit 'space' to shoot enemies (who have varying levels of health)",
        fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+100, 
        text="Don't let enemies touch you!", fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+150,
        text="Click to place obstacles to block enemies", fill="white",
        font="Helvetica 20")
        s = '''Pick up yellow powerups like 'increase speed', 'decoy',
          'move through obstacles', and 'obstacle-piercing lasers' '''
        canvas.create_text(data.width/2, (data.height/4)+200,
        text=s, fill="white", font="Helvetica 20")
        s = "Visit settings menu to change difficulty or check the highscores"
        canvas.create_text(data.width/2, (data.height/4)+250, 
            text=s, fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+350, 
        text="Hit 's' to visit settings menu or 'return/enter' to start game",
        fill="white", font="Helvetica 20 bold")
            
    elif data.mode == "settings":
        drawBackground(canvas, data)
        canvas.create_text(data.width/2, data.height/8, text="Settings",
        fill="white", font="Helvetica %d bold" % (data.textSize))
        canvas.create_text(data.width/2, (data.height/4), 
        text="Current Difficulty: %s" % (data.difficulty), fill="white",
        font="Helvetica 20 bold")
        canvas.create_text(data.width/2, (data.height/4)+50, 
        text="Hit 'd' to switch difficulty level", fill="white",
        font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+100,
        text="High Scores", fill="white", font="Helvetica 20 bold")
        scores = getHighScores()
        canvas.create_text(data.width/2, (data.height/4)+125,
        text="#1: %s" % (scores[0]), fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+150,
        text="#2: %s" % (scores[1]), fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+175,
        text="#3: %s" % (scores[2]), fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+200,
        text="#4: %s" % (scores[3]), fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+225,
        text="#5: %s" % (scores[4]), fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/4)+300, 
        text="Hit 'h' to visit help screen or 'return/enter' to start game",
        fill="white", font="Helvetica 20 bold")
    
    elif data.mode == "gameOver":
        drawBackground(canvas, data)
        canvas.create_text(data.width/2, data.height/4, 
        text="Game Over", fill="white", font="Helvetica 36 bold")
        canvas.create_text(data.width/2, data.height/2,
        text="Score: %s" % (data.score), fill="white", font="Helvetica 20 bold")
        canvas.create_text(data.width/2, (data.height/2)+50,
        text="Press 's' to check the highscores or change settings",
        fill="white", font="Helvetica 20")
        canvas.create_text(data.width/2, (data.height/2)+100,
        text="Press 'return/enter' to play again", fill="white",
        font="Helvetica 20")
        
def drawBackground(canvas, data):
    #referenced from Pillow documentation
    #http://pillow.readthedocs.io/en/3.4.x/reference/ImageTk.html
    if data.mode == "splash":
        drawText(canvas, data)
    if data.mode == "game" or data.mode == "gameOver":
        canvas.create_image(0, 0, anchor="nw", image=data.bg_tk)
    else:
        canvas.create_image(0,0,anchor="nw",
        image=data.animated[data.count%len(data.animated)])
        data.count += 1

def redrawAll(canvas, data):
    if data.mode == "game":
        # draw background
        drawBackground(canvas, data)
        # draw the square
        drawSquare(canvas, data)
        # draw powerups
        drawPowerup(canvas, data)
        # draw the obstacles
        numObstacles = len(data.obstacles)
        for obstacle in data.obstacles:
            obstacle.draw(canvas)
        # draw the enemies
        for enemy in data.enemies:
            enemy.draw(canvas)
        # draw decoy, if there is one
        if data.powerupName == "decoy":
            drawDecoy(canvas, data)
        # draw lasers
        drawLaser(canvas, data)
        # draw the text
        drawText(canvas, data)
    elif data.mode != "splash":
        drawText(canvas, data)

####################################
# use the run function as-is
####################################

#adapted from events-example3.py
#http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-animations.html
def run(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.title("tp")
    root.geometry("600x600")
    root.resizable(width=FALSE, height=FALSE)
    root.configure(background="white")
    # create root and store root in data so buttons can access
    data.root = root
    init(data)
    # create the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    data.canvas = canvas
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)