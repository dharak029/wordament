import pygame
import random

white = (255, 255, 255)
darkturqoise = (3, 54, 73)
black = (0, 0, 0)


class Tile:
    def __init__(self, x, y, image, cover):
        self.image = image
        self.cover = cover
        self.rect = pygame.Rect(x, y, 30, 30)
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
            '''if self.rect.collidepoint(event.pos):
                self.covered = not self.covered
                if not self.covered:
                    # if uncovered then set +2000ms to cover
                    #self.time_to_cover = pygame.time.get_ticks() + 2000'''


# ----------------------------------------------------------------------

# init

pygame.init()

screen = pygame.display.set_mode((550, 550))
screen.fill(darkturqoise)


total_time = 120
frame_rate = 60
frame_count = 0

basicfont = pygame.font.Font('freesansbold.ttf', 30)

# create images

# char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

img = pygame.surface.Surface((30, 30))
img.fill((255, 0, 0))

cov = pygame.surface.Surface((30, 30))
cov.fill((0, 255, 0))

# create tiles-

tiles = []
for y in range(3, 11):
    for x in range(3, 11):
        tiles.append(Tile(x * 35, y * 35, img, cov))

# mainloop

clock = pygame.time.Clock()

running = True

while running:

    # events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        for x in tiles:
            x.handle_event(event)


    # Timer

    total_seconds = total_time - (frame_count // frame_rate)

    if total_seconds < 0:
        total_seconds = 0

    minutes = total_seconds // 60

    seconds = total_seconds % 60

    timer = "{0:02}:{1:02}".format(minutes, seconds)

    text = basicfont.render(timer, True, black)

    screen.fill(darkturqoise)
    screen.blit(text, [100, 65])

    frame_count += 1

    clock.tick(frame_rate)

    pygame.draw.rect(screen, white, [100, 100, 285, 285])

    # updates

    for x in tiles:
        x.update()

    # draws

    for x in tiles:
        x.draw(screen)

    pygame.display.flip()

pygame.quit()