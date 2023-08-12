import csv
from collections import Counter

from db_poker import *

def get_hand_probability(card_1, card_2, players):
    probability = get_hand(card_1, card_2, players)
    if probability is None:
        probability = get_hand(card_2, card_1, players)

    if probability is not None:
        return probability[3], probability[0], probability[1]
    else:
        return None, None, None
def calculate_flop_pro(c1, c2, c3, c4, c5, p):
    _, c1, c2 = get_hand_probability(c1, c2, p)
    if c1 is None or c2 is None:
        return None

    prob = get_flop(c1, c2, c3, c4, c5, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c3, c5, c4, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c4, c5, c3, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c5, c3, c4, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c5, c4, c3, p)
    if prob is not None:
        return prob[6]

    if prob is None:
        return None




def load_probabilities_from_csv(file_name):
    probabilities = {}
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Asume que las cartas se representan como tuplas
            card1 = row['card_1']  # Convierte la cadena de texto a una tupla
            card2 = row['card_2']  # Convierte la cadena de texto a una tupla
            probabilities[(card1, card2)] = float(row['Win Probability'])
    return probabilities


def determine_player_profile(player_actions_by_phase):
    player_profile = {}

    for phase, player_actions in player_actions_by_phase.items():
        total_actions = len(player_actions)
        action_counts = Counter(player_actions)

        action_percentages = {action: count / total_actions for action, count in action_counts.items()}

        # Profiling players based on their action percentages in each phase
        if action_percentages.get('Retirarse', 0) > 0.3 or action_percentages.get('Pasar', 0) > 0.2 or action_percentages.get('Igualar', 0) > 0.2:
            player_profile[phase] = 'C'
        elif action_percentages.get('Apostar', 0) > 0.2 or action_percentages.get('Subir', 0) > 0.2 or action_percentages.get('Apostar todas', 0) > 0.1:
            player_profile[phase] = 'A'
        else:
            player_profile[phase] = 'E'  # You might want to handle players that do not fall into the aggressive or conservative categories

    return player_profile


def count_profiles(player_actions_by_phase, phase):
    profile_counts = Counter()

    for player_name, actions_by_phase in player_actions_by_phase.items():
        if phase in actions_by_phase:
            # Aquí, estamos pasando una lista de acciones a la función determine_player_profile
            player_profile = determine_player_profile(actions_by_phase)
            profile = player_profile[phase]
            profile_counts[profile] += 1

    # Obtenemos la lista de perfiles y sus cuentas, ordenada por la cuenta
    profile_list = profile_counts.most_common()

    # Si la lista no está vacía, devolvemos el primer elemento, que será el perfil con la mayor cantidad
    if profile_list:
        most_common_profile, count = profile_list[0]
        return most_common_profile

def determine_simple_action(has_raised,  phase, force):
    if phase == 'Pre-Flop':
        if 0 <= force < 0.9:
            return 'fold'
        if 0.9 <= force <= 0.95:
            return 'call'
        if 0.95 <= force <= 1.0:
            return 'bet'
    if phase == 'Flop':
        if 0 <= force < 0.85:
            return 'fold'
        if 0.85 <= force <= 0.95:
            return 'call'
        if 0.95 <= force <= 1.0:
            return 'bet'
    if phase == 'Turn':
        if 0 <= force < 0.85:
            return 'fold'
        if 0.85 <= force <= 0.95:
            return 'call'
        if 0.95 <= force <= 1.0:
            return 'bet'
    if phase == 'River':
        if 0 <= force < 0.85:
            return 'fold'
        if 0.85 <= force <= 0.95:
            return 'call'
        if 0.95 <= force <= 1.0:
            return 'bet'
    return 'fold'


def determine_action(players,  phase, force, percentage_required):
    player_names = []
    for p in players:
        if not p.player.me:
            player_names.append(p.player.name)

    player_actions_by_phase = get_phase_actions_by_players(player_names)
    profile = count_profiles(player_actions_by_phase, phase)
    print(f"profile detected: {profile}")

    if phase == 'Pre-Flop':
        if profile == 'C':
            if 0 <= force < 0.8:
                return 'fold'
            if 0.8 <= force <= 0.9 and percentage_required < 10:
                return 'bet'
            if 0.9 <= force <= 1.0 and percentage_required < 10:
                return 'bet'

        if profile == 'A':
            if 0 <= force < 0.8:
                return 'fold'
            if 0.8 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.9 <= force <= 1.0 and percentage_required < 10 :
                return 'bet'

        if profile == 'E':
            if 0 <= force < 0.8:
                return 'fold'
            if 0.8 <= force <= 0.9 and percentage_required < 10 :
                return 'bet'
            if 0.9 <= force <= 1.0 and percentage_required < 10 :
                return 'bet'

    if phase == 'Flop':
        if profile == 'C':
            if 0 <= force < 0.7:
                return 'fold'

            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 20 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

        if profile == 'A':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 20 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

        if profile == 'E':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

    if phase == 'Turn':
        if profile == 'C':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

        if profile == 'A':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

        if profile == 'E':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

    if phase == 'River':
        if profile == 'C':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

        if profile == 'A':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

        if profile == 'E':
            if 0 <= force < 0.7:
                return 'fold'
            if 0.7 <= force <= 0.9 and percentage_required < 5 :
                return 'bet'
            if 0.7 <= force <= 0.9 and percentage_required < 10 :
                return 'call'
            if 0.7 <= force < 0.9 and percentage_required >= 10 :
                return 'fold'
            if 0.9 <= force <= 1:
                return 'bet'

    return 'fold'
