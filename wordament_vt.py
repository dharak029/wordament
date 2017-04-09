import pygame
import random

# color = (  R    G    B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKTURQOISE = (3, 54, 73)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Tile:
    def __init__(self, x, y, screen):
        BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
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
    startGame(tiles)
    pygame.quit()


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



def startGame(tiles):
    clock = pygame.time.Clock()
    found_words=[]
    word=""
    while True:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tile = getTile(tiles, event)
                tile.updateState(event)
                word = word+""+tile.value
                print(word) # check console when you execute this

        # updates

        for tile in tiles:
            pass#tile.update(screen)



        pygame.display.flip()

        # clock

        clock.tick(25)


if __name__ == '__main__':
    main()
