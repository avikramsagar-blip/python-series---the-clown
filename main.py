import pygame
import sys
import random

# --------------------
# Initialize Pygame
# --------------------
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laughing Clown Carnival Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# --------------------
# Colors
# --------------------
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (70, 130, 180)
GREEN = (0, 200, 100)
BLACK = (0, 0, 0)

# --------------------
# Game Variables
# --------------------
BALL_SPEED = 10
clown_health = 5
game_over = False

taunts = [
    "Haha! That tickled!",
    "Is that all you've got?",
    "I didn't feel anything!",
    "Try harder!",
]

# --------------------
# Player
# --------------------
player = pygame.Rect(50, HEIGHT // 2 - 25, 40, 40)

# --------------------
# Clown (Target)
# --------------------
clown = pygame.Rect(700, 200, 80, 120)
clown_speed = 4
direction = 1

# --------------------
# Ball
# --------------------
balls = []

# --------------------
# Functions
# --------------------
def draw_text(text, x, y, color=BLACK):
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))

def reset_game():
    global clown_health, balls, game_over
    clown_health = 5
    balls = []
    game_over = False

# --------------------
# Game Loop
# --------------------
running = True
current_taunt = "Hit the clown!"

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                ball = pygame.Rect(
                    player.x + player.width,
                    player.y + player.height // 2,
                    15, 15
                )
                balls.append(ball)

            if event.key == pygame.K_r and game_over:
                reset_game()

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.y < HEIGHT - player.height:
        player.y += 5

    # Clown Movement
    if not game_over:
        clown.y += clown_speed * direction
        if clown.y <= 50 or clown.y >= HEIGHT - clown.height:
            direction *= -1

    # Ball Movement
    for ball in balls[:]:
        ball.x += BALL_SPEED
        if ball.x > WIDTH:
            balls.remove(ball)

        # Collision
        if ball.colliderect(clown) and not game_over:
            balls.remove(ball)
            clown_health -= 1

            if clown_health > 0:
                current_taunt = random.choice(taunts)
            else:
                current_taunt = "OUCH! You got me!"
                game_over = True

    # --------------------
    # Draw Objects
    # --------------------
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, clown)

    for ball in balls:
        pygame.draw.ellipse(screen, BLACK, ball)

    # UI
    draw_text(f"Clown Health: {clown_health}", 20, 20)
    draw_text(current_taunt, 300, 20, RED)

    if game_over:
        draw_text("🎉 YOU WIN! 🎉", 360, 220, GREEN)
        draw_text("Press R to Restart", 340, 260)

    pygame.display.update()

pygame.quit()
sys.exit()