def congruential_mixto_decimal(seed: int, a = 1103515245, c = 12345, m= 2**32, n=100):
    """
    Genera una secuencia de números aleatorios decimales utilizando el método de congruencia mixto.

    Args:
    - seed: Semilla inicial para el generador.
    - a: Multiplicador.
    - c: Constante aditiva.
    - m: Módulo.
    - n: Número de valores a generar.

    Returns:
    - Lista de números aleatorios decimales.
    """
    random_numbers = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        random_numbers.append(x / m)  # Normalizando el resultado para obtener números entre 0 y 1
    return random_numbers

def congruential_mixto_decimal_interval(seed: int, intervalo: list, a=1103515245, c=12345, m=2**32, quant_digits=100):
    """
    Genera una secuencia de números aleatorios decimales dentro de un intervalo utilizando el método de congruencia mixto.

    Args:
    - seed: Semilla inicial para el generador.
    - interval: Arreglo de dos números representando el intervalo [a, b].
    - a: Multiplicador.
    - c: Constante aditiva.
    - m: Módulo.
    - n: Número de valores a generar.

    Returns:
    - Lista de números aleatorios decimales dentro del intervalo.
    """
    random_numbers = []
    a_interval, b_interval = intervalo
    for rand in congruential_mixto_decimal(seed, a, c, m, quant_digits):
        random_numbers.append(rand * (b_interval - a_interval) + a_interval)
    return random_numbers