def middle_square(seed: int, iterations = 100, quant_digits = 100):
    results = []
    for _ in range(iterations):
        seed_squared = seed ** 2 
        seed_str = str(seed_squared)
        seed_str = seed_str.zfill(8)
        seed = int(seed_str[2:6])

        for i in range(0,4):
            if len(results) == quant_digits:
                return results
            
            try:
                results.append(int(str(seed)[i]))
                
            except IndexError:
                results.append(0)

    return results
