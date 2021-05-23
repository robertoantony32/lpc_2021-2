# player object
import pygame

from utils.dimensions import WINDOW_HEIGHT


class Player:
    # function for player dimensions
    def __init__(self, x, y):
        # setting the stats of the sprites
        self.sprites = []
        for number_sprite in range(6):
            self.sprites.append(pygame.image.load(f'sprites/special_power{number_sprite}.png'))

        self.current = 0
        self.image = self.sprites[self.current]

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        # movement of the player
        self.up = False
        self.down = False
        self.score = 0

        # setting a cooldown for special power
        self.special_power_k = False
        self.special_power_frame = 0
        self.special_power_cooldown = 200
        self.special_power_on = True

    # function for the movement of the player
    def movement(self):
        if self.up:
            self.rect.y -= 5
        elif self.down:
            self.rect.y += 5

    # player colliding with limits
    def is_colliding_with_limits(self):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.y = 570
        elif self.rect.top <= 0:
            self.rect.y = 0

    def special_power_animate(self):
        if self.special_power_k and self.special_power_on:
            self.current += 0.2
            if self.current >= len(self.sprites):
                self.current = 5
        else:
            self.current = 0

    # function that calls the other functions previously programmed
    def update(self):
        self.special_power_frame += 1
        if self.special_power_frame == self.special_power_cooldown:
            self.special_power_on = True

        self.special_power_animate()
        self.movement()
        self.is_colliding_with_limits()

    # function for drawing the player
    def render(self, screen: pygame.surface):
        screen.blit(self.sprites[int(self.current)], (self.rect.x, self.rect.y))

    # function for restarting the game
    def restart_player(self):
        self.score = 0
        self.special_power_on = True
        self.rect.x = 50
        self.rect.y = 300
