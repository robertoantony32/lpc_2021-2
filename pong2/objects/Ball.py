# ball object
from random import choice

import pygame

from utils.dimensions import *


class Ball:

    # ball structure function
    def __init__(self, x, y):
        # ball direction
        self.dy = 1
        self.dx = 1
        # speed of the ball
        self.SPEED = 5
        self.rect = pygame.Rect(x, y, 20, 20)

    #  colliding function
    def is_colliding_with_paddle(self, player, bot):
        #  colliding with paddle 1 verification
        if self.rect.colliderect(player.rect) and self.dx < 0:
            self.dx *= -1

            # power_shot verification
            if player.special_power_k and player.current >= 5 and player.special_power_on:
                # reset of the special power cooldown
                player.special_power_frame = 0
                player.special_power_on = False

                # ball boost
                self.SPEED = 20
                player.current = 0

            # setting the bounce sound
            pygame.mixer.Sound('assets/bounce.wav').play()

            # reaction of the ball when it touches the bottom of the paddle 1
            if player.rect.bottom >= self.rect.top > (player.rect.centery + 20):
                self.dy = 1
            # reaction of the ball when it touches the top of the paddle 1
            elif player.rect.top <= self.rect.bottom < (player.rect.centery - 20):
                self.dy = -1
            # reaction of the ball when it touches the middle of the paddle 1
            elif (player.rect.centery + 20) >= self.rect.centery > (player.rect.centery - 20):
                self.dy = 0

        # colliding with paddle 2 verification
        elif self.rect.colliderect(bot.rect) and self.dx > 0:
            self.dx *= -1

            # setting the bounce sound
            pygame.mixer.Sound('assets/bounce.wav').play()

            # reaction of the ball when it touches the bottom of the paddle 2
            if bot.rect.bottom >= self.rect.top > (bot.rect.centery - 20):
                self.dy = 1
                if self.SPEED > 5:
                    self.SPEED = 5

            # reaction of the ball when it touches the top of the paddle 2
            elif bot.rect.top <= self.rect.bottom < (bot.rect.centery - 20):
                self.dy = -1
                if self.SPEED > 5:
                    self.SPEED = 5

            # reaction of the ball when it touches the middle of the paddle 2
            elif (bot.rect.centery + 20) >= self.rect.centery > (bot.rect.centery - 20):
                self.dy = 0
                if self.SPEED > 5:
                    self.SPEED = 5

    # check the collision of the ball with boundaries of the screen
    def is_colliding_with_limits(self, player, bot):
        if self.rect.top >= WINDOW_HEIGHT or self.rect.bottom <= 0:
            self.dy *= -1
            pygame.mixer.Sound('assets/bounce.wav').play()

        # setting the score
        elif self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav').play()
            if self.rect.right >= WINDOW_WIDTH:
                player.score += 1
            elif self.rect.left <= 0:
                bot.score += 1
            self.rect.x = 640
            self.rect.y = 360
            self.dx *= -1
            self.SPEED = 5
            self.dy = choice([1, -1])

    # function that calls the other functions previously programmed
    def update(self, player, bot):
        self.rect.y += self.dy * self.SPEED
        self.rect.x += self.dx * self.SPEED
        self.is_colliding_with_limits(player, bot)
        self.is_colliding_with_paddle(player, bot)

    # function for restarting the game
    def restart_ball(self):
        self.rect.x = 640
        self.rect.y = 360
        self.SPEED = 5

    # function to draw the ball
    def render(self, screen: pygame.surface):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
