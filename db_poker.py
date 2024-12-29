import mysql.connector

mydb = mysql.connector.connect(
    host="2.tcp.ngrok.io",
    port=15904,
    user="admin",
    password="12345678",
    database="poker"
)


def get_hand(card_1, card_2, players):
    try:
        cursor = mydb.cursor()
        query = ("SELECT * FROM hand WHERE card_1 = %s AND card_2 = %s AND players = %s")
        cursor.execute(query, (card_1, card_2, players))
        result = cursor.fetchone()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None

def has_hand(card_1, card_2, players):
    try:
        cursor = mydb.cursor()
        query = ("SELECT COUNT(*) FROM hand WHERE card_1 = %s AND card_2 = %s AND players = %s")
        cursor.execute(query, (card_1, card_2, players))
        if cursor.fetchone()[0] > 0:
            print("Record already exists")
            return True
        return False
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def insert_into_hand(card_1, card_2, players, win_probability):
    try:
        cursor = mydb.cursor()

        # Check if the record already exists
        query = ("SELECT COUNT(*) FROM hand WHERE card_1 = %s AND card_2 = %s AND players = %s")
        cursor.execute(query, (card_1, card_2, players))
        if cursor.fetchone()[0] > 0:
            print("Record already exists")
            return

        query = ("INSERT INTO hand "
                 "(card_1, card_2, players, win_probability) "
                 "VALUES (%s, %s, %s, %s)")

        data = (card_1, card_2, players, win_probability)

        cursor.execute(query, data)

        mydb.commit()

        cursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def insert_into_hand_many(data):
    try:
        cursor = mydb.cursor()
        query = ("INSERT INTO hand "
                 "(card_1, card_2, players, win_probability) "
                 "VALUES (%s, %s, %s, %s)")

        cursor.executemany(query, data)
        mydb.commit()

        cursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def get_flop(card_1, card_2, card_3, card_4, card_5, players):
    try:
        cursor = mydb.cursor()
        query = ("SELECT * FROM flop WHERE card_1 = %s AND card_2 = %s AND card_3 = %s AND card_4 = %s AND card_5 = %s AND players = %s")
        cursor.execute(query, (card_1, card_2, card_3, card_4, card_5, players))
        result = cursor.fetchone()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None

def has_flop(card_1, card_2, card_3, card_4, card_5, players):
    try:
        cursor = mydb.cursor()
        query = ("SELECT COUNT(*) FROM flop WHERE card_1 = %s AND card_2 = %s and card_3 = %s AND card_4 = %s AND card_5 = %s AND players = %s")
        cursor.execute(query, (card_1, card_2, card_3, card_4, card_5, players))
        if cursor.fetchone()[0] > 0:
            print("Record already exists")
            return True
        return False
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def insert_into_flop_many(data):
    try:
        cursor = mydb.cursor()
        query = ("INSERT INTO flop "
                 "(card_1, card_2, card_3, card_4, card_5, players, win_probability) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        cursor.executemany(query, data)

        mydb.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def get_player(player_name):
    try:
        cursor = mydb.cursor()
        query = ("SELECT * FROM player WHERE name = %s")
        cursor.execute(query, (player_name, ))
        result = cursor.fetchone()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None


def insert_player(player):
    if get_player(player.name) is None:
        try:
            cursor = mydb.cursor()
            query = ("INSERT INTO poker.player (name) VALUES(%s)")
            cursor.execute(query, (player.name,))
            mydb.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))


def insert_game(game_id, players_information):
    player_1_name = ''
    player_2_name = ''
    player_3_name = ''
    player_4_name = ''
    player_5_name = ''
    player_6_name = ''

    # insertar jugadores
    for p in players_information:
        insert_player(p)

    try:
        cursor = mydb.cursor()

        if len(players_information) > 0:
            player_1_name = players_information[0].name
        if len(players_information) > 1:
            player_2_name = players_information[1].name
        if len(players_information) > 2:
            player_3_name = players_information[2].name
        if len(players_information) > 3:
            player_4_name = players_information[3].name
        if len(players_information) > 4:
            player_5_name = players_information[4].name
        if len(players_information) > 5:
            player_6_name = players_information[5].name

        # Check if the record already exists
        query = ("INSERT INTO poker.game (id, players, player1, player2, player3, player4, player5, player6) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (game_id, len(players_information), player_1_name, player_2_name, player_3_name, player_4_name, player_5_name, player_6_name))
        mydb.commit()

        cursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def has_action(game_id, phase, player_action):
    try:
        cursor = mydb.cursor()
        query = ("SELECT COUNT(*) FROM player_action WHERE game_id = %s AND phase = %s AND player_action = %s AND player_name = %s AND cash = %s AND bet = %s")
        cursor.execute(query, (game_id, phase, player_action.action, player_action.player.name, player_action.actual_cash, player_action.bet_player.bet))
        if cursor.fetchone()[0] > 0:
            return True
        return False
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))



def insert_action(game_id, phase, cards, player_action):

    if has_action(game_id, phase, player_action):
        return

    card_1 = ''
    card_2 = ''
    card_3 = ''
    card_4 = ''
    card_5 = ''

    try:
        cursor = mydb.cursor()

        if len(cards) > 0:
            card_1 = cards[0]
        if len(cards) > 1:
            card_2 = cards[1]
        if len(cards) > 2:
            card_3 = cards[2]
        if len(cards) > 3:
            card_4 = cards[3]
        if len(cards) > 4:
            card_5 = cards[4]

        # Check if the record already exists
        query = ("INSERT INTO poker.player_action (player_name, phase, player_action, game_id, card_1, card_2, card_3, card_4, card_5, cash, position, bet) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
        cursor.execute(query, (player_action.player.name, phase, player_action.action, game_id, card_1, card_2, card_3, card_4, card_5, player_action.actual_cash, player_action.position, player_action.bet_player.bet))
        mydb.commit()

        cursor.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def get_phase_actions_by_players(players_name):
    try:
        formatted_player_names = ', '.join("'" + player + "'" for player in players_name)

        query = f"""
        SELECT player_name, phase, player_action
        FROM player_action
        WHERE player_name IN ({formatted_player_names})
        """
        cursor = mydb.cursor()
        cursor.execute(query)

        player_actions_by_phase = {}

        for player_name, phase, player_action in cursor:
            if player_name not in player_actions_by_phase:
                player_actions_by_phase[player_name] = {}
            if phase not in player_actions_by_phase[player_name]:
                player_actions_by_phase[player_name][phase] = []

            player_actions_by_phase[player_name][phase].append(player_action)

        cursor.close()
        return player_actions_by_phase
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def get_player_profiles(player_names):
    try:
        cursor = mydb.cursor(dictionary=True)
        formatted_player_names = ', '.join("'" + player + "'" for player in player_names)

        query = f"""
        SELECT 
            player_name,
            COUNT(*) AS total_actions,
            SUM(CASE WHEN player_action = 'Retirarse' THEN 1 ELSE 0 END) AS total_folds,
            SUM(CASE WHEN player_action = 'Subir' THEN 1 ELSE 0 END) AS total_raises,
            SUM(CASE WHEN player_action = 'Igualar' THEN 1 ELSE 0 END) AS total_calls,
            AVG(CAST(cash AS UNSIGNED)) AS avg_cash,
            MAX(CAST(cash AS UNSIGNED)) AS max_cash,
            MIN(CAST(cash AS UNSIGNED)) AS min_cash
        FROM 
            player_action
        WHERE 
            player_name IN ({formatted_player_names})
        GROUP BY 
            player_name
        ORDER BY 
            player_name;
        """

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None


def get_game_actions_by_phase(game_id):
    try:
        cursor = mydb.cursor(dictionary=True)

        query = f"""
        SELECT 
            player_name,
            phase,
            player_action,
            cash,
            position
        FROM 
            player_action
        WHERE 
            game_id = %s
            AND player_action <> ''    
        ORDER BY 
            CASE 
                WHEN phase = 'Pre-Flop' THEN 1
                WHEN phase = 'Flop' THEN 2
                WHEN phase = 'Turn' THEN 3
                WHEN phase = 'River' THEN 4
                ELSE 5
            END, 
            player_name;
        """

        cursor.execute(query, (game_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None

def insert_friend_cards(game_id, player_name, card_1, card_2):
    try:
        cursor = mydb.cursor(dictionary=True)
        # Validar que no exista un registro con los mismos datos
        select_query = """
            SELECT COUNT(0) as dup
            FROM friend_cards
            WHERE game_id = %s AND player_name = %s AND card_1 = %s AND card_2 = %s;
        """
        cursor.execute(select_query, (game_id, player_name, card_1, card_2))
        count = cursor.fetchone()

        if count['dup'] != 0:
            print("Registro friend_cards duplicado.")
            return

        # Query de inserción
        insert_query = """
            INSERT INTO friend_cards (game_id, player_name, card_1, card_2)
            VALUES (%s, %s, %s, %s);
        """

        # Ejecutar el query
        cursor.execute(insert_query, (game_id, player_name, card_1, card_2))
        mydb.commit()

        print("insert_friend_cards correctamente.")
    except Exception as e:
        print("Something went wrong: {}".format(e))

def get_friend_cards_by_game(game_id, exclude_player_name):
    try:
        cursor = mydb.cursor(dictionary=True)

        select_query = """
            SELECT card_1, card_2
            FROM friend_cards
            WHERE game_id = %s AND player_name <> %s;
        """

        cursor.execute(select_query, (game_id, exclude_player_name))
        result = cursor.fetchall()

        cards = []
        for row in result:
            cards.append(row['card_1'])
            cards.append(row['card_2'])

        return cards
    except Exception as e:
        print(f"Error al consultar  friend_cards_by_game: {e}")
        return []


