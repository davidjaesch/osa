```python
import pygame

# Initialize Pygame
pygame.init()

# Window dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Player properties
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([32, 32])
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_acceleration = 0
        self.gravity = 0.5
        self.friction = 0.1
        self.is_grounded = False

    def update(self):
        # Horizontal movement
        self.x_velocity += self.x_acceleration
        self.x_velocity *= (1 - self.friction)

        # Vertical Movement
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        # Ground collision
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.y_velocity = 0
            self.is_grounded = True
        else:
            self.is_grounded = False


        self.rect.x += self.x_velocity

    def move_left(self):
        self.x_acceleration = -0.5

    def move_right(self):
        self.x_acceleration = 0.5

    def stop_moving(self):
        self.x_acceleration = 0

    def jump(self):
      if self.is_grounded:
        self.y_velocity = -10


# Player instance
player = Player(50, height - 50)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_SPACE:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.x_acceleration < 0:
                player.stop_moving()
            if event.key == pygame.K_RIGHT and player.x_acceleration > 0:
                player.stop_moving()

    # Update
    player.update()

    # Draw
    screen.fill(black)
    pygame.draw.rect(screen, (0,255,0), (0, height - 20, width, 20))
    screen.blit(player.image, player.rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
```