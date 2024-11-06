import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1400
screen_height = 800
ground_level = 550

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_green = (0, 200, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
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
bird_launched = False
mouse_start = None

# Box settings
def create_boxes():
    return [[random.randint(500, 750), random.randint(400, 550)] for _ in range(5)]

boxes = create_boxes()

# Global gravity setting
gravity = 0.5

# Button settings
button_width = 150
button_height = 30
button_rect = pygame.Rect((screen_width - button_width) // 2, 10, button_width, button_height)
button_color = green
button_hover_color = dark_green
button_text_color = black
font = pygame.font.Font(None, 36)

# Game over settings
missed_shots = 0
max_missed_shots = 3
game_over = False

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                boxes = create_boxes()
                bird_pos = [150, 450]
                bird_speed = [0, 0]
                bird_launched = False
                mouse_start = None
                missed_shots = 0
                game_over = False
            elif not bird_launched and not game_over:
                mouse_start = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and not bird_launched and mouse_start and not game_over:
            mouse_end = pygame.mouse.get_pos()
            distance = ((mouse_start[0] - mouse_end[0]) ** 2 + (mouse_start[1] - mouse_end[1]) ** 2) ** 0.5
            bird_speed = [(mouse_start[0] - mouse_end[0]) / 10, (mouse_start[1] - mouse_end[1]) / 10]
            bird_speed = [speed * (distance / 50) for speed in bird_speed]
            bird_launched = True

    if bird_launched and not game_over:
        bird_speed[1] += gravity
        bird_pos[0] += bird_speed[0]
        bird_pos[1] += bird_speed[1]

        # Check for collisions with boxes
        bird_rect = pygame.Rect(bird_pos[0], bird_pos[1], 50, 50)
        for box in boxes:
            box_rect = pygame.Rect(box[0], box[1], 50, 50)
            if bird_rect.colliderect(box_rect):
                boxes.remove(box)
                bird_speed = [0, 0]
                bird_launched = False
                bird_pos = [150, 450]
                mouse_start = None

        # Check for collision with ground
        if bird_pos[1] >= ground_level:
            bird_speed = [0, 0]
            bird_launched = False
            bird_pos = [150, 450]
            mouse_start = None
            missed_shots += 1
            if missed_shots >= max_missed_shots:
                game_over = True

    # Restart game if all boxes are destroyed
    if not boxes and not game_over:
        boxes = create_boxes()
        bird_pos = [150, 450]
        bird_speed = [0, 0]
        bird_launched = False
        mouse_start = None

    # Fill the screen with white
    screen.fill(white)

    # Draw the bird
    screen.blit(bird_image, bird_pos)

    # Draw the boxes
    for box in boxes:
        screen.blit(box_image, box)

    # Draw the slingshot trajectory
    if mouse_start and not bird_launched and not game_over:
        mouse_current = pygame.mouse.get_pos()
        pygame.draw.line(screen, red, (bird_pos[0] + 25, bird_pos[1] + 25), mouse_current, 5)

    # Draw the restart button
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, black, button_rect, 2)
    button_text = font.render('Restart Game', True, button_text_color)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Draw game over text
    if game_over:
        game_over_text = font.render('GAME OVER', True, red)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)
