import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

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
    return [[random.randint(500, 750), random.randint(350, 500)] for _ in range(5)]

boxes = create_boxes()

ground_box = pygame.Rect(0, screen_height - 50, screen_width, 50)

# Physics settings
gravity = 0.5

# Button settings
button_rect = pygame.Rect(700, 50, 80, 30)
button_color = green
button_text_color = black
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
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
            elif not bird_launched:
                mouse_start = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and not bird_launched:
            mouse_end = pygame.mouse.get_pos()
            bird_speed = [(mouse_start[0] - mouse_end[0]) / 10, (mouse_start[1] - mouse_end[1]) / 10]
            bird_launched = True

    if bird_launched:
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

    # Check for collision with the ground box
    if bird_rect.colliderect(ground_box):
        bird_speed = [0, 0]
        bird_launched = False
        time.sleep(3)
        bird_pos = [150, 450]
        bird_speed = [0, 0]

    # Restart game if all boxes are destroyed
    if not boxes:
        boxes = create_boxes()
        bird_pos = [150, 450]
        bird_speed = [0, 0]
        bird_launched = False

    # Fill the screen with white
    screen.fill(white)
    # Draw the ground
    pygame.draw.rect(screen, black, ground_box)
    # Draw the bird
    screen.blit(bird_image, bird_pos)

    # Draw the boxes
    for box in boxes:
        screen.blit(box_image, box)

    # Draw the slingshot trajectory
    if mouse_start and not bird_launched:
        mouse_current = pygame.mouse.get_pos()
        pygame.draw.line(screen, red, (bird_pos[0] + 25, bird_pos[1] + 25), mouse_current, 5)

    # Draw the restart button
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render('Restart', True, button_text_color)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)
