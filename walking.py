import pgzrun
import pygame
from random import randint

WIDTH = 1200
HEIGHT = 600

# Load images for animation
original_images = [pygame.image.load(f'images/{i}.png') for i in range(1, 6)]
flipped_images = [pygame.transform.flip(img, True, False) for img in original_images]

# Create actors
character = Actor('1')
character.pos = (WIDTH / 2, HEIGHT / 2)


# Create clouds
class Cloud:
    def __init__(self):
        self.x = randint(0, WIDTH)
        self.y = randint(50, 200)
        self.speed = randint(1, 3)
        self.size = randint(30, 60)


clouds = [Cloud() for _ in range(5)]

# Animation and physics variables
current_frame = 0
animation_speed = 0
moving = False
facing_right = True
jump_height = -15
gravity = 0.8
vertical_speed = 0
is_jumping = False
ground_y = HEIGHT / 2  # Original y position

# Background colors for gradient
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (200, 230, 255)


def draw_background():
    # Draw sky gradient
    for y in range(HEIGHT):
        lerp = y / HEIGHT
        color = [int(SKY_TOP[i] + (SKY_BOTTOM[i] - SKY_TOP[i]) * lerp) for i in range(3)]
        pygame.draw.line(screen.surface, color, (0, y), (WIDTH, y))

    # Draw ground
    pygame.draw.rect(screen.surface, (34, 139, 34), (0, HEIGHT / 2, WIDTH, HEIGHT / 2))


def update_clouds():
    for cloud in clouds:
        cloud.x += cloud.speed
        if cloud.x > WIDTH + cloud.size:
            cloud.x = -cloud.size
            cloud.y = randint(50, 200)


def draw_clouds():
    for cloud in clouds:
        pygame.draw.ellipse(screen.surface, (255, 255, 255),
                            (cloud.x, cloud.y, cloud.size * 2, cloud.size))
        pygame.draw.ellipse(screen.surface, (255, 255, 255),
                            (cloud.x + cloud.size * 0.5, cloud.y - cloud.size * 0.2,
                             cloud.size * 1.5, cloud.size * 0.8))


def draw():
    draw_background()
    draw_clouds()

    # Get the current frame's surface
    if facing_right:
        surface = original_images[current_frame]
    else:
        surface = flipped_images[current_frame]

    # Draw the surface at the character's position
    screen.surface.blit(surface,
                        (character.x - surface.get_width() // 2,
                         character.y - surface.get_height() // 2))


def update():
    global current_frame, animation_speed, moving, facing_right, vertical_speed, is_jumping

    update_clouds()
    moving = False

    # Horizontal movement
    if keyboard.right:
        character.x += 5
        facing_right = True
        moving = True
        if character.x >= WIDTH:
            character.x = 0
    elif keyboard.left:
        character.x -= 5
        facing_right = False
        moving = True
        if character.x <= 0:
            character.x = WIDTH

    # Jumping
    if keyboard.space and not is_jumping:
        vertical_speed = jump_height
        is_jumping = True

    # Apply gravity
    if character.y < ground_y or vertical_speed < 0:
        vertical_speed += gravity
        character.y += vertical_speed
    else:
        character.y = ground_y
        vertical_speed = 0
        is_jumping = False

    # Animation
    if moving and not is_jumping:
        animation_speed += 1
        if animation_speed >= 5:
            animation_speed = 0
            current_frame = (current_frame + 1) % len(original_images)
    elif not is_jumping:
        current_frame = 0
        animation_speed = 0


pgzrun.go()