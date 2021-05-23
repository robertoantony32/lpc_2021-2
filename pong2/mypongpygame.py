import pygame
from pygame.locals import *

from objects.Ball import Ball
from objects.Player import Player
from utils.dimensions import *


# text function
def text_creator(text_value, x, y, font_size):
    font = pygame.font.Font('assets/PressStart2P.ttf', font_size)
    text = font.render(text_value, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    Screen.blit(text, text_rect)
    return text_rect


# bot object
class Bot:
    # bot stats
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.score = 0
        self.bot_SPEED = 5

    # bot movement
    def bot_movement(self):
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
    def update(self):
        self.bot_movement()
        self.is_colliding_with_limits()

    # function to draw the bot paddle
    def render(self, screen: pygame.surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # function for restarting the game
    def restart_bot(self):
        self.score = 0
        self.rect.x = 1180
        self.rect.y = 300


if __name__ == '__main__':
    # setting the screen
    pygame.init()

    Screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("MyPong - Pygame by Roberto.")

    # setting the fps
    clock = pygame.time.Clock()

    # setting the objects
    player = Player(50, 300)
    ball = Ball(640, 360)
    bot = Bot(1180, 300)

    # score max
    SCORE_MAX = 3

    is_running = True

    # start Key value
    start_key = False

    count_for_restart = 10
    fps_count = 0

    # movement start text var
    start_text = text_creator('Press SPACE to start the game!!', 630, 580, 30)
    start_text_dy = 1

    # movement restart text var
    restart_text = text_creator(f'Press U to restart the game... {count_for_restart}', 630, 600, 30)
    restart_text_dy = 1

    # screen loop
    while is_running:
        # fps
        clock.tick(60)

        # verification to pick up interactions with the keyboard or mouse
        for event in pygame.event.get():

            # defining a way out of the game
            if event.type == QUIT:
                is_running = False

            # checking for when the key is pressed
            elif event.type == KEYDOWN:

                # setting the player movement
                if event.key == K_UP:
                    player.up = True
                elif event.key == K_DOWN:
                    player.down = True

                # setting the start key
                elif event.key == K_SPACE:
                    start_key = True

                # Verification for restart key
                elif player.score == SCORE_MAX or bot.score == SCORE_MAX:

                    # setting a restart key
                    if event.key == K_u:
                        player.restart_player()
                        bot.restart_bot()
                        ball.restart_ball()
                        count_for_restart = 10

                # setting the player power shot key
                elif event.key == K_x:
                    player.special_power_k = True

            # checking when the key is released
            elif event.type == KEYUP:

                # setting the player movement
                if event.key == K_UP:
                    player.up = False
                elif event.key == K_DOWN:
                    player.down = False

                elif event.key == K_x:
                    player.special_power_k = False

        # Menu text
        Screen.fill((0, 0, 0))
        text_creator('PONG!', 640, 100, 70)
        text_creator('Hold UP to go up.', 630, 310, 20)
        text_creator('Hold DOWN to go down.', 630, 340, 20)
        text_creator('Hold X to do a special power.', 630, 370, 20)
        text_creator('Press SPACE to start the game!!', 630, start_text.y, 30)

        # movement for start game text
        start_text.y += start_text_dy
        if start_text.y >= 580 and start_text_dy > 0:
            start_text_dy *= -1
        elif start_text.y <= 550 and start_text_dy < 0:
            start_text_dy *= -1

        if start_key:

            # win condition verification
            if player.score < SCORE_MAX and bot.score < SCORE_MAX:
                player.update()
                ball.update(player, bot)
                bot.update()
                Screen.fill((0, 0, 0))
                player.render(Screen)
                ball.render(Screen)
                bot.render(Screen)

                # update the score
                text_creator(f'{player.score} | {bot.score}', 630, 50, 50)

            else:
                Screen.fill((0, 0, 0))
                text_creator(f'{player.score} | {bot.score}', 630, 50, 50)

                # setting a time for the countdown
                fps_count += 1

                # setting a condition for the countdown
                if fps_count == 60:
                    count_for_restart -= 1
                    fps_count = 0

                    # setting a condition for closing the game
                    if count_for_restart == 0:
                        # Restarting the stats of all objects
                        player.restart_player()
                        bot.restart_bot()
                        ball.restart_ball()
                        count_for_restart = 10
                        start_key = False

                text_creator(f'Press U to restart the game... {count_for_restart}',
                             630, restart_text.y, 30)

                # movement of the restart text
                restart_text.y += restart_text_dy
                if restart_text.y >= 615 and restart_text_dy > 0:
                    restart_text_dy *= -1
                elif restart_text.y <= 590 and restart_text_dy < 0:
                    restart_text_dy *= -1

                if player.score == SCORE_MAX:

                    # drawing the victory text
                    text_creator('YOU WIN!!!', 650, 340, 50)

                elif bot.score == SCORE_MAX:
                    # drawing the lose text
                    text_creator('YOU LOSE.', 630, 300, 50)

        pygame.display.flip()
