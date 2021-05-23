# bot object
import pygame

from utils.dimensions import WINDOW_HEIGHT


class Bot:
    # bot stats
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.score = 0
        self.bot_SPEED = 5

    # bot movement
    def bot_movement(self, ball):
        if self.rect.top < ball.rect.y:
            self.rect.top += self.bot_SPEED
        if self.rect.bottom > ball.rect.y and self.rect.top > ball.rect.y:
            self.rect.bottom -= self.bot_SPEED

    # bot colliding with limits
    def is_colliding_with_limits(self):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.y = 570
        elif self.rect.top <= 0:
            self.rect.y = 0

    # function that calls the other functions previously programmed
    def update(self, ball):
        self.bot_movement(ball)
        self.is_colliding_with_limits()

    # function to draw the bot paddle
    def render(self, screen: pygame.surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # function for restarting the game
    def restart_bot(self):
        self.score = 0
        self.rect.x = 1180
        self.rect.y = 300
