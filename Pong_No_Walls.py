import pygame, sys, time, random
from pygame.locals import *

# Set up pygame
pygame.init()
main_clock = pygame.time.Clock()

# Set up window
window_width = 800
window_height = 400
window_surface = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption('Pong')

# Set up scores
player1_score = 0
player2_score = 0
p1_wins = 0
p2_wins = 0

# Set up colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
basic_font = pygame.font.SysFont(None, 36)

# Set up paddle data structure
player1_side = pygame.Rect(785, 125, 15, 150)
player1_side_image = pygame.transform.scale(pygame.image.load('player1.png'), (15, 150))
player1_top = pygame.Rect(550, 0, 150, 15)
player1_top_image = pygame.transform.scale(pygame.image.load('player1_horizontal.png'), (150, 15))
player1_bottom = pygame.Rect(550, 385, 150, 15)
player1_bottom_image = pygame.transform.scale(pygame.image.load('player1_horizontal.png'), (150, 15))

player2_side = pygame.Rect(0, 125, 15, 150)
player2_side_image = pygame.transform.scale(pygame.image.load('player2.png'), (15, 150))
player2_top = pygame.Rect(150, 0, 150, 15)
player2_top_image = pygame.transform.scale(pygame.image.load('player2_horizontal.png'), (150, 15))
player2_bottom = pygame.Rect(150, 385, 150, 15)
player2_bottom_image = pygame.transform.scale(pygame.image.load('player2_horizontal.png'), (150, 15))

# Ball direction variables
# Get random number between 0-3 for ball direction
DOWNLEFT = 0
DOWNRIGHT = 1
UPLEFT = 2
UPRIGHT = 3

# Randomly get ball direction
direction = random.randint(0, 3)

# Set up ball data structure
ball = pygame.Rect(385, 150, 25, 25)
balls = [ball]
ball_image = pygame.transform.scale(pygame.image.load('sphere.png'), (25, 25))

# Set up keyboard variables
move_left = False
move_right = False
move_up = False
move_down = False
move_speed = 5

# Set up sounds
bounce_sound = pygame.mixer.Sound('bounce.wav')
out_of_bounds = pygame.mixer.Sound('out_of_bounds.wav')


# Functions
def draw_ball(ball):
    window_surface.blit(ball_image, ball)


# Reset ball function to spawn at net after point made
def reset_ball():
    ball.x = 385
    ball.y = 150
    direction = random.randint(0, 3)
    return direction


# AI function to control computer paddles by comparing center coordinates
# of paddle to center coordinate of balls
def computer_top_bottom(ball, direction, player2_top, player2_bottom, move_speed):
    if direction == 2 or direction == 3:
        if player2_top.centerx < ball.centerx and player2_top.right < window_width / 2:
            player2_top.x += move_speed
            player2_bottom.x += move_speed
        elif player2_top.centerx > ball.centerx and player2_top.left > 0:
            player2_top.x -= move_speed
            player2_bottom.x -= move_speed
    if direction == 0 or direction == 1:
        if player2_bottom.centerx < ball.centerx and player2_bottom.right < window_width / 2:
            player2_top.x += move_speed
            player2_bottom.x += move_speed
        elif player2_bottom.centerx > ball.centerx and player2_bottom.left > 0:
            player2_top.x -= move_speed
            player2_bottom.x -= move_speed
    return player2_top, player2_bottom


# Separate AI function to control computer side paddle (same principle as top/bottom paddles)
def computer_side(ball, direction, player2_side, move_speed):
    if direction == 0 or direction == 2:
        if player2_side.centery < ball.centery and player2_side.bottom < window_height:
            player2_side.y += move_speed
        elif player2_side.centery > ball.centery and player2_side.top > 0:
            player2_side.y -= move_speed
    return player2_side


def display_score(score1, score2, player_wins, cpu_wins):
    # Scoreboard text
    scoreboard = basic_font.render('Computer: %s/11             Player: %s/11' % (score2, score1), True, WHITE)
    wins = basic_font.render('Wins: %s/3             Wins: %s/3' % (cpu_wins, player_wins), True, WHITE)
    score_text = scoreboard.get_rect()
    wins_text = wins.get_rect()
    score_text.centerx = window_surface.get_rect().centerx - 15
    score_text.centery = window_surface.get_rect().centery
    wins_text.centerx = window_surface.get_rect().centerx - 15
    wins_text.centery = window_surface.get_rect().centery + 35
    window_surface.blit(wins, wins_text)
    window_surface.blit(scoreboard, score_text)


# Run game loop only when number of wins is below 3
while p1_wins < 2 or p2_wins < 2:
    # Check for QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Change keyboard variables
            if event.key == K_UP or event.key == K_w:
                move_down = False
                move_up = True
            if event.key == K_DOWN or event.key == K_s:
                move_up = False
                move_down = True
            if event.key == K_LEFT or event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == K_d:
                move_left = False
                move_right = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP or event.key == K_w:
                move_up = False
            if event.key == K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = False

    # Draw background onto surface
    window_surface.fill(BLACK)

    # controls ball movement
    ball_speed = random.randint(5, 15)
    for b in balls:
        if direction == DOWNLEFT:
            ball.left -= ball_speed
            ball.top += ball_speed
        if direction == DOWNRIGHT:
            ball.left += ball_speed
            ball.top += ball_speed
        if direction == UPLEFT:
            ball.left -= ball_speed
            ball.top -= ball_speed
        if direction == UPRIGHT:
            ball.left += ball_speed
            ball.top -= ball_speed

        # Check if collision with player1 paddles
        if player1_top.colliderect(ball):
            if ball.top < player1_top.bottom:
                bounce_sound.play()
                # box has moved past the top
                if direction == UPLEFT:
                    direction = DOWNLEFT
                if direction == UPRIGHT:
                    direction = DOWNRIGHT
        elif player1_bottom.colliderect(ball):
            bounce_sound.play()
            if ball.bottom > player1_bottom.top:
                # box has moved past the bottom
                if direction == DOWNLEFT:
                    direction = UPLEFT
                if direction == DOWNRIGHT:
                    direction = UPRIGHT
        elif player1_side.colliderect(ball):
            bounce_sound.play()
            if ball.right > player1_side.left:
                # box has moved past the bottom
                if direction == DOWNRIGHT:
                    direction = DOWNLEFT
                if direction == UPRIGHT:
                    direction = UPLEFT
                    '''
        else:
            # Ball has moved out of window without colliding with a paddle
            if (ball.top < 0 or ball.bottom > window_height) and \
                    (ball.left > (window_width / 2) or ball.right < window_width):
                out_of_bounds.play()
                if player2_score < 10:
                    player2_score += 1
                    direction = reset_ball()
                else:
                    player2_score = 0
                    p2_wins += 1
                    
            if (ball.top < 0 or ball.bottom > window_height) and \
                    (ball.left < 0 or ball.right < window_width / 2):
                out_of_bounds.play()
                if player1_score < 10:
                    player1_score += 1
                    direction = reset_ball()
                else:
                    player1_score = 0
                    p1_wins += 1

        '''
        # Check if collision with player2 paddles
        elif player2_top.colliderect(ball):
            bounce_sound.play()
            if ball.top < player2_top.bottom:
                # box has moved past the top
                if direction == UPLEFT:
                    direction = DOWNLEFT
                if direction == UPRIGHT:
                    direction = DOWNRIGHT
        elif player2_bottom.colliderect(ball):
            bounce_sound.play()
            if ball.bottom > player2_bottom.top:
                # box has moved past the bottom
                if direction == DOWNLEFT:
                    direction = UPLEFT
                if direction == DOWNRIGHT:
                    direction = UPRIGHT
        elif player2_side.colliderect(ball):
            bounce_sound.play()
            if ball.left < player2_side.right:
                # box has moved past the left side
                if direction == DOWNLEFT:
                    direction = DOWNRIGHT
                if direction == UPLEFT:
                    direction = UPRIGHT
        else:
            # Ball has moved out of window without colliding with a paddle
            '''
            if (ball.top < 0 or ball.bottom > window_height) and (ball.left < 0 or ball.right < window_width / 2):
                out_of_bounds.play()
                if player1_score < 10:
                    player1_score += 1
                    direction = reset_ball()
                else:
                    player1_score = 0
                    p1_wins += 1
                    '''
        # Ball has moved out of window without colliding with a paddle
        if (ball.top < 0 or ball.bottom > window_height or ball.right > window_width) and \
                (ball.left > 400 or ball.right < window_width):
            out_of_bounds.play()
            if player2_score < 10:
                player2_score += 1
                direction = reset_ball()
            else:
                player2_score = 0
                p2_wins += 1

        if (ball.top < 0 or ball.bottom > window_height or ball.left < 0) and \
                (ball.left < 0 or ball.right < window_width / 2):
            out_of_bounds.play()
            if player1_score < 10:
                player1_score += 1
                direction = reset_ball()
            else:
                player1_score = 0
                p1_wins += 1

    # Draw the net
    pygame.draw.line(window_surface, WHITE, (400, 0), (400, 400), 5)

    # Draw player1 paddles
    window_surface.blit(player1_side_image, player1_side)
    window_surface.blit(player1_top_image, player1_top)
    window_surface.blit(player1_bottom_image, player1_bottom)

    # Draw player 2 paddles
    window_surface.blit(player2_side_image, player2_side)
    window_surface.blit(player2_top_image, player2_top)
    window_surface.blit(player2_bottom_image, player2_bottom)

    # Draw the ball
    draw_ball(ball)

    # Move player1 paddles
    if move_down and player1_side.bottom < window_height:
        player1_side.top += move_speed
    if move_up and player1_side.top > 0:
        player1_side.top -= move_speed
    if move_left and player1_top.left > 400:
        player1_top.left -= move_speed
        player1_bottom.left -= move_speed
    if move_right and player1_top.right < window_width:
        player1_top.right += move_speed
        player1_bottom.right += move_speed

    # Computer artificial intelligence paddles
    computer_top_bottom(ball, direction, player2_top, player2_bottom, move_speed)
    computer_side(ball, direction, player2_side, move_speed)

    display_score(player1_score, player2_score, p1_wins, p2_wins)

    # Draw window onto screen
    pygame.display.update()
    main_clock.tick(40)
