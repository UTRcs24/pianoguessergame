import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_COLOR = (200, 200, 200)  # Light gray color for borders
SCREEN_WIDTH = 800 #TO DO: Take up whole screen, not constant.
SCREEN_HEIGHT = 400 #Same as above
WHITE_KEY_WIDTH = 100
WHITE_KEY_HEIGHT = 300
BLACK_KEY_WIDTH = 30
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
    pygame.Rect(WHITE_KEY_WIDTH * 4 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 5 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
    pygame.Rect(WHITE_KEY_WIDTH * 6 - 30, 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
] #MORE BROKEN THAN WHITE KEYS, I THINK

# Function to play the tune
def play_tune(tune):
    for note in tune:
        note.play()
        time.sleep(1)

# Function to check if the player replicated the tune
def check_tune(player_tune, tune):
    return player_tune == tune

# Function to display the Game Over screen
def game_over_screen(message, success):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    # Draw a message based on success or failure
    screen.blit(text, text_rect)

    # Display options to restart or quit
    font = pygame.font.Font(None, 36)
    if success:
        text_restart = font.render("The next digit is: 0 Type Q to Quit", True, WHITE)
    else:
        text_restart = font.render("Press R to Restart or Q to Quit", True, WHITE)

    text_rect = text_restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text_restart, text_rect)

    pygame.display.flip()

    # Wait for player input to either restart or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not success:  # Restart
                    waiting_for_input = False
                    return True #Restarts game by setting game_running to true when function returns
                elif event.key == pygame.K_q:  # Quit
                    return False #Ends game by setting game_running to false when function returns
    return False

# Main game loop
def game_loop():
    one_more_game = True #Keeps track if the user wants to play again.
    clock = pygame.time.Clock()

    # Generate a random melody (sequence of keys)
    melody = [random.choice(list(keys.values())) for _ in range(4)]

    # Display Instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Click the keys in the same order!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    # Wait for player input
    player_tune = []
    game_running = True
    melody_played = False #Keeps track of whether or not the melody's been played.
    while game_running:
        screen.fill((0, 0, 0))
        
        # Draw the piano
        for i in range(len(white_keys)):
            pygame.draw.rect(screen, WHITE, white_keys[i])

            # Draw the border around the white key (slightly smaller)
            border_rect = white_keys[i].inflate(-5, -5)  # Inflate by -5 pixels to create a smaller border
            pygame.draw.rect(screen, BORDER_COLOR, border_rect, 3)  # Draw the border with a width of 3 pixels
        
        for i in range(len(black_keys)):
            pygame.draw.rect(screen, BLACK, black_keys[i])
        
        # Play the melody
        if not melody_played:
            melody_played = True
            play_tune(melody)

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
                        one_more_game = game_over_screen("Correct!", True)
                    else:
                        print("Try again!")
                        one_more_game = game_over_screen("Incorrect", False)
                    game_running = False

        pygame.display.flip()
        clock.tick(FPS)
    if one_more_game:
        game_loop()
    pygame.quit()

# Run the game
game_loop()
    