def congruential_multiplicative(seed: int, a = 16807, m = 2147483647 , iterations = 100, quant_digits = 100):
    results = []
    for _ in range(iterations):
        seed = (a * seed) % m

        for i in range(0,4):
            if len(results) == quant_digits:
                return results
            
            try:
                results.append(int(str(seed)[i]))
                
            except IndexError:
                results.append(0)
    return results