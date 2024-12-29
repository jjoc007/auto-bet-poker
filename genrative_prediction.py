from ollama import Client
from db_poker import *
import datetime
import google.generativeai as genai
import os


def load_prompt_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def format_prompt(template, data):
    return template.format(
        player_profiles=data['player_profiles'],
        game_actions=data['game_actions'],
        game_id=data['game_id'],
        phase=data['phase'],
        my_cards=data['my_cards'],
        community_cards=data['community_cards'],
        my_cash=data['my_cash'],
        big_blind=data['big_blind'],
        small_blind=data['small_blind'],
        ante=data['ante'],
        pot=data['pot'],
        required_bet=data['required_bet'],
        m=data['m'],
        force=data['force'],
        game_information=data['game_information'],
    )

# Función para guardar el prompt y la respuesta
def save_prompt_and_response(prompt, response):
    # Generar un nombre de archivo con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato: YYYYMMDD_HHMMSS
    filename = f"ollama_responses/{timestamp}.txt"

    # Escribir el prompt y la respuesta en el archivo
    with open(filename, "w") as file:
        file.write("### Prompt ###\n")
        file.write(prompt + "\n\n")
        file.write("### Response ###\n")
        file.write(response)

    print(f"Prompt and response saved to {filename}")


def send_to_google(prompt):
    genai.configure(api_key=os.environ.get('G_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    # save_prompt_and_response(prompt, response.text)
    return response.text.replace("\n", "")

def send_to_ollama(prompt):
    client = Client(
        host='http://192.168.10.14:11435'
    )
    options = {
        "stop": ["User:", "Assistant:"],  # Define las palabras o tokens donde detener la generación.
        "temperature": 0.6,  # Controla la creatividad del modelo (valores bajos = respuestas más deterministas).
        "top_p": 0.8
    }
    response = client.generate(model='llama3.2', prompt=prompt)
    save_prompt_and_response(prompt, response.response)
    return response.response

def get_strategy_from_model(data, t_info):
    profiles = get_player_profiles(data['players'])
    actions = get_game_actions_by_phase(data['game_id'])

    profiles_prompt = ''
    actions_prompt = ''

    for profile in profiles:
        profiles_prompt += (
            f"- {profile['player_name']}:\n"
            f"  - Total actions: {profile['total_actions']}\n"
            f"  - Folds: {profile['total_folds']}, Raises: {profile['total_raises']}, Calls: {profile['total_calls']}\n"
            f"  - Cash avg: {profile['avg_cash']}, Máx: {profile['max_cash']}, Mín: {profile['min_cash']}\n"
        )

    for action in actions:
        actions_prompt += (
            f"- player: {action['player_name']}, phase: {action['phase']}, action: {action['player_action']}, "
            f"Cash: {action['cash']} \n"
        )

    game_info_prompt = ''
    for key, value in t_info.items():
        game_info_prompt += f"- {key.replace('_', ' ').capitalize()}: {value}\n"

    template_path = "prompt/cash.txt"
    template = load_prompt_template(template_path)

    data['player_profiles'] = profiles_prompt
    data['game_actions'] = actions_prompt
    data['game_information'] = game_info_prompt

    final_prompt = format_prompt(template, data)

    action = send_to_google(final_prompt)
    if action not in ['fold', 'call', 'raise', 'bet']:
        print(f'invalid action : {action}')
        return 'fold'
    else:
        return action
