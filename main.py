"""
This module contains the main game logic for a simple Pygame-based game.
"""

import time
import sys
import random
import pygame


# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
GROUND_HEIGHT = 20

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_green = (0, 200, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Slingshot Game')

# Load images
bird_image = pygame.image.load('bird.png')
box_image = pygame.image.load('box.png')

# Scale images
bird_image = pygame.transform.scale(bird_image, (50, 50))
box_image = pygame.transform.scale(box_image, (50, 50))

# Bird settings
bird_pos = [150, 450]
bird_speed = [0, 0]
bird_acceleration = [0, 0.5]  # Gravity
BIRD_DRAG = 0.99  # Air resistance
BIRD_LAUNCHED = False
MOUSE_START = None

# Box settings
def create_boxes():
    """
    Create a list of boxes with random positions.

    Returns:
        list: A list of box positions, each represented as a [x, y] coordinate.
    """
    return [[random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50), random.randint(400, 550)]
            for _ in range(5)]

boxes = create_boxes()

# Button settings
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 36)

button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT
                          // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT)

# Game over settings
MISSED_SHOTS = 0
MAX_MISSED_SHOTS = 3
GAME_OVER = False
YOU_DID_IT = False
GAME_OVER_TEXT = ''
YOU_DID_IT_TEXT = ''

# Main game loop
RUNNING = True
while RUNNING:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (GAME_OVER or YOU_DID_IT) and button_rect.collidepoint(event.pos):
                boxes = create_boxes()
                bird_pos = [150, 450]
                bird_speed = [0, 0]
                BIRD_LAUNCHED = False
                MOUSE_START = None
                MISSED_SHOTS = 0
                GAME_OVER = False
                YOU_DID_IT = False
            elif not BIRD_LAUNCHED and not GAME_OVER:
                MOUSE_START = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and not BIRD_LAUNCHED:
            if MOUSE_START and not GAME_OVER:
                mouse_end = pygame.mouse.get_pos()
                distance = ((MOUSE_START[0] - mouse_end[0]) ** 2 + (MOUSE_START[1] - mouse_end[1])
                            ** 2) ** 0.5
                bird_speed = [(MOUSE_START[0] - mouse_end[0]) / 10, (MOUSE_START[1] - mouse_end[1])
                              / 10]
                bird_speed = [speed * (distance / 50) for speed in bird_speed]
                BIRD_LAUNCHED = True

    if BIRD_LAUNCHED and not GAME_OVER:
        # Apply gravity
        bird_speed[1] += bird_acceleration[1]
        # Apply drag
        bird_speed[0] *= BIRD_DRAG
        bird_speed[1] *= BIRD_DRAG
        # Update position
        bird_pos[0] += bird_speed[0]
        bird_pos[1] += bird_speed[1]

        # Check for collisions with boxes
        bird_rect = pygame.Rect(bird_pos[0], bird_pos[1], 50, 50)
        for box in boxes:
            box_rect = pygame.Rect(box[0], box[1], 50, 50)
            if bird_rect.colliderect(box_rect):
                boxes.remove(box)
                bird_speed = [0, 0]
                BIRD_LAUNCHED = False
                bird_pos = [150, 450]
                MOUSE_START = None

        # Check for collision with ground or going beyond the screen
        if bird_pos[1] >= SCREEN_HEIGHT - GROUND_HEIGHT - 50:
            bird_pos[1] = SCREEN_HEIGHT - GROUND_HEIGHT - 50
            screen.blit(bird_image, bird_pos)
            pygame.display.flip()
            time.sleep(2)
            bird_speed = [0, 0]
            BIRD_LAUNCHED = False
            bird_pos = [150, 450]
            MOUSE_START = None
            MISSED_SHOTS += 1
            if MISSED_SHOTS >= MAX_MISSED_SHOTS:
                GAME_OVER = True

        # Check for going above the screen
        if bird_pos[1] < 0:
            bird_pos[1] = 0
            bird_speed[1] = abs(bird_speed[1])  # Reverse the vertical speed

    # Check if all boxes are destroyed and missed shots are less than max allowed
    if not boxes and not GAME_OVER and MISSED_SHOTS < MAX_MISSED_SHOTS:
        YOU_DID_IT = True

    # Fill the screen with white
    screen.fill(white)

    # Draw the ground
    pygame.draw.rect(screen, green, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Draw the bird
    screen.blit(bird_image, bird_pos)

    # Draw the boxes with small movements
    for box in boxes:
        box[0] += random.randint(-1, 1)
        box[1] += random.randint(-1, 1)
        box[0] = max(SCREEN_WIDTH // 2, min(SCREEN_WIDTH - 50, box[0]))
        box[1] = max(400, min(550, box[1]))
        screen.blit(box_image, box)

    # Draw the slingshot trajectory and strength
    if MOUSE_START and not BIRD_LAUNCHED and not GAME_OVER:
        mouse_current = pygame.mouse.get_pos()
        pygame.draw.line(screen, red, (bird_pos[0] + 25, bird_pos[1] + 25), mouse_current, 5)
        distance = ((MOUSE_START[0] - mouse_current[0]) ** 2
                    + (MOUSE_START[1] - mouse_current[1]) ** 2) ** 0.5
        strength_text = FONT.render(f'Strength: {int(distance)}', True, black)
        screen.blit(strength_text, (10, 50))

    # Draw game over text and restart button
    if GAME_OVER or YOU_DID_IT:
        if GAME_OVER:
            GAME_OVER_TEXT = FONT.render('GAME OVER', True, red)
            screen.blit(GAME_OVER_TEXT, (SCREEN_WIDTH // 2 - GAME_OVER_TEXT.get_width()
                                         // 2, SCREEN_HEIGHT // 2 - GAME_OVER_TEXT.get_height()
                                         // 2))
        if YOU_DID_IT:
            YOU_DID_IT_TEXT = FONT.render('YOU DID IT!', True, blue)
            screen.blit(YOU_DID_IT_TEXT, (SCREEN_WIDTH // 2 - YOU_DID_IT_TEXT.get_width()
                                          // 2, SCREEN_HEIGHT // 2 - YOU_DID_IT_TEXT.get_height()
                                          // 2))
        button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT
                                  // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        pygame.draw.rect(screen, black, button_rect, 2)
        button_text = FONT.render('Restart Game', True, BUTTON_TEXT_COLOR)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

    # Draw missed shots count
    missed_shots_text = FONT.render(f'{MISSED_SHOTS}/{MAX_MISSED_SHOTS}', True, black)
    screen.blit(missed_shots_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)
