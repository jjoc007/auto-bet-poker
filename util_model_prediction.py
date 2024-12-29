from genrative_prediction import *

game_id = 42313636
player_names = ['26998565', 'Aguirruncho']

data = {
    'game_id': game_id,
    'players':  ['26998565', 'Aguirruncho'],
    'phase': 'Turn',
    'big_blind': 200,
    'small_blind':22 / 2,
    'ante':0,
    'm': 16,
    'my_cash': 1000,
    'pot': 3000,
    'required_bet': 400,
    'force': 0.9,
    'my_cards': "C_9, C_A",
    'community_cards': "D_A, P_T, P_2, P_5"
}

action = get_strategy_from_model(data, {})
print(action)