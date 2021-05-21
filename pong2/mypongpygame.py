import pygame
from pygame.locals import *
from random import choice

pygame.init()

# screen dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


# text function
def text_creator(text_value, x, y, font_size):
    font = pygame.font.Font('assets/PressStart2P.ttf', font_size)
    text = font.render(text_value, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    Screen.blit(text, text_rect)
    return text_rect

# player object
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


# ball object
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
    def is_colliding_with_paddle(self):
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
    def is_colliding_with_limits(self):
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
    def update(self):
        self.rect.y += self.dy * self.SPEED
        self.rect.x += self.dx * self.SPEED
        self.is_colliding_with_limits()
        self.is_colliding_with_paddle()

    # function for restarting the game
    def restart_ball(self):
        self.rect.x = 640
        self.rect.y = 360
        self.SPEED = 5

    # function to draw the ball
    def render(self, screen: pygame.surface):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)


# setting the screen
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
            ball.update()
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
                   
                    # Restarting the stats of all obejcts
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
