import pygame
import random
from PyDictionary import PyDictionary

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

class Tile:
    def __init__(self, x, y, screen):
        self.value = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.textInactive = BASICFONT.render(self.value, True, BLACK)
        self.textActive = BASICFONT.render(self.value, True, WHITE)
        self.rect = pygame.Rect(x, y, 30, 30)
        self.coords = (x + 10, y + 10)
        self.surf = pygame.surface.Surface((30, 30))
        self.active = False
        self.time_to_cover = None
        self.screen = screen

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
        return self.active, self.value


# ----------------------------------------------------------------------

def main():
    global BASICFONT
    pygame.init()
    pygame.display.set_caption('Wordament')
    screen = pygame.display.set_mode((500, 500))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
    screen.fill(DARKTURQOISE)
    pygame.draw.rect(screen, WHITE, [100, 100, 285, 285])
    tiles = createTiles(screen)
    startGame(screen, tiles)
    pygame.quit()


#creating buttons
def submitButton(screen):
    text = 'Submit'
    basicfont = pygame.font.Font('freesansbold.ttf', 30)
    submitbutton = basicfont.render(text, True, WHITE)
    rect = pygame.Rect(Submit_X, Submit_Y, submitbutton.get_width() + 5, submitbutton.get_height()-5)
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


#creating scorelabel
def scoreLabel(screen,score):
    text = 'Score:'+score
    basicfont = pygame.font.Font('freesansbold.ttf', 30)
    scorelabel = basicfont.render(text, True, WHITE)
    rect = pygame.Rect(Score_X, Score_Y, scorelabel.get_width() + 5, scorelabel.get_height() - 5)
    surf = pygame.surface.Surface(rect.size)
    surf.fill(GREEN)
    screen.blit(surf, rect)
    screen.blit(scorelabel, (Score_X, Score_Y))


def createTiles(screen):
    # create
    tiles = []
    for y in range(3, 11):
        for x in range(3, 11):
            tiles.append(Tile(x * 35, y * 35, screen))

    # draws
    for x in tiles:
        x.draw()
    return tiles

def getTile(tiles, event):
    for tile in tiles:
        if tile.rect.collidepoint(event.pos):
            return tile


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
    rect = pygame.Rect(TIMER_X, TIMER_Y, timeLabel.get_width()+5, timeLabel.get_height())
    # del. CAUTION! Update the constants in header
    surf = pygame.surface.Surface(rect.size)

    surf.fill(DARKTURQOISE)
    screen.blit(surf, rect)
    screen.blit(timeLabel, (TIMER_X, TIMER_Y))

    FRAME_COUNT += 1

    clock.tick(FRAME_RATE)

def startGame(screen, tiles):
    score = 0
    submit = submitButton(screen)
    reset = resetButton(screen)
    scoreLabel(screen,'0')
    clock = pygame.time.Clock()
    found_words=[]
    word=""

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
                tile = getTile(tiles, event)
                if tile: # check if it is a valid tile
                    tile.updateState(event)
                    word = word+""+tile.value
                    print(word) # del. check console when you execute this
                if reset.collidepoint(event.pos):
                    main()
                if submit.collidepoint(event.pos):
                    if(word=='DOG'):
                        score = score+1
                        scoreLabel(screen, str(score))


# calling main()
if __name__ == '__main__':
    main()
