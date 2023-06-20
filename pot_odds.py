def is_bet_profitable(pot_size, bet_size, hand_strength, total_players):
    # Calcular las pot odds
    pot_odds = bet_size / (pot_size + bet_size)

    # Estimar las card odds. Supongamos que tienes una mano fuerte (top 10%)
    card_odds = 0.10

    # Ajustar las card odds por la cantidad de jugadores
    card_odds *= total_players

    # Si las pot odds son mayores que las card odds, la apuesta es rentable
    return pot_odds > card_odds