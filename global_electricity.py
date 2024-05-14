import datetime

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

def get_numeros_indices(probabilidad):
    numero = str(probabilidad)

    numeros_despues_del_punto = numero.split(".")[1]

    maximo = ""
    for i in range(len(numeros_despues_del_punto)):
        maximo += "9"
    
    maximo = int(maximo)
    rangos = {
        "defectuoso": [0, int(numeros_despues_del_punto)-1],
        "no_defectuoso": [int(numeros_despues_del_punto), maximo]
    }

    return rangos, maximo 







"""
Contexto:
La empresa “Global Electronic" se dedica a la fabricación de placas de video de alta calidad para computadoras. Para garantizar la calidad de sus productos, la empresa implementa un riguroso proceso de control de calidad que incluye la inspección de una muestra aleatoria de placas de video de cada lote producido.
Se desea desarrollar un modelo de simulación que permita evaluar la efectividad del proceso de control de calidad en la fábrica de placas de video. El modelo debe considerar los siguientes aspectos ingresados por el encargado de fábrica, basándose en datos históricos de producción:
•	Probabilidad de defecto en la producción (p= x): Probabilidad de que una placa de video producida sea defectuosa. (ej. Rango de defectuosas 0-7defectuosas por lote)
•	Tamaño de la muestra de control (n): Número de placas de video seleccionadas aleatoriamente para su inspección.
•	Límite de aceptación (a): Valor máximo de proporción de placas defectuosas en la muestra para que el lote sea aprobado. (establecido por la empresa según sus estándares, ej. 5 defectuosas en 100)

"""

def simulador_lote(p, n, a, seed=12344):

    rangos_probabilidad, maximo = get_numeros_indices(p)
    
    # print(rangos_probabilidad)
    # print(maximo)

    defectuosas = 0
    no_defectuosas = 0

    numeros_generados = congruential_mixed(seed = seed, quant_digits=n*len(str(maximo))*2)
    validacion, _, _ = chi_squared_test(numeros_generados)

    while not validacion:
        seed = seed + 1
        numeros_generados = congruential_mixed(seed = seed, quant_digits=n*len(str(maximo))*2)
        validacion, _, _ = chi_squared_test(numeros_generados)


    #Funcionamiento de la simulación
        
    
    for i in range(n):
        numero = ""
        for _ in range(0, len(str(maximo))):
            numero += str(numeros_generados.pop(0))
        numero = int(numero)
            

        # print(numero)
        if numero >= rangos_probabilidad["defectuoso"][0] and numero <= rangos_probabilidad["defectuoso"][1]:
            defectuosas += 1
        else:
            no_defectuosas += 1
        
    if defectuosas <= a:
        print(f"El lote ha sido aprobado")
        print(f"Placas defectuosas: {defectuosas}")
        print(f"Placas no defectuosas: {no_defectuosas}")
        print(f"Proporción de placas defectuosas: {(defectuosas/n)*100}%")
        return True, defectuosas, no_defectuosas
    else:
        print(f"El lote ha sido rechazado")
        print(f"Placas defectuosas: {defectuosas}")
        print(f"Placas no defectuosas: {no_defectuosas}")
        print(f"Proporción de placas defectuosas: {(defectuosas/n)*100}%")
        return False, defectuosas, no_defectuosas

# global_electricity(p=0.23123123, n=100, a=20, seed=333)

import pandas as pd
import plotnine as p9


# simulador_lote(p=p, n=n, a=a, seed=333)

def simulador_global_electricity(cantidad_lotes):
    lotes = []

    print("Ingresar los valores de p, n y a para la simulación de la fábrica de placas de video")
    p = float(input("Probabilidad de placa grafica defectuosa (En decimales): "))
    n = int(input("Tamaño de la muestra de control: "))
    a = int(input("Límite de aceptación (Del tamaño de la muestra actual): "))

    for i in range(cantidad_lotes):
        lotes.append(simulador_lote(p=0.23, n=60, a=15, seed=333))

    lotes = pd.DataFrame(lotes, columns=["Aprobado", "Placas defectuosas", "Placas no defectuosas"])
    print(lotes)
    print(lotes["Aprobado"].value_counts())
    print(lotes["Aprobado"].value_counts(normalize=True))
    print(lotes["Placas defectuosas"].mean())
    print(lotes["Placas no defectuosas"].mean())

    grafico_aprobacion = (
        p9.ggplot(lotes) +
        p9.aes(x="Aprobado") +
        p9.geom_bar() +
        p9.labs(title="Aprobación de lotes de placas de video", x="Aprobado", y="Cantidad de lotes") +
        p9.theme_538()
    )

    grafico_defectuosas = (
        p9.ggplot(lotes) +
        p9.aes(x=lotes.index, y="Placas defectuosas") +
        p9.geom_bar(stat="identity") +
        p9.geom_point() +
        p9.geom_line() +
        p9.labs(title="Cantidad de placas defectuosas por lote", x="Lote", y="Cantidad de placas defectuosas") +
        p9.theme_538()
    )

    print(grafico_aprobacion)
    print(grafico_defectuosas)

    
simulador_global_electricity(10)

# simulador_lote(p=0.23123123, n=100, a=20, seed=333)
