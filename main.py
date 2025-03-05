import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PLAYER_SIZE = 40
CAR_WIDTH, CAR_HEIGHT = 60, 40
CAR_SPEED = 11  # Car speed
NUM_ROWS = 3  # Number of rows for cars
NUM_CARS_PER_ROW = 2  # Number of cars per row
PLAYER_SPEED = 12  # Increased player speed

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossroad Game")
clock = pygame.time.Clock()

# Font for score and game over text
font = pygame.font.SysFont("Arial", 24)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - PLAYER_SIZE
        self.speed = PLAYER_SPEED  # Increased speed
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - PLAYER_SIZE:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - PLAYER_SIZE:
            self.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

# Car class
class Car:
    def __init__(self, row):
        self.x = random.randint(0, WIDTH - CAR_WIDTH)
        self.y = random.randint(-200, -40) + row * (HEIGHT // NUM_ROWS)
        self.speed = random.randint(CAR_SPEED, CAR_SPEED + 3)  # Randomized speed for variation
    
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-200, -40)
            self.x = random.randint(0, WIDTH - CAR_WIDTH)
            self.speed = random.randint(CAR_SPEED, CAR_SPEED + 3)
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))

# Button class for restarting the game
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 255)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                  self.rect.y + (self.rect.height - text_surface.get_height()) // 2))
    
    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

# Main function
def main():
    player = Player()
    cars = [Car(row) for row in range(NUM_ROWS) for _ in range(NUM_CARS_PER_ROW)]  # Create cars in rows
    score = 0
    game_over = False
    restart_button = Button("Restart", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    
    while True:
        screen.fill(WHITE)
        
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw()
        
        for car in cars:
            car.move()
            car.draw()
            
            # Collision detection
            if pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE).colliderect(
                pygame.Rect(car.x, car.y, CAR_WIDTH, CAR_HEIGHT)):
                game_over = True
        
        # Update score
        if not game_over:
            score += 1
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            # Game Over text
            game_over_text = font.render("Game Over! Click Restart to play again.", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            restart_button.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if restart_button.is_pressed(event.pos):
                    main()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
