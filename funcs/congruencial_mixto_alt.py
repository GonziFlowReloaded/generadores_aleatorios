import datetime

def congruential_mixed(seed: int, a=16807, c=32, m=2147483647, iterations=100, quant_digits=123):
    results = []
    for _ in range(iterations):
        seed = (a * seed + c) % m
        seed += datetime.datetime.now().microsecond
  
        for digit in str(seed):
            results.append(int(digit))
            if len(results) == quant_digits:
                return results
            

    return results