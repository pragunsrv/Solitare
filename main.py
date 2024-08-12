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

# Colors for suits
SUIT_COLORS = {
    'hearts': (255, 0, 0),
    'diamonds': (255, 0, 0),
    'clubs': (0, 0, 0),
    'spades': (0, 0, 0)
}

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
flipped_cards = [False] * len(cards)
stacks = [[] for _ in range(7)]

# Deal cards into stacks
for i in range(7):
    for j in range(i + 1):
        card = cards.pop()
        stacks[i].append(card)
        flipped_cards[cards.index(card)] = j == i

def draw_cards():
    for i, stack in enumerate(stacks):
        for j, card in enumerate(stack):
            x = i * (CARD_WIDTH + 10) + 10
            y = 50 + j * 20
            if flipped_cards[cards.index(card)]:
                screen.blit(deck[card], (x, y))
            else:
                pygame.draw.rect(screen, CARD_BACK_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT))

# Flip a card
def flip_card(stack_index):
    if stacks[stack_index]:
        card = stacks[stack_index][-1]
        flipped_cards[cards.index(card)] = True

# Check if a move is valid
def is_valid_move(card1, card2):
    if not card2:  # Empty stack, any card can move
        return True
    value1 = card1.split('_')[0]
    value2 = card2.split('_')[0]
    suit1 = card1.split('_')[2]
    suit2 = card2.split('_')[2]
    color1 = SUIT_COLORS[suit1]
    color2 = SUIT_COLORS[suit2]

    value_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}

    return color1 != color2 and value_order[value1] == value_order[value2] - 1

# Handle clicks
selected_card = None
selected_stack = None

def handle_click(pos):
    global selected_card, selected_stack
    for i in range(7):
        x = i * (CARD_WIDTH + 10) + 10
        if x <= pos[0] <= x + CARD_WIDTH:
            if selected_card is None:
                if stacks[i]:
                    selected_card = stacks[i][-1]
                    selected_stack = i
            else:
                if is_valid_move(selected_card, stacks[i][-1] if stacks[i] else None):
                    stacks[i].append(selected_card)
                    stacks[selected_stack].remove(selected_card)
                    selected_card = None
                    selected_stack = None
                else:
                    selected_card = None
                    selected_stack = None
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
