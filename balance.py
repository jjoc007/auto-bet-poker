

def get_balance(balance_str):
    try:
        # Primero intenta reemplazar el signo de dólar y la coma, y convertir a entero.
        balance = balance_str.replace('$', '').replace(',', '').replace('K', '00')
        balance = balance.split(".")[0]
        return int(balance)
    except ValueError:
        print(f"balance fallido: {balance_str}")
        return 1

