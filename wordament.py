import pygame
import random

class Tile:

    def __init__(self, x, y, image, cover):
        self.image = image
        self.cover = cover
        self.rect = pygame.Rect(x, y, 20, 20)
        self.covered = True
        self.time_to_cover = None

    def draw(self, screen):
        # draw cover or image
        if self.covered:
            screen.blit(self.cover, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self):
        # hide card (after 2000ms)
        if not self.covered and pygame.time.get_ticks() >= self.time_to_cover:
            self.covered = True

    def handle_event(self, event):
        # check left button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # check position
            if self.rect.collidepoint(event.pos):
                self.covered = not self.covered
                if not self.covered:
                    # if uncovered then set +2000ms to cover
                    self.time_to_cover = pygame.time.get_ticks() + 2000

#----------------------------------------------------------------------

# init

pygame.init()

screen = pygame.display.set_mode((195,195))

# create images

char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

img = pygame.surface.Surface((20, 20))
img.fill((255,0,0))

cov = pygame.surface.Surface((20, 20))
cov.fill((0,255,0))

# create tiles-

tiles = []
for y in range(8):
    for x in range(8):
        tiles.append( Tile(x*25, y*25, img, cov) )

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
        x.update()

    # draws

    for x in tiles:
        x.draw(screen)

    pygame.display.flip()

    # clock

    clock.tick(25)

pygame.quit()