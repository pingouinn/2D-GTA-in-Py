import pyxel

class Game(object):
    def __init__(self):
        #Init pyxel
        self.x = 240
        self.y = 270
        pyxel.init(self.x, self.y, title="GTA 2D Remake by Pingouin#8843", fps = 60)
        pyxel.tilemap(0)
        pyxel.load("src/assets/avoidThem.pyxres")

        #Classes
        self.player = Player()
        self.vehicle = Vehicle()

        #Variables
        self.baseColor = [[0 for y in range(self.y)] for x in range(self.x)]

        pyxel.run(self.update, self.draw)

    def GetPixelColors(self):
        """Save the pixel colors of the map"""
        for x in range(self.x):
            for y in range(self.y):
                self.baseColor[x][y] = pyxel.pget(x, y)

    def update(self):
        """Mise à jour des variables (60 fPS)"""
        self.player.movement(self.x, self.y)

    def draw(self):
        """Création et positionnement des objets (60fps)"""
        #Clear screen
        pyxel.cls(0)
        #Draw map
        pyxel.blt(0, 0, 1, 0, 0, self.x, self.y/2)
        pyxel.blt(0, self.y/2, 1, 0, 0, self.x, self.y/2)
        #Save the pixel colors of the map only at the init of the game
        if self.baseColor[0][0] == 0:
            self.GetPixelColors()
        #Draw
        self.player.draw(self.baseColor)
        self.vehicle.draw()

class Player(object):
    def __init__(self):

        #Coords
        self.x = 50
        self.y = 115

        #Logics
        self.speed = 1
        self.savedBlit = (0, 0)
        self.frameCounter = -1
        self.legSpeed = 16

        #State variables
        self.isRunning = False
        self.lastPosIsSide = False

    def calculateBlit(self, column, line, isSide, legRate):
        if not isSide :
            otherLine = 1 if line == 3 else 3
            if self.savedBlit[0] != column or self.savedBlit == (column, 0) or self.savedBlit == (column, otherLine) or self.savedBlit == (column, otherLine+1):
                self.savedBlit = (column, line)
                self.frameCounter = 0
            elif self.frameCounter > legRate and self.savedBlit == (column, line):
                self.savedBlit = (column, line + 1)
                self.frameCounter = 0
            elif self.frameCounter > legRate and self.savedBlit == (column, line + 1):
                self.savedBlit = (column, line)
                self.frameCounter = 0
        else:
            otherLine = 0 if line == 2 else 2
            if self.savedBlit[0] != column or self.savedBlit == (column, otherLine) or self.savedBlit == (column, otherLine+1):
                self.savedBlit = (column, line)
                self.frameCounter = 0
            elif self.frameCounter > legRate and self.savedBlit == (column, line):
                self.savedBlit = (column, line + 1)
                self.frameCounter = 0
            elif self.frameCounter > legRate and self.savedBlit == (column, line + 1):
                self.savedBlit = (column, line)
                self.frameCounter = 0

    def movement(self, x, y):

        # Determine player speed
        if pyxel.btnp(pyxel.KEY_SHIFT):
            self.isRunning = not self.isRunning

        if self.isRunning:
            speed = self.speed
            legRate = self.legSpeed/2
        else:
            speed = self.speed/2
            legRate = self.legSpeed


        self.frameCounter += 1
        if self.frameCounter > 18:
            if self.lastPosIsSide:
                self.savedBlit = (3, 0)
            else: 
                self.savedBlit = (0, 0)


        #Determine player movement
        #L and R
        if pyxel.btn(pyxel.KEY_D) and not pyxel.btn(pyxel.KEY_Z) and not pyxel.btn(pyxel.KEY_S) and self.x < x-16:
            self.x += 1.5 * speed
            self.calculateBlit(3, 3, False, legRate)
            self.lastPosIsSide = True
    
        elif pyxel.btn(pyxel.KEY_Q) and not pyxel.btn(pyxel.KEY_Z) and not pyxel.btn(pyxel.KEY_S) and self.x > 0:
            self.x -= 1.5 * speed
            self.calculateBlit(3, 1, False, legRate)
            self.lastPosIsSide = True

        #Fwd, Fwd-L, Fwd-R
        elif pyxel.btn(pyxel.KEY_Z) and not pyxel.btn(pyxel.KEY_D) and not pyxel.btn(pyxel.KEY_Q) and self.y > 0:
            self.y -= 1.5 * speed
            self.calculateBlit(0, 1, False, legRate)
            self.lastPosIsSide = False

        elif pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_Q) and self.x > 0 and self.y > 0:
            self.y -= 1 * speed
            self.x -= 1 * speed
            self.calculateBlit(1, 0, True, legRate)

        elif pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_D) and self.x < x-16 and self.y > 0:
            self.y -= 1 * speed
            self.x += 1 * speed
            self.calculateBlit(2, 0, True, legRate)

        #Back, Back-L, Back-R
        elif pyxel.btn(pyxel.KEY_S) and not pyxel.btn(pyxel.KEY_D) and not pyxel.btn(pyxel.KEY_Q) and self.y < y - 16:
            self.y += 1.5 * speed
            self.calculateBlit(0, 3, False, legRate)
            self.lastPosIsSide = False

        elif pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_Q) and self.x > 0 and self.y < y - 16:
            self.y += 1 * speed
            self.x -= 1 * speed
            self.calculateBlit(2, 2, True, legRate)

        elif pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_D) and self.x < x-16 and self.y < y - 16:
            self.y += 1 * speed
            self.x += 1 * speed
            self.calculateBlit(1, 2, True, legRate)

    def GetCorrectValue(self, value, mapSave, isX):
        tempVal = round(value)
        if isX :
            if tempVal < len(mapSave):
                return tempVal
        else:
            if tempVal < len(mapSave[0]):
                return tempVal
        return tempVal - 1
        
    def draw(self, mapSave):
        pyxel.blt(self.x, self.y, 0, self.savedBlit[0]*16, self.savedBlit[1]*16, 16, 16)
        for x in range(16):
            for y in range(16):
                if pyxel.pget(self.x+x, self.y+y) == 0:
                    pyxel.pset(self.x+x, self.y+y, mapSave[self.GetCorrectValue(self.x+x, mapSave, True)][self.GetCorrectValue(self.y+y, mapSave, False)])

        

class Vehicle(object):
    def __init__(self):
        #Coords
        self.x = 1
        self.y = 28

        #Logics
        self.speed = 3
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 1, 87, 36, 23)

if __name__ == '__main__':
    game = Game()