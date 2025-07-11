import pygame
import menu

pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Game state
game_state = "menu"
start_rect = None
quit_rect = None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "menu":
            action = menu.handle_menu_input(event, start_rect, quit_rect)
            if action == "start":
                game_state = "game"
            elif action == "quit":
                running = False
                
    # Clear the screen
    screen.fill((0, 0, 0))
    
    if game_state == "menu":
        start_rect, quit_rect = menu.draw_menu(screen)
    elif game_state == "game":
        font = pygame.font.Font(None, 36)
        text = font.render("Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
    
    # Update display
    pygame.display.flip()

pygame.quit()