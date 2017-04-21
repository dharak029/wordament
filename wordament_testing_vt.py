import pygame
import random
from random import randint
import itertools
from copy import deepcopy

words = ["python", "jack", "word", "code", "review", "funion",
         "light", "cat", "camel", "dog"]

letters = "qwertyuiopasdfghjklzxcvbnm"


# color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKTURQOISE = (3, 54, 73)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# time constants
TOTAL_TIME = 120
FRAME_RATE = 60
FRAME_COUNT = 0

# other constants
TIMER_X = 100
TIMER_Y = 65
Submit_X = 275
Submit_Y = 400
Reset_X = 100
Reset_Y = 400
Score_X = 275
Score_Y = 65

ROW_SIZE = 8
COL_SIZE = 8

grid = [[j for j in range(ROW_SIZE)] for i in range(COL_SIZE)]



def makeGrid(words, grid, size=[8, 8], attempts=10):
    '''Run attemptGrid trying attempts number of times.
    Size contains the height and width of the board.
    Word is a list of words it should contain.'''

    for _ in range(attempts):
        try:
            return attemptGrid(words, grid, size)
        except RuntimeError as e:

            pass
    else:
        print ("ERROR - Couldn't create valid board")
        raise

def attemptGrid(words, grid, size):
    '''Attempt a grid of letters to be a wordsearch
    Size contains the height and width of the board.
    Word is a list of words it should contain.
    Returns the 2D list grid and a dictionary of the words as keys and
    lists of their co-ordinates as values.'''

    #Make sure that the board is bigger than even the biggest word
    sizeCap = (size[0] if size[0] >= size[1] else size[1])
    sizeCap -= 1
    if any(len(word) > sizeCap for word in words):
        print ("ERROR: Too small a grid for supplied words.")
        return


    #Insert answers and store their locations
    answers = {}
    for word in words:
        grid, answer = insertWord(word,grid)
        answers[word] = answer

    #Add other characters to fill the empty space
    for i,j in itertools.product(range(size[1]),range(size[0])):
        if grid[i][j].char == ' ':
            grid[i][j].set_char(letters[randint(0,len(letters)-1)])

    return grid, answers

def insertWord(word, grid, invalid=None):
    '''Insert a word into the letter grid
    'word' will be inserted into the 2D list grid.
    invalid is either None or a list of coordinates
    These coordinates are denote starting points that don't work.
    Returns an updated grid as well as a list of the added word's indices.'''

    height, width = len(grid), len(grid[0])
    length = len(word)

    #Detect whether the word can fit horizontally or vertically.
    hori = width >= length + 1
    vert = height >= length + 1
    if hori and vert:
        #If both can be true, flip a coin to decide which it will be
        hori = bool(randint(0,1))
        vert = not hori

    line = [] #For storing the letters' locations
    if invalid is None:
        invalid = [[None,None,True],[None,None,False]]

    #Height * width is an approximation of how many attempts we need
    for _ in range(height*width):
        if hori:
            x = randint(0,width-1-length)
            y = randint(0,height-1)
        else:
            x = randint(0,width-1)
            y = randint(0,height-1-length)
        if [y,x,hori] not in invalid:
            break
    else:
        # Probably painted into a corner, raise an error to retry.
        raise(RuntimeError)

    start = [y, x, hori] #Saved in case of invalid placement
    #Now attempt to insert each letter
    for letter in word:
        if grid[y][x].get_char() in (' ', letter):
            line.append([y,x])
            if hori:
                x += 1
            else:
                y += 1
        else:
            #We found a place the word can't fit
            #Mark the starting point as invalid
            invalid.append(start)
            return insertWord(word, grid, invalid)

    #Since it's a valid place, write to the grid and return
    for i,cell in enumerate(line):
        grid[cell[0]][cell[1]].set_char(word[i])
    return grid, line

# ===copied code ends===================================================================================================




class Tile:
    def __init__(self, x, y, screen):
        self.char = ' '
        self.textInactive = BASICFONT.render(self.char, True, BLACK)
        self.textActive = BASICFONT.render(self.char, True, WHITE)
        self.rect = pygame.Rect(x, y, 30, 30)
        self.coords = (x + 10, y + 10)
        self.surf = pygame.surface.Surface((30, 30))
        self.active = False
        self.time_to_cover = None
        self.screen = screen
        self.row = y/35 - 3
        self.col = x/35 - 3

    def draw(self):
        self.surf.fill(GREEN)
        self.screen.blit(self.surf, self.rect)
        self.screen.blit(self.textInactive, self.coords)

    def update(self, active):
        if active:
            self.surf.fill(RED)
            self.screen.blit(self.surf, self.rect)
            self.screen.blit(self.textActive, self.coords)
        else:
            self.surf.fill(GREEN)
            self.screen.blit(self.surf, self.rect)
            self.screen.blit(self.textInactive, self.coords)

    def updateState(self, event):
        # check left button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # check position
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.update(self.active)
        return self.active, self.char

    def set_char(self, char):
        self.char = char
        self.textInactive = BASICFONT.render(self.char, True, BLACK)
        self.textActive = BASICFONT.render(self.char, True, WHITE)

    def get_char(self):
        return self.char

# ----------------------------------------------------------------------

def main():
    global BASICFONT
    pygame.init()
    pygame.display.set_caption('Wordament')
    screen = pygame.display.set_mode((500, 500))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
    screen.fill(DARKTURQOISE)
    pygame.draw.rect(screen, WHITE, [100, 100, 285, 285])
    grid = createTiles(screen)
    startGame(screen, grid)
    pygame.quit()


# creating buttons
def submitButton(screen):
    text = 'Submit'
    basicfont = pygame.font.Font('freesansbold.ttf', 30)
    submitbutton = basicfont.render(text, True, WHITE)
    rect = pygame.Rect(Submit_X, Submit_Y, submitbutton.get_width() + 5, submitbutton.get_height() - 5)
    surf = pygame.surface.Surface(rect.size)
    surf.fill(GREEN)
    screen.blit(surf, rect)
    screen.blit(submitbutton, (Submit_X, Submit_Y))
    return rect


def resetButton(screen):
    text = 'Reset'
    basicfont = pygame.font.Font('freesansbold.ttf', 30)
    submitbutton = basicfont.render(text, True, WHITE)
    rect = pygame.Rect(Reset_X, Reset_Y, submitbutton.get_width() + 5, submitbutton.get_height() - 5)
    surf = pygame.surface.Surface(rect.size)
    surf.fill(GREEN)
    screen.blit(surf, rect)
    screen.blit(submitbutton, (Reset_X, Reset_Y))
    return rect


# creating scorelabel
def scoreLabel(screen, score):
    text = 'Score:' + score
    basicfont = pygame.font.Font('freesansbold.ttf', 30)
    scorelabel = basicfont.render(text, True, WHITE)
    rect = pygame.Rect(Score_X, Score_Y, scorelabel.get_width() + 5, scorelabel.get_height() - 5)
    surf = pygame.surface.Surface(rect.size)
    surf.fill(GREEN)
    screen.blit(surf, rect)
    screen.blit(scorelabel, (Score_X, Score_Y))


def createTiles(screen):

    # create
    for row in range(ROW_SIZE):
        for col in range(COL_SIZE):
            row_pix = (row + 3) * 35
            col_pix = (col + 3) * 35
            grid[row][col] = Tile(col_pix, row_pix, screen)

    # set character values function here use the grid[][] List

    # set characters
    display_grid, answers = makeGrid(words, grid)


    # draws
    for of_row in display_grid:
        for tile in of_row:
            tile.draw()

    return display_grid


def getTile(grid, event):
    for row in grid:
        for tile in row:
            if tile.rect.collidepoint(event.pos):
                return tile


def checkAlignment(lastTiles, currentTile):
    horizontal = None
    tile1 = lastTiles[0]
    tile2 = currentTile
    if tile1.row == tile2.row:
        horizontal = True
    if tile1.col == tile2.col:
        horizontal = False

    return horizontal

def validTile(lastTile, currentTile, horizontal):
    pass


def runClock(screen, clock):
    global FRAME_COUNT
    basicfont = pygame.font.Font('freesansbold.ttf', 30)
    total_seconds = TOTAL_TIME - (FRAME_COUNT // FRAME_RATE)

    if total_seconds < 0:
        total_seconds = 0
        return False

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    timer = "{0:02}:{1:02}".format(minutes, seconds)

    timeLabel = basicfont.render(timer, True, WHITE)
    rect = pygame.Rect(TIMER_X, TIMER_Y, timeLabel.get_width() + 5, timeLabel.get_height())
    # del. CAUTION! Update the constants in header
    surf = pygame.surface.Surface(rect.size)

    surf.fill(DARKTURQOISE)
    screen.blit(surf, rect)
    screen.blit(timeLabel, (TIMER_X, TIMER_Y))

    FRAME_COUNT += 1

    clock.tick(FRAME_RATE)


def startGame(screen, grid):
    global FRAME_COUNT
    score = 0
    submit = submitButton(screen)
    reset = resetButton(screen)
    scoreLabel(screen, '0')
    clock = pygame.time.Clock()
    found_words = []
    word = ""
    prevTiles = []
    horizontal = None
    while True:
        pygame.display.flip()

        runningClock = runClock(screen, clock)
        if runningClock is not None and not runningClock:
            # del. for now it closes the window, code to be written
            # del. current total time is set to 3 sec for debug purpouse check TOTAL_TIME on line 13
            return

        # events thread
        for event in pygame.event.get():

            # exit events
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            # game events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tile = getTile(grid, event)
                if tile:  # check if the component clicked is a tile
                    if len(prevTiles) == 0:
                        tile.updateState(event)
                        prevTiles.append(tile)
                        word = word + "" + tile.char
                    elif len(prevTiles) == 1:
                        horizontal = checkAlignment(prevTiles, tile)
                        if horizontal is not None:
                            tile.updateState(event)
                            prevTiles.append(tile)
                            word = word + "" + tile.char
                    else: # length > 2
                        if horizontal:
                            lastTile = prevTiles[-1]
                            if lastTile.row == tile.row and lastTile.col < tile.col:
                                tile.updateState(event)
                                prevTiles.append(tile)
                                word = word + "" + tile.char
                        if not horizontal:
                            lastTile = prevTiles[-1]
                            if lastTile.col == tile.col and lastTile.row < tile.row:
                                tile.updateState(event)
                                prevTiles.append(tile)
                                word = word + "" + tile.char

                    print(word)  # del. check console when you execute this
                if reset.collidepoint(event.pos):
                    screen = pygame.display.set_mode((500, 500))
                    screen.fill(DARKTURQOISE)
                    pygame.draw.rect(screen, WHITE, [100, 100, 285, 285])
                    grid = createTiles(screen)
                    score = 0
                    scoreLabel(screen, str(score))
                    submit = submitButton(screen)
                    reset = resetButton(screen)
                    clock = pygame.time.Clock()
                    FRAME_COUNT = 0
                    runClock(screen, clock)
                if submit.collidepoint(event.pos):
                    for x in words:
                        if (word == x and word not in found_words):
                            score = score + 1
                            scoreLabel(screen, str(score))
                            found_words.append(word)
                    word = ""


# calling main()
if __name__ == '__main__':
    main()