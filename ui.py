import pygame

MAIN_MENU_OPTIONS = ["Start Game", "Settings", "Quit"]

def draw_overlay(screen, screen_width, screen_height, text, subtext=None, color="white"):
    font_large = pygame.font.SysFont("arial", 74)
    font_small = pygame.font.SysFont("arial", 36)
    
    # Main text (centered)
    main_text = font_large.render(text, True, color)
    screen.blit(
        main_text,
        (screen_width // 2 - main_text.get_width() // 2,
         screen_height // 2 - main_text.get_height() // 2)
    )

    # subtext (centered below main text)
    if subtext:
        sub_text = font_small.render(subtext, True, color)
        screen.blit(
            sub_text,
            (screen_width // 2 - sub_text.get_width() // 2,
             screen_height // 2 + main_text.get_height() // 2 + 10)
        )
        
def draw_main_menu(screen, screen_width, screen_height, selected_index=0, mouse_pos=None, MAIN_MENU_OPTIONS=MAIN_MENU_OPTIONS):
    font = pygame.font.SysFont("arial", 48)

    for i, option in enumerate(MAIN_MENU_OPTIONS):
        color = "yellow" if i == selected_index else "white"
        text = font.render(option, True, color)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2,
                           screen_height // 2 - 50 + i * 60))