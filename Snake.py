import pygame
import random

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

score = 0
level = 1
fruit_eaten = False
speed = 120 

head_square = [100, 100]
squares = [
    [30, 100], [40, 100], [50, 100], [60, 100],
    [70, 100], [80, 100], [90, 100], [100, 100]
]

def generate_fruit():
    while True:
        fr_x = random.randrange(0, width // 10) * 10
        fr_y = random.randrange(0, height // 10) * 10
        if [fr_x, fr_y] not in squares:  # Fruit cannot appear in snake
            return [fr_x, fr_y]

fruit_coor = generate_fruit()

direction = "right"
next_dir = "right"
done = False

def game_over():
    global done
    font = pygame.font.SysFont("times new roman", 45)
    text = font.render(f"Game Over! Score: {score}, Level: {level}", True, (255, 0, 0)) #just text of score and level in the corner
    rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"
    
    for square in squares[:-1]:
        if head_square == square:
            game_over()
    
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"

    # teleporting
    if direction == "right":
        head_square[0] = (head_square[0] + 10) % width
    if direction == "left":
        head_square[0] = (head_square[0] - 10) % width
    if direction == "up":
        head_square[1] = (head_square[1] - 10) % height
    if direction == "down":
        head_square[1] = (head_square[1] + 10) % height

    new_square = head_square[:]
    squares.append(new_square)
    squares.pop(0)

    if head_square == fruit_coor:
        fruit_eaten = True
        score += 10
        squares.insert(0, squares[0][:])  # growing up
        
        #higher difficult
        if score % 30 == 0:
            level += 1
            speed = max(50, speed - 10)  #more speed

    if fruit_eaten:
        fruit_coor = generate_fruit()
        fruit_eaten = False

    screen.fill((0, 0, 0))
    #Counters of score and level
    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.draw.circle(screen, (0, 255, 0), (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)

    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()
    pygame.time.delay(speed)

pygame.quit()
