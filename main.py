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

# Game state
stacked_cards = []
flipped_cards = [False] * len(cards)

def draw_cards():
    for i, card in enumerate(cards[:7]):
        if flipped_cards[i]:
            screen.blit(deck[card], (i * (CARD_WIDTH + 10) + 10, 50))
        else:
            pygame.draw.rect(screen, CARD_BACK_COLOR, (i * (CARD_WIDTH + 10) + 10, 50, CARD_WIDTH, CARD_HEIGHT))

# Flip a card
def flip_card(index):
    flipped_cards[index] = not flipped_cards[index]

# Handle clicks
def handle_click(pos):
    for i in range(7):
        x = i * (CARD_WIDTH + 10) + 10
        if x <= pos[0] <= x + CARD_WIDTH and 50 <= pos[1] <= 50 + CARD_HEIGHT:
            flip_card(i)
            break

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw cards
    draw_cards()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
