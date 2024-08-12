import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 70, 100
BACKGROUND_COLOR = (0, 128, 0)
CARD_BACK_COLOR = (0, 0, 128)
FPS = 30

# Load images
def load_card_images():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    card_images = {}
    for suit in suits:
        for value in values:
            card_name = f"{value}_of_{suit}"
            image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            image.fill(CARD_BACK_COLOR)
            card_images[card_name] = image
    return card_images

# Setup game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solitaire")
clock = pygame.time.Clock()

# Card setup
deck = load_card_images()
cards = list(deck.keys())
random.shuffle(cards)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw cards (basic)
    for i, card in enumerate(cards[:7]):
        screen.blit(deck[card], (i * (CARD_WIDTH + 10) + 10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
