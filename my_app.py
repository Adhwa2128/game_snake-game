import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Font and clock
font = pygame.font.SysFont("comicsans", 35)
clock = pygame.time.Clock()

def draw_snake(snake_blocks):
    for block in snake_blocks:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

def message(text, color, x, y):
    msg = font.render(text, True, color)
    screen.blit(msg, [x, y])

def main():
    # Game variables
    game_over = False
    game_close = False

    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake = [[x, y]]
    snake_length = 1

    fruit_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    fruit_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

    special_fruit_timer = random.randint(10, 20)  # Timer for special fruit
    special_fruit = None

    score = 0
    game_timer = 60  # Set timer for game (in seconds)
    start_time = time.time()

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press R to Restart or Q to Quit", RED, WIDTH // 12, HEIGHT // 3)
            message(f"Your Score: {score}", WHITE, WIDTH // 3, HEIGHT // 2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        main()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_d and dx == 0:
                    dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_w and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_s and dy == 0:
                    dx, dy = 0, BLOCK_SIZE

        # Update snake position
        x += dx
        y += dy
        snake.append([x, y])

        if len(snake) > snake_length:
            del snake[0]

        # Check for collision with itself
        for block in snake[:-1]:
            if block == [x, y]:
                game_close = True

        # Check boundaries
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        # Check fruit collision
        if x == fruit_x and y == fruit_y:
            snake_length += 1
            score += 1
            fruit_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            fruit_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        # Handle special fruit
        if special_fruit:
            if x == special_fruit[0] and y == special_fruit[1]:
                snake_length += 3  # Special fruit effect
                score += 5
                special_fruit = None

        special_fruit_timer -= 1 / FPS
        if special_fruit_timer <= 0 and not special_fruit:
            special_fruit = (
                random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            )
            special_fruit_timer = random.randint(10, 20)

        # Update game timer
        elapsed_time = time.time() - start_time
        if elapsed_time >= game_timer:
            game_close = True

        # Draw everything
        screen.fill((212, 235, 248))
        pygame.draw.rect(screen, RED, (fruit_x, fruit_y, BLOCK_SIZE, BLOCK_SIZE))
        if special_fruit:
            pygame.draw.rect(screen, YELLOW, (special_fruit[0], special_fruit[1], BLOCK_SIZE, BLOCK_SIZE))
        draw_snake(snake)
        message(f"Score: {score}", (10, 57, 129), 10, 10)
        message(f"Time Left: {int(game_timer - elapsed_time)}s", (10, 57, 129), 10, 50)

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
