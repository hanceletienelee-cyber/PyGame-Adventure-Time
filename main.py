import pygame
import math
import random
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# Initialize Pygame
pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Define the colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load the music files
# Initialize Pygame mixer
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Load the game over sound
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")

# Create the bot
class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bot.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.path = []  # List to store the calculated path

    def update(self, maze):
        keys = pygame.key.get_pressed()
        velocity = 5  # Adjust the velocity for bot movement

        if keys[pygame.K_UP]:
            if maze[self.rect.y // 20 - 1][self.rect.x // 20] == 0:
                self.rect.y -= velocity
        if keys[pygame.K_DOWN]:
            if maze[self.rect.y // 20 + 1][self.rect.x // 20] == 0:
                self.rect.y += velocity
        if keys[pygame.K_LEFT]:
            if maze[self.rect.y // 20][self.rect.x // 20 - 1] == 0:
                self.rect.x -= velocity
        if keys[pygame.K_RIGHT]:
            if maze[self.rect.y // 20][self.rect.x // 20 + 1] == 0:
                self.rect.x += velocity

        # Calculate the path for the bot
        self.calculate_path(maze)

    def calculate_path(self, maze):
        # Create a grid representation of the game environment
        grid = Grid(int(window_width / 20), int(window_height / 20))

        # Set the walkable status of each cell in the grid
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    grid.node(x, y).walkable = False

        # Get the current position of the bot and the target (goal)
        start_node = grid.node(int(self.rect.x / 20), int(self.rect.y / 20))
        end_node = grid.node(int(goal.rect.x / 20), int(goal.rect.y / 20))

        # Find the path using A* algorithm
        finder = AStarFinder()
        self.path, _ = finder.find_path(start_node, end_node, grid)


# Create the enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.path = []  # List to store the calculated path
        self.target = target
        self.chasing = True  # Flag to indicate if enemy is chasing the target

    def update(self, maze):
        if self.chasing:
            # Create a grid representation of the game environment
            grid = Grid(int(window_width / 20), int(window_height / 20))

            # Set the walkable status of each cell in the grid
            for y in range(len(maze)):
                for x in range(len(maze[0])):
                    if maze[y][x] == 1:
                        grid.node(x, y).walkable = False

            # Get the current position of the enemy and the target (bot)
            start_node = grid.node(int(self.rect.x / 20), int(self.rect.y / 20))
            end_node = grid.node(int(self.target.rect.x / 20), int(self.target.rect.y / 20))

            # Find the path using A* algorithm
            finder = AStarFinder()
            self.path, _ = finder.find_path(start_node, end_node, grid)

            # Move towards the next node in the calculated path
            if len(self.path) > 1:
                next_node = self.path[1]
                dx = (next_node[0] * 20) - self.rect.x
                dy = (next_node[1] * 20) - self.rect.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                velocity_x = (dx / distance) * self.speed
                velocity_y = (dy / distance) * self.speed
                self.rect.x += velocity_x
                self.rect.y += velocity_y


# Create the goal
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("goal.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create the maze
def create_maze(width, height):
    maze = [[0] * width for _ in range(height)]

    # Generate the maze borders
    for x in range(width):
        maze[0][x] = 1
        maze[height - 1][x] = 1
    for y in range(height):
        maze[y][0] = 1
        maze[y][width - 1] = 1

    # Generate obstacles randomly
    obstacle_count = int((width * height) // 10)  # Adjust the obstacle density as needed
    for _ in range(obstacle_count):
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        maze[y][x] = 1

    return maze


# Initialize the game
maze_width = window_width // 20
maze_height = window_height // 20
maze = create_maze(maze_width, maze_height)

# Create the bot, enemy, and goal objects
bot = Bot(20, 20)
enemy = Enemy(window_width - 40, window_height - 40, bot)
goal = Goal(random.randint(1, maze_width - 2) * 20, random.randint(1, maze_height - 2) * 20)

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(bot, enemy, goal)

# Game loop variables
running = True
game_loop = False  # Set the initial game state to False (menu state)
score = 0
show_path = False

# Main menu loop
while running and not game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_loop = True  # Set the game state to True to start the game

    window.fill(WHITE)
    background_image = pygame.image.load("bg.png")  # Replace "background.png" with the path to your PNG image
    background_rect = background_image.get_rect()
    window.blit(background_image, background_rect)
    pygame.display.flip()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_path = not show_path

    if game_loop:
        window.fill(WHITE)

        # Draw the maze
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    pygame.draw.rect(window, BLUE, (x * 20, y * 20, 20, 20))

        # Update and draw sprites
        all_sprites.update(maze)
        all_sprites.draw(window)

        # Check for collision between bot and goal
        if pygame.sprite.collide_rect(bot, goal):
            score += 1  # Increment score
            goal.rect.x = random.randint(1, maze_width - 2) * 20
            goal.rect.y = random.randint(1, maze_height - 2) * 20
            maze = create_maze(maze_width, maze_height)  # Regenerate maze
            bot.rect.x = 20
            bot.rect.y = 20
            enemy.rect.x = window_width - 40
            enemy.rect.y = window_height - 40

        # Check for collision between bot and enemy
        if pygame.sprite.collide_rect(bot, enemy):
            game_loop = False

        # Show the path if enabled
        if show_path:
            for i in range(len(bot.path) - 1):
                current_node = bot.path[i]
                next_node = bot.path[i + 1]
                x1 = current_node[0] * 20 + 10
                y1 = current_node[1] * 20 + 10
                x2 = next_node[0] * 20 + 10
                y2 = next_node[1] * 20 + 10
                pygame.draw.line(window, GREEN, (x1, y1), (x2, y2), 3)

        pygame.display.flip()
        clock.tick(120)  # Increase the FPS value to 120
    else:
        # Game over screen
        window.fill(RED)
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over! Score: " + str(score), True, WHITE)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        pygame.display.flip()
        # Play the game over sound
        game_over_sound.play()

        # Stop the background music
        pygame.mixer.music.stop()

pygame.quit()
