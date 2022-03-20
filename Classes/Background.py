import pygame


class Background(object):
    def __init__(self, background):
        self.bg_image = background
        self.bg_width = self.bg_image.get_rect().width
        self.bgX = 0
        self.bgX2 = self.bg_width
        self.moving_speed = 10

    def draw(self, win):
        win.blit(self.bg_image, (self.bgX, 0))
        win.blit(self.bg_image, (self.bgX2, 0))

    def handle_move(self, keys, playerCollided, playerDirection):
        if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and ((keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]) or (not keys[pygame.K_RIGHT] and keys[pygame.K_LEFT])):

            self.bgX += self.moving_speed if keys[pygame.K_LEFT] else (
                self.moving_speed) * -1
            self.bgX2 += self.moving_speed * \
                1 if keys[pygame.K_LEFT] else self.moving_speed * -1

            if keys[pygame.K_LEFT] and (playerCollided and playerDirection != pygame.K_LEFT or not playerCollided):
                if self.bgX > self.bg_width:
                    self.bgX = (self.bg_width) * -1
                if self.bgX2 > self.bg_width:
                    self.bgX2 = (self.bg_width) * -1

            if keys[pygame.K_RIGHT] and (playerCollided and playerDirection != pygame.K_RIGHT or not playerCollided):
                if self.bgX < self.bg_width * -1:
                    self.bgX = self.bg_width
                if self.bgX2 < self.bg_width * -1:
                    self.bgX2 = self.bg_width
