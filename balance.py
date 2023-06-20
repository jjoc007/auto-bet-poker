

def get_balance(balance_str):
    try:
        # Primero intenta reemplazar el signo de dólar y la coma, y convertir a entero.
        return int(balance_str.replace('$', '').replace(',', ''))
    except ValueError:
        # Si eso falla, entonces el saldo estaba en el formato '$1,7K'.
        # Reemplaza '$' y 'K' con '', convierte el resto en un número decimal,
        # y luego multiplica por 1000 y lo convierte a entero.
        try:
            return int(float(balance_str.replace('$', '').replace('K', '').replace(',', '.')) * 1000)
        except ValueError:
            # Si aún eso falla, entonces retorna el string original.
            return balance_str

