import pygame
import random

# color         = (  R    G    B
WHITE           = (255, 255, 255)
BLACK           = (  0,   0,   0)
DARKTURQOISE    = (  3,  54,  73)
RED             = (255,   0,   0)
GREEN           = (  0, 255,   0)
BLUE            = (  0,   0, 255)



class Tile:

    def __init__(self, x, y, screen):
        BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
        self.value = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.textInactive = BASICFONT.render(self.value, True, BLACK)
        self.textActive = BASICFONT.render(self.value, True, WHITE)
        self.rect = pygame.Rect(x, y, 30, 30)
        self.coords = (x + 10, y + 10)
        self.surf = pygame.surface.Surface((30, 30))
        self.clicked = False
        self.time_to_cover = None
        self.screen = screen

    def draw(self):
        self.surf.fill(GREEN)
        self.screen.blit(self.surf, self.rect)
        self.screen.blit(self.textInactive, self.coords)


    def update(self):
        self.surf.fill(RED)
        self.screen.blit(self.surf, self.rect)
        screen.blit(self.textActive, self.coords)

    def handle_event(self, event):
        # check left button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # check position
            if self.rect.collidepoint(event.pos):
                print(event.pos)
                self.clicked = True
                self.update()

#----------------------------------------------------------------------

# init

pygame.init()

screen = pygame.display.set_mode((500, 500))
screen.fill(DARKTURQOISE)
pygame.draw.rect(screen, BLUE, [100, 100, 285, 285])


# create tiles

tiles = []
for y in range(3, 11):
    for x in range(3, 11):
        tiles.append(Tile(x*35, y*35, screen))

# draws
for x in tiles:
   x.draw()

# mainloop

clock = pygame.time.Clock()
running = True

while running:

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for x in tiles:
            x.handle_event(event)

    # updates

    for x in tiles:
        pass#x.update(screen)



    pygame.display.flip()

    # clock

    clock.tick(25)

pygame.quit()