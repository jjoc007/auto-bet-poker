from db_poker import *
from probabilities import *

player_actions_by_phase = get_phase_actions_by_players(['JOMAC', 'Oscarros'])


for player_name, actions_by_phase in player_actions_by_phase.items():
    player_profile = determine_player_profile(actions_by_phase)
    print(f"Perfil de {player_name}: {player_profile}")


# Usar la función para contar los perfiles en una fase específica
phase = 'Flop'
profile = count_profiles(player_actions_by_phase, phase)
print(f"Conteos de perfiles : {profile}")