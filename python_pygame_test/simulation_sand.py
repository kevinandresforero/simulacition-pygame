import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sand PvP Simulation")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
SAND_COLOR = (194, 178, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SPAWN_RATE = 30  # Initial spawn rate

MENU = "menu"
SIMULATION = "simulation"
current_state = MENU
frame_count = 0

particles = []


class SandParticle:
    def __init__(self, x, y, is_enemy=False):
        """
        Initializes a new sand particle.

        Args:
            x (int): The x-coordinate of the particle.
            y (int): The y-coordinate of the particle.
            is_enemy (bool): Flag to determine if the particle is an enemy or player particle.

        Returns:
            None
        """
        self.x = x
        self.y = y
        self.size = 4
        self.settled = False
        self.is_enemy = is_enemy
        self.color = RED if is_enemy else SAND_COLOR

    def can_move_to(self, x, y):
        """
        Checks if a particle can move to the specified position.

        Args:
           x (int): The x-coordinate to check.
           y (int): The y-coordinate to check.

        Returns:
           bool: True if the particle can move to the position, False otherwise.
       """
        if x < 0 or x > WIDTH or y > HEIGHT:
            return False
        for particle in particles:
            if particle != self and abs(particle.x - x) < self.size and abs(particle.y - y) < self.size:
                return False
        return True

    def update(self):
        """
        Updates the particle's position based on available movement options.

        Args:
            None

        Returns:
            None
        """
        if self.settled:
            return

        below = self.y + self.size
        bottom_left = (self.x - self.size, below)
        bottom_right = (self.x + self.size, below)

        if self.can_move_to(self.x, below):
            self.y += 2
        elif self.can_move_to(bottom_left[0], bottom_left[1]):
            self.x -= self.size
            self.y += 2
        elif self.can_move_to(bottom_right[0], bottom_right[1]):
            self.x += self.size
            self.y += 2
        else:
            self.settled = True


def spawn_enemy_particle():
    """
    Spawns an enemy particle at a random x-coordinate at the top of the screen.

    Args:
        None

    Returns:
        None
    """
    x = random.randint(0, WIDTH)
    particles.append(SandParticle(x, 10, is_enemy=True))


def draw_button():
    """
    Draws a "Play" button on the screen in the menu state.

    Args:
        None

    Returns:
        pygame.Rect: The rectangle representing the button's position.
    """
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    pygame.draw.rect(screen, WHITE, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Play", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect


def draw_counters():
    """
    Draws the counters showing the number of player and enemy particles on the screen.

    Args:
        None

    Returns:
        None
    """
    enemy_count = sum(1 for p in particles if p.is_enemy)
    player_count = sum(1 for p in particles if not p.is_enemy)

    font = pygame.font.Font(None, 36)
    enemy_text = font.render(f"Enemy: {enemy_count}", True, RED)
    player_text = font.render(f"Player: {player_count}", True, SAND_COLOR)

    screen.blit(enemy_text, (10, 10))
    screen.blit(player_text, (10, 50))


def adjust_spawn_rate(player_count, enemy_count):
    """
    Adjusts the spawn rate of enemy particles based on the player's particle count compared to the enemy's count.

    Args:
        player_count (int): The number of player particles.
        enemy_count (int): The number of enemy particles.

    Returns:
        None
    """
    global SPAWN_RATE
    # If player count is more than 25% of enemy count, set spawn rate to 20
    if player_count > (enemy_count * 1.25):
        SPAWN_RATE = random.randint(1, 22)
    else:
        if player_count < (enemy_count * 0.80):
            SPAWN_RATE = random.randint(22, 50)


running = True
while running:
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MENU:
                button_rect = draw_button()
                if button_rect.collidepoint(event.pos):
                    current_state = SIMULATION
            elif current_state == SIMULATION:
                x, y = pygame.mouse.get_pos()
                particles.append(SandParticle(x, 10, is_enemy=False))

    if current_state == SIMULATION:
        player_count = sum(1 for p in particles if not p.is_enemy)  # Count player particles
        enemy_count = sum(1 for p in particles if p.is_enemy)  # Count enemy particles
        adjust_spawn_rate(player_count, enemy_count)  # Adjust spawn rate based on player/enemy count

        if frame_count % SPAWN_RATE == 0:
            spawn_enemy_particle()

    screen.fill(BLACK)

    if current_state == MENU:
        draw_button()
    else:
        for particle in particles:
            particle.update()
            pygame.draw.rect(screen, particle.color,
                             (particle.x - particle.size // 2,
                              particle.y - particle.size // 2,
                              particle.size, particle.size))
        draw_counters()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
