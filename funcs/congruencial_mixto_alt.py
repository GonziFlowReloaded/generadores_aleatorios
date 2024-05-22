import datetime

def congruential_mixed(seed= 15647, quant_digits= 4622, _iterations_=30000):
    # Obtener semilla aleatoria a partir del tiempo actual
    seed += datetime.datetime.now().microsecond
    seed2 = seed ** 2
    # Parámetros para los generadores congruenciales
    a1, c1, m1 = 16807, 0, 2147483647
    a2, c2, m2 = 48271, 0, 2147483647
    a3, c3, m3 = 69621, 0, 2147483647
    a4, c4, m4 = 630360016, 0, 2147483647
    a5, c5, m5 = 421596, 0, 2147483647
    a6, c6, m6 = 685145, 0, 2147483647

    results = []

    for _ in range(_iterations_):
        # Combinar tres generadores congruenciales
        seed = (a1 * seed + c1) % m1
        seed = (a2 * seed + c2) % m2
        seed = (a3 * seed + c3) % m3
        seed = (a4 * seed + c4) % m4
        seed = (a5 * seed + c5) % m5
        seed = (a6 * seed + c6) % m6

        seed2 = (a1 * seed2 + c1) % m1
        seed2 = (a2 * seed2 + c2) % m2
        seed2 = (a3 * seed2 + c3) % m3
        seed2 = (a4 * seed2 + c4) % m4

        # Combinar bits del número generado
        seed ^= (seed >> 13)
        seed ^= (seed << 17)
        seed ^= (seed >> 5)

        seed2 ^= (seed2 >> 13)
        seed2 ^= (seed2 << 17)
        seed2 ^= (seed2 >> 5)

        for digit in str(seed):
            results.append(int(digit))
            if len(results) == quant_digits:
                return results
        for digit in str(seed2):
            results.append(int(digit))
            if len(results) == quant_digits:
                return results


    return results