from posible_games import *
import random, csv
from db_poker import *
from concurrent.futures import ProcessPoolExecutor

def create_deck():
    suits = ['C', 'D', 'P', 'T']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    deck = [(suit, rank) for suit in suits for rank in ranks]

    return deck

def simulate_hand(initial_hand, num_players):
    deck = create_deck()  # You need to define a function to create a deck of cards
    my_hand = initial_hand  # Or whatever your actual hand is
    community_cards = []  # Or whatever the actual community cards are

    # Remove your hand and community cards from the deck
    for card in my_hand + community_cards:
        deck.remove(card)

    # Simulate the hands of the other players
    other_hands = []
    for _ in range(num_players - 1):  # One player is you
        hand = random.sample(deck, 2)  # Each player gets 2 cards
        other_hands.append(hand)

        # Remove these cards from the deck
        for card in hand:
            deck.remove(card)

    # Simulate the remaining community cards
    for _ in range(5 - len(community_cards)):  # There are 5 community cards in total
        card = random.choice(deck)
        community_cards.append(card)

        # Remove this card from the deck
        deck.remove(card)

    # Now we compare hands using your hand evaluation function
    my_score = evaluate_complete_hand(my_hand + community_cards)

    # If any other hand has a higher score, you lose
    for hand in other_hands:
        if evaluate_complete_hand(hand + community_cards) > my_score:
            return False

    # If no other hand has a higher score, you win
    return True


def simulate_flop(hand, flop, num_players, num_simulations=10000):
    deck = create_deck()
    # Elimina tus cartas y el flop del mazo.
    for card in hand + flop:
        deck.remove(card)

    num_wins = 0
    for _ in range(num_simulations):
        # Escoge aleatoriamente las dos cartas restantes para el turno y el river.
        remaining_cards = random.sample(deck, 2)
        # Combina tu mano, el flop, y las dos cartas restantes.
        complete_hand = hand + flop + remaining_cards
        complete_hand_value = evaluate_hand(complete_hand)

        # Simula las manos para los otros jugadores y verifica si tu mano es mejor.
        other_hands = [random.sample(deck, 2) + flop + remaining_cards for _ in range(num_players)]
        if all(complete_hand_value >= evaluate_hand(other_hand) for other_hand in other_hands):
            num_wins += 1

    return num_wins / num_simulations

def monte_carlo_simulation(initial_hand, num_players, num_simulations=10000):
    num_wins = 0

    for _ in range(num_simulations):
        if simulate_hand(initial_hand, num_players):
            num_wins += 1

    return num_wins / num_simulations


def simulate_hands():
    # Define the number of players and simulations
    num_players = 3
    num_simulations = 1000
    global_deck = create_deck()
    # Generate all possible 2-card combinations
    initial_hands = [list(hand) for hand in combinations(global_deck, 2)]

    # Filtrar las manos que ya están en la base de datos.
    initial_hands = [hand for hand in initial_hands if
                     not has_hand(f'{hand[0][0]}_{hand[0][1]}', f'{hand[1][0]}_{hand[1][1]}', num_players)]

    data_to_insert = []
    max_rows = 0
    # For each initial hand, compute the win probability and write to CSV
    for hand in initial_hands:
        win_prob = monte_carlo_simulation(hand, num_players, num_simulations)
        data_to_insert.append((f'{hand[0][0]}_{hand[0][1]}', f'{hand[1][0]}_{hand[1][1]}', num_players, win_prob))
        max_rows = max_rows + 1
        if max_rows >= 10:
            max_rows = 0
            insert_into_hand_many(data_to_insert)
            data_to_insert = []
            print(f"termine mano: {hand}")

    if len(data_to_insert) > 0:
        insert_into_hand_many(data_to_insert)



def simulate_flop(hand, flop, num_players, num_simulations=10000):
    deck = create_deck()
    # Elimina tus cartas y el flop del mazo.
    for card in hand + flop:
        deck.remove(card)

    num_wins = 0
    for _ in range(num_simulations):
        # Escoge aleatoriamente las dos cartas restantes para el turno y el river.
        remaining_cards = random.sample(deck, 2)
        # Combina tu mano, el flop, y las dos cartas restantes.
        complete_hand = hand + flop + remaining_cards
        complete_hand_value = evaluate_hand(complete_hand)

        # Simula las manos para los otros jugadores y verifica si tu mano es mejor.
        other_hands = [random.sample(deck, 2) + flop + remaining_cards for _ in range(num_players)]
        if all(complete_hand_value >= evaluate_hand(other_hand) for other_hand in other_hands):
            num_wins += 1

    return num_wins / num_simulations


def flop_init(players, num_simulations):
    deck = create_deck()

    # Genera todas las posibles manos iniciales (combinaciones de 2 cartas).
    initial_hands = [list(hand) for hand in combinations(deck, 2)]

    # Para cada mano inicial, genera todos los posibles flops (combinaciones de 3 cartas del mazo restante).
    for hand in initial_hands[::-1]:
        remaining_deck = [card for card in deck if card not in hand]
        flops = [list(flop) for flop in combinations(remaining_deck, 3)]
        data_to_insert = []
        max_rows = 0
        for flop in flops:
            if not has_flop(f'{hand[0][0]}_{hand[0][1]}', f'{hand[1][0]}_{hand[1][1]}', f'{flop[0][0]}_{flop[0][1]}', f'{flop[1][0]}_{flop[1][1]}', f'{flop[2][0]}_{flop[2][1]}', players):
                win_probability = simulate_flop(hand, flop, players, num_simulations)
                data_to_insert.append(
                    (f'{hand[0][0]}_{hand[0][1]}', f'{hand[1][0]}_{hand[1][1]}',
                     f'{flop[0][0]}_{flop[0][1]}', f'{flop[1][0]}_{flop[1][1]}', f'{flop[2][0]}_{flop[2][1]}',
                     players, win_probability))
                max_rows = max_rows + 1
                if max_rows >= 100:
                    max_rows = 0
                    insert_into_flop_many(data_to_insert)
                    data_to_insert = []
                    print(f"termine hand:{hand} flop: {flop} pro: {win_probability}")

        if len(data_to_insert) > 0:
            insert_into_hand_many(data_to_insert)


flop_init(9, 1000)

#simulate_hands()