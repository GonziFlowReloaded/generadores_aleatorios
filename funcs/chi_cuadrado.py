import numpy as np
import scipy
def chi_squared_test(numbers: list, num_bins=10, alpha=0.05):
    expected_frequency = len(numbers) / num_bins
    
    # Calcular el histograma de los números generados
    observed_frequency, _ = np.histogram(numbers, bins=num_bins)
    
    # Calcular el estadístico de prueba (chi-cuadrado)
    chi_squared_statistic = np.sum((observed_frequency - expected_frequency) ** 2 / expected_frequency)
    
    # Calcular el valor crítico de chi-cuadrado
    critical_value = scipy.stats.chi2.ppf(1 - alpha, num_bins - 1)
    
    # Comparar el estadístico de prueba con el valor crítico
    if chi_squared_statistic <= critical_value:
        return True, chi_squared_statistic, critical_value
    else:
        return False, chi_squared_statistic, critical_value