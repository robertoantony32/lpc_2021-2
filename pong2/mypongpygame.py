import pygame
from pygame.locals import *
from random import choice

pygame.init()

# screen dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


# player object
class Player:
    # function for player dimensions
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        # movement of the player
        self.up = False
        self.down = False

        self.score = 0

        self.powerShot_k = False

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

    # function that calls the other functions previously programmed
    def update(self):
        self.movement()
        self.is_colliding_with_limits()

    # function for drawing the player
    def render(self, screen: pygame.surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# bot object
class Bot:
    # bot stats
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.score = 1

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

# ball object
class Ball:
    # Ball structure function
    def __init__(self, x, y):
        # dimensions
        self.width = 20
        self.height = 20

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

            # setting the bounce sound
            pygame.mixer.Sound('assets/bounce.wav').play()

            # reaction of the ball when it touches the bottom of the paddle 1
            if player.rect.bottom >= self.rect.top > (player.rect.centery + 20):
                self.dy = 1
                if player.powerShot_k:
                    self.SPEED = 20

            # reaction of the ball when it touches the top of the paddle 1
            elif player.rect.top <= self.rect.bottom < (player.rect.centery - 20):
                self.dy = -1
                if player.powerShot_k:
                    self.SPEED = 20


            # reaction of the ball when it touches the middle of the paddle 1
            elif (player.rect.centery + 20) >= self.rect.centery > (player.rect.centery - 20):
                self.dy = 0
                if player.powerShot_k:
                    self.SPEED = 20

        # colliding with paddle 2 verification
        elif self.rect.colliderect(bot.rect) and self.dx > 0:
            self.dx *= -1

            # setting the bounce sound
            pygame.mixer.Sound('assets/bounce.wav').play()

            # reaction of the ball when it touches the bottom of the paddle 2
            if bot.rect.bottom >= self.rect.top > (bot.rect.centery - 15):
                self.dy = 1
                if self.SPEED > 5:
                    self.SPEED = 5

            # reaction of the ball when it touches the top of the paddle 2
            elif bot.rect.top <= self.rect.bottom < (bot.rect.centery - 15):
                self.dy = -1
                if self.SPEED > 5:
                    self.SPEED = 5

            # reaction of the ball when it touches the middle of the paddle 2
            elif (bot.rect.centery + 15) >= self.rect.centery > (bot.rect.centery - 15):
                self.dy = 0
                if self.SPEED > 5:
                    self.SPEED = 5

    # check the collision of the with boundaries of the screen
    def is_colliding_with_limits(self):
        if self.rect.top >= WINDOW_HEIGHT or self.rect.bottom <= 0:
            self.dy *= -1
            pygame.mixer.Sound('assets/bounce.wav').play()

        # setting the player score
        elif self.rect.right >= WINDOW_WIDTH:
            pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav').play()
            self.rect.x = 640
            self.rect.y = 360
            self.dx *= -1
            self.SPEED = 5
            player.score += 1
            self.dy = choice([1, -1])

        # setting the bot score
        elif self.rect.left <= 0:
            pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav').play()
            self.rect.x = 640
            self.rect.y = 360
            self.dx *= -1
            self.SPEED = 5
            bot.score += 1
            self.dy = choice([1, -1])

    # function that calls the other functions previously programmed
    def update(self):
        self.rect.y += self.dy * self.SPEED
        self.rect.x += self.dx * self.SPEED
        self.is_colliding_with_limits()
        self.is_colliding_with_paddle()

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
SCORE_MAX = 1

# text function
def text_creator(text_value, x, y, font_size):
    font = pygame.font.Font('assets/PressStart2P.ttf', font_size)
    text = font.render(text_value, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    Screen.blit(text, text_rect)


is_run = True

# screen loop
while is_run:
    # fps
    clock.tick(60)

    # verification to pick up interactions with the keyboard or mouse
    for event in pygame.event.get():
        # defining a way out of the game
        if event.type == QUIT:
            is_run = False

        # checking for when the key is pressed
        elif event.type == KEYDOWN:
            # setting the player movement
            if event.key == K_UP:
                player.up = True
            elif event.key == K_DOWN:
                player.down = True

            # setting the player power shot key
            elif event.key == K_x:
                player.powerShot_k = True

        # checking when the key is released
        elif event.type == KEYUP:
            # setting the player movement
            if event.key == K_UP:
                player.up = False
            elif event.key == K_DOWN:
                player.down = False

            elif event.key == K_x:
                player.powerShot_k = False

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
        text_creator(f'{player.score}x{bot.score}', 630, 50, 50)

    else:
        Screen.fill((0, 0, 0))
        text_creator(f'{player.score}x{bot.score}', 630, 50, 50)
        text_creator('Press U to restart game... ', 550, 600, 30)
        if player.score == SCORE_MAX:
            # drawing the victory text
            text_creator('YOU WIN!!!', 630, 310, 50)
        elif bot.score == SCORE_MAX:
            # drawing the lose text
            text_creator('YOU LOSE :(', 630, 300, 50)

    pygame.display.flip()
