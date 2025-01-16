

def get_balance(balance_str):
    try:
        # Primero intenta reemplazar el signo de dólar y la coma, y convertir a entero.
        bank_value = balance_str.replace('Pozo:', '').replace('$', '').replace(',', '').strip()
        bank_value = bank_value.split('.')[0]
        bank_value = int(bank_value)
        return bank_value
    except ValueError:
        print(f"balance fallido: {balance_str}")
        return 1

