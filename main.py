import time
import pygame
import sys

pygame.init()

#Starting Dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Breakout Game')
clock = pygame.time.Clock()
running = True

class Game:
    def __init__(self, player, ball, brick_group):
        self.player = player
        self.ball = ball
        self.brick_group = brick_group
        self.score = 0
        self.lives = 2
        self.round_number = 1
        self.font = pygame.font.SysFont('couriernew', 30)

    def update(self):
        self.check_game_over()
        self.start_new_round()
        self.draw()
        self.check_collisions()
        self.draw()

    def check_game_over(self):
        if self.ball.rect.top >= WINDOW_HEIGHT:
            if self.lives <= 1:
                self.lives = 2
                self.score = 0
                self.round_number = 1
                self.brick_group.empty()
                self.ball.speed = self.ball.starting_speed
                self.ball.rect.center = self.ball.starting_position
                self.player.rect.center = (self.player.starting_x, self.player.starting_y)
                num_bricks = 10
                brick_spacing = 2  # Adjust this value based on your preference

                # Create bricks in a loop with horizontal spacing
                for i in range(num_bricks):
                    for j in range(6):
                        brick_width = 128
                        brick_height = 45
                        x = 5 + i * (brick_width + brick_spacing)
                        y = 128 + j * (brick_height + brick_spacing)
                        my_brick_group.add(Brick(j, x, y))

            else:
                self.lives -= 1
                self.ball.rect.center = self.ball.starting_position

    def start_new_round(self):
        '''check if all bricks are gone to start a new round'''
        if len(self.brick_group) == 0 and self.lives > 0:
            print('hey')
            self.round_number += 1
            self.ball.rect.center = self.ball.starting_position
            self.player.rect.center = (self.player.starting_x, self.player.starting_y)
            self.ball.speed = self.ball.starting_speed
            num_bricks = 10
            brick_spacing = 2  # Adjust this value based on your preference

            # Create bricks in a loop with horizontal spacing
            for i in range(num_bricks):
                for j in range(6):
                    brick_width = 128
                    brick_height = 45
                    x = 5 + i * (brick_width + brick_spacing)
                    y = 128 + j * (brick_height + brick_spacing)
                    self.brick_group.add(Brick(j, x, y))


    def check_collisions(self):
        '''Check collisions between different sprites'''
        if pygame.sprite.spritecollide(self.player, [self.ball], False):
            self.ball.dy = -1
        collided_brick = pygame.sprite.spritecollide(self.ball, self.brick_group, True)
        if collided_brick:
            for brick in collided_brick:
                if brick.color_num == 4 or brick.color_num == 5:
                    self.score += 1
                elif brick.color_num == 2 or brick.color_num == 3:
                    self.score += 2
                    if self.ball.speed < self.ball.max_speed:
                        self.ball.speed += 1
                elif brick.color_num == 0 or brick.color_num == 1:
                    self.score += 3
                    if self.ball.speed < self.ball.max_speed:
                        self.ball.speed += 2
            self.ball.dy *= -1

    def draw(self):
        '''draw some text to the screen'''
        self.score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.round_text = self.font.render(f'Round: {self.round_number}', True, (255, 255, 255))
        screen.blit(self.score_text, (WINDOW_WIDTH-200, 40))
        screen.blit(self.lives_text, (30, 40))
        screen.blit(self.round_text, (30, 80))

class Brick(pygame.sprite.Sprite):
    def __init__(self, color_num, x, y):
        #0, 1 --> red, 2, 3 --> yellow, 4, 5--> green
        super(Brick, self).__init__()
        self.x = x
        self.y = y
        self.color_num = color_num

        #brick color base on their number
        if self.color_num == 0 or self.color_num == 1:
            self.image = pygame.transform.scale(pygame.image.load('red_brick.png'), (100, 30))
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        if self.color_num == 2 or self.color_num == 3:
            self.image = pygame.transform.scale(pygame.image.load('yellow_brick.png'), (100, 30))
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        if self.color_num == 4 or self.color_num == 5:
            self.image = pygame.transform.scale(pygame.image.load('green_brick.png'), (100, 30))
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.starting_speed = 2
        self.speed = self.starting_speed
        self.max_speed = 10
        self.starting_position = (WINDOW_WIDTH//2, WINDOW_HEIGHT-100)

        self.image = pygame.transform.scale(pygame.image.load('ball.png'), (16, 16))
        self.rect = self.image.get_rect()
        self.rect.center = self.starting_position

        #direction in the x or y axis
        self.dx = -1
        self.dy = -1

    def move(self):
        #changing the direction base on where the ball hit
        if self.rect.right >= WINDOW_WIDTH:
            self.dx = -1
        elif self.rect.left <= 0:
            self.dx = 1
        elif self.rect.top <= 0:
            self.dy = 1

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def update(self):
        self.move()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.starting_x = WINDOW_WIDTH//2
        self.starting_y = WINDOW_HEIGHT - 60

        #Create the player image and turning it to a rect
        self.image = pygame.transform.scale(pygame.image.load('player_block.png'), (280, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (self.starting_x, self.starting_y)

        self.velocity = 8

    def move(self):
        '''Move the player from left to right'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.right < WINDOW_WIDTH:
                self.rect.x += self.velocity
        elif keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= self.velocity

    def update(self):
        self.move()

my_player = Player()
my_ball = Ball()

#Create groups to put the sprite in
my_player_group = pygame.sprite.Group()
my_ball_group = pygame.sprite.Group()
my_brick_group = pygame.sprite.Group()

my_player_group.add(my_player)
my_ball_group.add(my_ball)

num_bricks = 10
brick_spacing = 2 # Adjust this value based on your preference

# Create bricks in a loop with horizontal spacing
for i in range(num_bricks):
    for j in range(6):
        brick_width = 128
        brick_height = 45
        x = 5 + i * (brick_width + brick_spacing)
        y = 128 + j * (brick_height + brick_spacing)
        my_brick_group.add(Brick(j, x, y))

my_game = Game(my_player, my_ball, my_brick_group)

while running:
    for event in pygame.event.get():
        #check for certain event types
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill('black')

    #updating and drawing the sprite groups
    my_player_group.update()
    my_player_group.draw(screen)

    my_ball_group.update()
    my_ball_group.draw(screen)

    my_brick_group.update()
    my_brick_group.draw(screen)

    my_game.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()