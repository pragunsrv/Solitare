import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 70, 100
CARD_BACK_COLOR = (0, 0, 128)
FPS = 30
FONT_COLOR = (255, 255, 255)

# Colors for suits
SUIT_COLORS = {
    'hearts': (255, 0, 0),
    'diamonds': (255, 0, 0),
    'clubs': (0, 0, 0),
    'spades': (0, 0, 0)
}

# Random background color
BACKGROUND_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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

# Font setup
font = pygame.font.SysFont(None, 36)

# Card setup
deck = load_card_images()
cards = list(deck.keys())
random.shuffle(cards)

# Game state
flipped_cards = [False] * len(cards)
stacks = [[] for _ in range(7)]
foundations = [[] for _ in range(4)]
game_won = False
dragging_card = None
dragging_offset_x = 0
dragging_offset_y = 0

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

    for i, foundation in enumerate(foundations):
        x = WIDTH - (i + 1) * (CARD_WIDTH + 10) - 10
        y = 10
        if foundation:
            screen.blit(deck[foundation[-1]], (x, y))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT))

def draw_text(text, pos):
    text_surface = font.render(text, True, FONT_COLOR)
    screen.blit(text_surface, pos)

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

    value_order = {'A': 1, '2': 2, '3': 3', '4': 4, '5': 5', '6': 6', '7': 7', '8': 8', '9': 9', '10': 10', 'J': 11', 'Q': 12', 'K': 13}

    return color1 != color2 and value_order[value1] == value_order[value2] - 1

def is_valid_foundation_move(card, foundation):
    value = card.split('_')[0]
    suit = card.split('_')[2]
    if not foundation:
        return value == 'A'
    top_card = foundation[-1]
    top_value = top_card.split('_')[0]
    top_suit = top_card.split('_')[2]
    value_order = {'A': 1, '2': 2, '3': 3', '4': 4, '5': 5', '6': 6', '7': 7', '8': 8', '9': 9', '10': 10', 'J': 11', 'Q': 12', 'K': 13}

    return suit == top_suit and value_order[value] == value_order[top_value] + 1

# Auto-move to foundation
def auto_move_to_foundation():
    for i in range(7):
        if stacks[i]:
            card = stacks[i][-1]
            for foundation in foundations:
                if is_valid_foundation_move(card, foundation):
                    foundations[foundations.index(foundation)].append(card)
                    stacks[i].remove(card)
                    break

# Check if the game is won
def check_win():
    return all(len(foundation) == 13 for foundation in foundations)

# Handle drag-and-drop
def handle_drag(pos):
    global dragging_card, dragging_offset_x, dragging_offset_y
    for i in range(7):
        x = i * (CARD_WIDTH + 10) + 10
        y = 50 + len(stacks[i]) * 20
        if dragging_card is None and stacks[i]:
            if x <= pos[0] <= x + CARD_WIDTH and y <= pos[1] <= y + CARD_HEIGHT:
                dragging_card = stacks[i][-1]
                dragging_offset_x = pos[0] - x
                dragging_offset_y = pos[1] - y
                stacks[i].remove(dragging_card)
                break

def handle_drop(pos):
    global dragging_card
    for i in range(7):
        x = i * (CARD_WIDTH + 10) + 10
        if x <= pos[0] <= x + CARD_WIDTH:
            if is_valid_move(dragging_card, stacks[i][-1] if stacks[i] else None):
                stacks[i].append(dragging_card)
                dragging_card = None
                return
    for i in range(4):
        x = WIDTH - (i + 1) * (CARD_WIDTH + 10) - 10
        y = 10
        if x <= pos[0] <= x + CARD_WIDTH and y <= pos[1] <= y + CARD_HEIGHT:
            if is_valid_foundation_move(dragging_card, foundations[i]):
                foundations[i].append(dragging_card)
                dragging_card = None
                return
    stacks[selected_stack].append(dragging_card)
    dragging_card = None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_drop(event.pos)

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw cards
    draw_cards()

    # Auto-move cards to foundation
    auto_move_to_foundation()

    # Draw game status
    if check_win():
        game_won = True
        draw_text("Congratulations! You've won the game!", (200, 300))
        running = False
    else:
        draw_text("Move cards to foundation piles.", (200, 20))

    # Handle dragging
    if dragging_card:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(deck[dragging_card], (mouse_x - dragging_offset_x, mouse_y - dragging_offset_y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
