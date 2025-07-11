import pygame

def draw_menu(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Main Menu", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
    screen.blit(text, text_rect)
    
    start_text = font.render("Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(start_text, start_rect)

    quit_text = font.render("Quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() * 3 // 4))
    screen.blit(quit_text, quit_rect)
    
    return start_rect, quit_rect

def handle_menu_input(event, start_rect, quit_rect):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_rect.collidepoint(event.pos):
            return "start"
        elif quit_rect.collidepoint(event.pos):
            return "quit"
    return None