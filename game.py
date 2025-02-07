import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
WHITE_KEY_WIDTH = 100
WHITE_KEY_HEIGHT = 300
BLACK_KEY_WIDTH = 60
BLACK_KEY_HEIGHT = 200
FPS = 60

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Piano Melody Game")

# Load sounds for the keys (assumes sound files are available)
C4 = pygame.mixer.Sound("C4.wav")
D4 = pygame.mixer.Sound("D4.wav")
E4 = pygame.mixer.Sound("E4.wav")
F4 = pygame.mixer.Sound("F4.wav")
G4 = pygame.mixer.Sound("G4.wav")
A4 = pygame.mixer.Sound("A4.wav")
B4 = pygame.mixer.Sound("B4.wav")

# Define keys mapping
keys = {
    pygame.K_a: C4,
    pygame.K_s: D4,
    pygame.K_d: E4,
    pygame.K_f: F4,
    pygame.K_g: G4,
    pygame.K_h: A4,
    pygame.K_j: B4
}

# Piano keys
white_keys = [
    pygame.Rect(0, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 2, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 3, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 4, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 5, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 6, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT)
]

black_keys = [
    pygame.Rect(WHITE_KEY_WIDTH - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 2 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 3 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 5 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 6 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
]

# Function to play the tune
def play_tune(tune):
    for note in tune:
        note.play()
        time.sleep(0.5)

# Function to check if the player replicated the tune
def check_tune(player_tune, tune):
    return player_tune == tune

# Main game loop
def game_loop():
    clock = pygame.time.Clock()

    # Generate a random melody (sequence of keys)
    melody = [random.choice(list(keys.values())) for _ in range(4)]

    # Display Instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Click the keys in the same order!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    # Play the melody
    play_tune(melody)

    # Wait for player input
    player_tune = []
    game_running = True
    while game_running:
        screen.fill((0, 0, 0))

        # Draw the piano
        for i, key in enumerate(white_keys):
            pygame.draw.rect(screen, WHITE, key)
            if i < len(black_keys):
                pygame.draw.rect(screen, BLACK, black_keys[i])

        # Draw instructions
        screen.blit(text, text_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check which key was clicked
                for i, key in enumerate(white_keys):
                    if key.collidepoint(mouse_x, mouse_y):
                        keys[list(keys.keys())[i]].play()  # Play the sound of the clicked key
                        player_tune.append(keys[list(keys.keys())[i]])

                # Check if the player completed the tune
                if len(player_tune) == len(melody):
                    if check_tune(player_tune, melody):
                        print("You replicated the tune!")
                    else:
                        print("Try again!")
                    game_running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the game
game_loop()
    