import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
PLAYER_SIZE = 40
PLAYER_SPEED = 5
ADD_BLOCK_INTERVAL = 5
SPEED_UP_INTERVAL = 10
BLOCK_SIZE_MIN = 20
BLOCK_SIZE_MAX = 50

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
FPS = 60

def get_random_speed(multiplier):
    base_speeds = [-4, -3, -2, 2, 3, 4]
    return random.choice(base_speeds) * multiplier

def add_block(blocks, speed_multiplier):
    size = random.randint(BLOCK_SIZE_MIN, BLOCK_SIZE_MAX)
    x = random.randint(WIDTH // 2, WIDTH - size)
    y = random.randint(HEIGHT // 2, HEIGHT - size)
    dx = get_random_speed(speed_multiplier)
    dy = get_random_speed(speed_multiplier)
    block = {'rect': pygame.Rect(x, y, size, size), 'dx': dx, 'dy': dy}
    blocks.append(block)

def move_player(keys, rect):
    if keys[pygame.K_LEFT] and rect.left > 0:
        rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and rect.right < WIDTH:
        rect.x += PLAYER_SPEED

def move_blocks(blocks):
    for block in blocks:
        rect = block['rect']
        rect.x += block['dx']
        rect.y += block['dy']
        if rect.left <= 0 or rect.right >= WIDTH:
            block['dx'] *= -1
        if rect.top <= 0 or rect.bottom >= HEIGHT:
            block['dy'] *= -1

def check_collision(player, blocks):
    for block in blocks:
        if player.colliderect(block['rect']):
            return True
    return False

def draw_score(score):
    text = font.render(f"Time Survived: {int(score)}s", True, WHITE)
    screen.blit(text, (10, 10))

def show_game_over_screen(score):
    game_over_text = font.render("Game Over!", True, RED)
    final_score_text = font.render(f"You survived for {int(score)} seconds.", True, WHITE)
    prompt_text = font.render("Press R to Restart or any other key to Quit", True, WHITE)

    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                else:
                    return False

def game_loop():
    player = pygame.Rect(WIDTH // 2, HEIGHT - 2*PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
    blocks = []
    speed_multiplier = 1.0
    start_time = time.time()
    last_block_added = start_time
    last_speed_up = start_time

    add_block(blocks, speed_multiplier)

    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_player(keys, player)
        move_blocks(blocks)

        current_time = time.time()
        elapsed_time = current_time - start_time

        if current_time - last_block_added >= ADD_BLOCK_INTERVAL:
            add_block(blocks, speed_multiplier)
            last_block_added = current_time

        if current_time - last_speed_up >= SPEED_UP_INTERVAL:
            speed_multiplier += 0.2
            for block in blocks:
                block['dx'] *= 1.2
                block['dy'] *= 1.2
            last_speed_up = current_time

        draw_score(elapsed_time)

        if check_collision(player, blocks):
            should_restart = show_game_over_screen(elapsed_time)
            if should_restart:
                game_loop()
            else:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, BLUE, player)
        for block in blocks:
            pygame.draw.rect(screen, RED, block['rect'])

        pygame.display.flip()
        clock.tick(FPS)

# Start the first game
game_loop()
