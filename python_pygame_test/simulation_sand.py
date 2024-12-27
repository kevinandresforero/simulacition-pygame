import pygame
import random
import sys

# Initialize Pygame and set up the display window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sand Simulation")
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
SAND_COLOR = (194, 178, 128)
BLACK = (0, 0, 0)

# Game states
MENU = "menu"
SIMULATION = "simulation"
current_state = MENU

# List to store all sand particles
particles = []


class SandParticle:
    """
    Represents a single particle of sand in the simulation.
    Each particle can fall and slide based on surrounding particles.
    """

    def __init__(self, x, y):
        """
        Initialize a new sand particle.

        Args:
            x (int): Initial x-coordinate
            y (int): Initial y-coordinate

        Returns:
            None
        """
        self.x = x
        self.y = y
        self.size = 4
        self.settled = False

    def can_move_to(self, x, y):
        """
        Check if the particle can move to a new position.

        Args:
            x (int): Target x-coordinate
            y (int): Target y-coordinate

        Returns:
            bool: True if movement is possible, False otherwise
        """
        # Check screen boundaries
        if x < 0 or x > WIDTH or y > HEIGHT:
            return False

        # Check collision with other particles
        for particle in particles:
            if particle != self and abs(particle.x - x) < self.size and abs(particle.y - y) < self.size:
                return False
        return True

    def update(self):
        """
        Update particle position based on physics rules.
        Particles can fall straight down or slide diagonally if blocked.

        Args:
            None

        Returns:
            None
        """
        if self.settled:
            return

        # Calculate potential movement positions
        below = self.y + self.size
        bottom_left = (self.x - self.size, below)
        bottom_right = (self.x + self.size, below)

        # Try to move in priority order: down, diagonal left, diagonal right
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


def draw_button():
    """
    Draw the play button in the menu state.

    Args:
        None

    Returns:
        pygame.Rect: Rectangle object representing button boundaries
    """
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    pygame.draw.rect(screen, WHITE, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Play", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MENU:
                # Check for play button click
                button_rect = draw_button()
                if button_rect.collidepoint(event.pos):
                    current_state = SIMULATION
            elif current_state == SIMULATION:
                # Create new sand particle on click
                x, y = pygame.mouse.get_pos()
                particles.append(SandParticle(x, 10))

    # Clear screen
    screen.fill(BLACK)

    # Draw current state
    if current_state == MENU:
        draw_button()
    else:
        # Update and draw all particles
        for particle in particles:
            particle.update()
            pygame.draw.rect(screen, SAND_COLOR,
                             (particle.x - particle.size // 2,
                              particle.y - particle.size // 2,
                              particle.size, particle.size))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()