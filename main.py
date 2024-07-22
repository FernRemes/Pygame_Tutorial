import pygame
import random
import math
# Initialize pygame
pygame.init()

# Set up the window

window_width = 800
window_height = 600
window_title = "Pygame Window"

window = pygame.display.set_mode((window_width, window_height))


playerX = (window_width / 2)- 25
playerY = window_height - 60
player_rect = pygame.Rect(playerX, playerY, 50, 50)
player_speed = 5

# Define enemy
enemy_rects = []
enemy_speedX = []
enemy_speedY = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyX = random.randint(0, 750)
    enemyY = random.randint(25, 200)
    enemy_rects.append(pygame.Rect(enemyX, enemyY, 50, 50))

    enemy_speedX.append(2)
    enemy_speedY.append(25)

# Define bullet

bullet_width = 5
bullet_height = 8
bulletX = 0
bulletY = playerY
bullet_rect = pygame.Rect(bulletX, bulletY, bullet_width, bullet_height)
bullet_speedY = 10

bullet_state = "ready"


# Score
score = 0
font = pygame.font.SysFont("Poppins", 32)

textX = 10
textY = 10

# Game Over
game_over_font = pygame.font.SysFont("Poppins", 64)

def show_score():
    scoreboard = font.render("Score: " + str(score), True, (0,0,0)) 
    window.blit(scoreboard, (textX, textY))

def game_over():
    game_over_text = game_over_font.render("Game Over!", True, (255, 255, 255))
    window.blit(game_over_text, ((window_width - game_over_text.get_width()) // 2, (window_height - game_over_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def player():
    pygame.draw.rect(window, (255, 255, 255), player_rect)

def enemy():
    for enemy_rect in enemy_rects:
        pygame.draw.rect(window, (0, 255, 0), enemy_rect)

def draw_bullet():
    pygame.draw.rect(window, (255, 50, 0), bullet_rect )

def fire_bullet():
    global bulletX, bulletY, bullet_state
    
    bulletX = player_rect.centerx - bullet_width // 2
    bulletY = player_rect.top
    bullet_rect.x = bulletX
    bullet_rect.y = bulletY

    bullet_state = "fire"

def bullet_collision(enemy_rect, bullet_rect):
    return bullet_rect.colliderect(enemy_rect)

def main():
    global enemy_speedX, enemy_speedY, bullet_state, bulletY, score
    # Create a clock object to track time
    clock = pygame.time.Clock()
    # Set up the game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        if keys[pygame.K_UP]:
            player_rect.y -= player_speed

        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        if keys[pygame.K_SPACE] and bullet_state == 'ready':
            fire_bullet()

        if player_rect.left <= 0:
            player_rect.left = 0
        if player_rect.right >= window_width:
            player_rect.right = window_width

        if player_rect.top <= 0:
            player_rect.top = 0
        if player_rect.bottom >= window_height:
            player_rect.bottom = window_height

        # Move the enemy

        for i in range(num_of_enemies):
            # Game over
            if enemy_rects[i].top >= window_height - 25:
                for j in range(num_of_enemies):
                    enemy_rects[j].y = 2000
                game_over()
                break


            enemy_rects[i].x += enemy_speedX[i]

            # Bounce the enemy off the walls
            if enemy_rects[i].left <= 0 or enemy_rects[i].right >= window_width:
                enemy_speedX[i] = -enemy_speedX[i]
                enemy_rects[i].y += enemy_speedY[i]
            
        
            # Collision detection
            if player_rect.colliderect(enemy_rects[i]):
                game_over() 
                running = False

            if bullet_collision(enemy_rects[i], bullet_rect):
                bullet_state = "ready"
                enemy_rects[i].x = random.randint(0, 750)
                enemy_rects[i].y = random.randint(25, 200)
                score += 1
                print(f"Score: {score}")

        # Move the bullet
        if bullet_state == "fire":
            bullet_rect.y -= bullet_speedY
            if bullet_rect.bottom < 0:
                bullet_state = "ready"




        window.fill((0,50,50))
        player()
        enemy()
        show_score()

        if bullet_state == "fire":
            draw_bullet()
        
        
        pygame.display.update()

        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
