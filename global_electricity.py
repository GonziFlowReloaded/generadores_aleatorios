from funcs.chi_cuadrado import chi_squared_test
from funcs.congruencial_mixto_alt import congruential_mixed

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

    #En base a la probabilidad dada, se generan los numeros indices y se obtiene el maximo
    rangos_probabilidad, maximo = get_numeros_indices(p)
    
    
    #Se inicializan variables
    defectuosas = 0
    no_defectuosas = 0

    #Generación de numeros aleatorios
    numeros_generados = congruential_mixed(seed = seed, quant_digits=n*len(str(maximo))*2)
    validacion, _, _ = chi_squared_test(numeros_generados)

    #Bucle de validación
    while not validacion:
        seed = seed + 1
        numeros_generados = congruential_mixed(seed = seed, quant_digits=n*len(str(maximo))*2)
        validacion, _, _ = chi_squared_test(numeros_generados)

    #Funcionamiento de la simulación
    for i in range(n):
        numero = ""

        #Generación de nuestra muestra artificial
        for _ in range(0, len(str(maximo))):
            numero += str(numeros_generados.pop(0))
        numero = int(numero)
            
        #Suma si es defectuosa o no defectuosa
        if numero >= rangos_probabilidad["defectuoso"][0] and numero <= rangos_probabilidad["defectuoso"][1]:
            defectuosas += 1
        else:
            no_defectuosas += 1
        
    if defectuosas <= a:
        # print(f"El lote ha sido aprobado")
        # print(f"Placas defectuosas: {defectuosas}")
        # print(f"Placas no defectuosas: {no_defectuosas}")
        # print(f"Proporción de placas defectuosas: {(defectuosas/n)*100}%")
        return True, defectuosas, no_defectuosas
    else:
        # print(f"El lote ha sido rechazado")
        # print(f"Placas defectuosas: {defectuosas}")
        # print(f"Placas no defectuosas: {no_defectuosas}")
        # print(f"Proporción de placas defectuosas: {(defectuosas/n)*100}%")
        return False, defectuosas, no_defectuosas

# global_electricity(p=0.23123123, n=100, a=20, seed=333)

import pandas as pd
import plotnine as p9


# simulador_lote(p=p, n=n, a=a, seed=333)

def simulador_global_electricity(cantidad_lotes):
    lotes = []

    #Ingreso de datos
    print("Ingresar los valores de p, n y a para la simulación de la fábrica de placas de video")
    p = float(input("Probabilidad de placa grafica defectuosa (En decimales): "))
    n = int(input("Tamaño de la muestra de control: "))
    a = int(input("Límite de aceptación (Del tamaño de la muestra actual): "))

    #Bucle de simulación
    for i in range(cantidad_lotes):
        lotes.append(simulador_lote(p=p, n=n, a=a, seed=333))

    #Se convierte a dataframe
    lotes = pd.DataFrame(lotes, columns=["Aprobado", "Placas defectuosas", "Placas no defectuosas"])
    print(lotes)
    print(lotes["Aprobado"].value_counts())
    print(lotes["Aprobado"].value_counts(normalize=True))
    print(lotes["Placas defectuosas"].mean())
    print(lotes["Placas no defectuosas"].mean())

    #Gráficos
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
        # p9.geom_point() +
        p9.geom_smooth() +  # Se añade esta línea para obtener una línea suavizada
        p9.labs(title="Cantidad de placas defectuosas por lote", x="Lote", y="Cantidad de placas defectuosas") +
        p9.theme_538()
    )

    grafico_aprobacion.show()
    grafico_defectuosas.show()
    print("Cantidad de lotes aprobados: ", lotes["Aprobado"].value_counts()[True])
    print("Cantidad de lotes rechazados: ", lotes["Aprobado"].value_counts()[False])
    print("Proporción de lotes aprobados: ", lotes["Aprobado"].value_counts(normalize=True)[True])
    print("Proporción de lotes rechazados: ", lotes["Aprobado"].value_counts(normalize=True)[False])
    print("Porcentaje de placas no defectuosas promedio por lote: ")
    print(lotes["Placas no defectuosas"].mean())
    print("Porcentaje de placas defectuosas promedio por lote")
    print(lotes["Placas defectuosas"].mean())




print("Simulador de fábrica de placas de video")
cantidad_lotes = int(input("Ingrese la cantidad de lotes a simular: "))
simulador_global_electricity(cantidad_lotes)

# simulador_lote(p=0.23123123, n=100, a=20, seed=333)
