import pygame

pygame.init()

size = [640, 480]
screen = pygame.display.set_mode(size)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

player_x = 50
player_y = 400
player_speed = 5

game_over = False

clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_x += player_speed

    screen.fill(white)
    pygame.draw.rect(screen, red, [player_x, player_y, 50, 50])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()