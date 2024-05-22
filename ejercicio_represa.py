import datetime
from funcs.chi_cuadrado import chi_squared_test
from funcs.congruencial_mixto_alt import congruential_mixed

"""
Nivel máximo de agua soportado por la represa: 45 m
Niveles de activación de las compuertas: 15 m, 25 m, 32 m, 40 m
Altura máxima de la represa: 52 m
Ley de distribución de los incrementos diarios del nivel del lago
"""
"""
Rangos de probabilidad de los incrementos diarios del nivel del lago:
[000 - 036] -3
[037 - 188] -2
[189 - 224] -1
[225 - 605] 0
[606 - 659] 1
[660 - 887] 2
[888- 999] 3
"""


"""
Nivel máximo de agua soportado por la represa: 45 m
Niveles de activación de las compuertas: 15 m, 25 m, 32 m, 40 m
Altura máxima de la represa: 52 m
Ley de distribución de los incrementos diarios del nivel del lago
"""
"""
Rangos de probabilidad de los incrementos diarios del nivel del lago:
[000 - 036] -3
[037 - 188] -2
[189 - 224] -1
[225 - 605] 0
[606 - 659] 1
[660 - 887] 2
[888- 999] 3
"""
import datetime
import plotnine as p9
import pandas as pd

def simular_represa(dias = 10, nivel_del_lago = 10, seed=4443):
    #Se crean los numeros aleatorios mediante congruencial mixto
    print(f'Simulación de la represa durante {dias} días')
    numeros_generados = congruential_mixed(seed = seed, quant_digits=dias*3)
    validacion, _, _ = chi_squared_test(numeros_generados, alpha=0.10)
    
    max_validacion = 1000
    #Se validan los numeros generados mediante chicuadrado
    while not validacion:
        tiempo_actual_microsegundos = datetime.datetime.now().microsecond
        tiempo_actual_microsegundos += seed
        numeros_generados = congruential_mixed(seed = tiempo_actual_microsegundos, quant_digits=dias*4)
        validacion, _, _ = chi_squared_test(numeros_generados)
        max_validacion -= 1
        if max_validacion == 0:
            print("No se pudo validar los números generados")
            break

    #Se declaran variables
    nivel_maximo = 52
    nivel_minimo = 0
    nivel_actual = nivel_del_lago
    nivel_alerta_roja = 45
    niveles_de_agua = []

    compuertas = {
        1: 15,
        2: 25,
        3: 32,
        4: 40
    }

    cantidad_de_veces_compuerta_abierta = {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }

    compuertas_escurrimiento = {
        1: 1,
        2: 2,
        3: 3,
        4: 4
    }
    
    #Metodo de numeros indice
    probabilidades = {
        -3: [0, 36],
        -2: [37, 188],
        -1: [189, 224],
        0: [225, 605],
        1: [606, 659],
        2: [660, 887],
        3: [888, 999]
    }

    contar_alerta_roja = 0
    contar_riesgo_sequia = 0

    #Obtener ultimos 5 digitos de los numeros generados 
    

    #Inicia la simulación
    for i in range(dias):
        probabilidad_obtenida = ""
        
        niveles_de_agua.append(nivel_actual)
        
        #Agarrar 3 digitos de la lista de numeros generados y eliminarlos para obtener nuestros numeros indice
        
        for _ in range(3):
            probabilidad_obtenida += str(numeros_generados.pop(0))
            
        #Se verifica en que rango cae nuestro numero generado "probabilidad_obtenida" y suma el nivel actual del agua
        for key, value in probabilidades.items():
            if int(probabilidad_obtenida) >= value[0] and int(probabilidad_obtenida) <= value[1]:
                nivel_actual += float(key)
                break
            
        if nivel_actual > nivel_maximo:
            nivel_actual = nivel_maximo

        if nivel_actual < nivel_minimo:
            nivel_actual = nivel_minimo

        print(f'Día {i+1}: Nivel del lago: {nivel_actual} m')

        #Se contabilizan cuantas veces se abre cada compuerta y se escurre
        for compuerta in compuertas:
            if nivel_actual >= compuertas[compuerta]:

                cantidad_de_veces_compuerta_abierta[compuerta] += 1
                nivel_actual -= compuertas_escurrimiento[compuerta]


                print(f'Compuerta {compuerta} abierta - Nivel del lago: {nivel_actual} m')
        
        if nivel_actual >= nivel_alerta_roja:
            print('Nivel de alerta roja')
            contar_alerta_roja += 1

        if nivel_actual <= 2:
            print('Riesgo de sequía')
            contar_riesgo_sequia += 1

        if nivel_actual >= nivel_maximo:
            print('La represa ha colapsado')
            break

        if nivel_actual <= nivel_minimo:
            print('El lago se ha secado')
            break
        


    print(f'El nivel de alerta roja se activó {contar_alerta_roja} veces')
    print('Veces que se abrieron las compuertas:')
    for compuerta, veces in cantidad_de_veces_compuerta_abierta.items():
        print(f'Compuerta {compuerta}: {veces} veces')
    
    print(f'El nivel de peligro de sequía se activó {contar_riesgo_sequia} veces')
    
    
    #Grafikitos
    print(len(niveles_de_agua))
    print(len(list(range(1, dias+1))))
    df = pd.DataFrame({
        'Día': list(range(1, len(niveles_de_agua)+1)),
        'Nivel del lago': niveles_de_agua
    })

    p = (p9.ggplot(df) +
            p9.aes(x='Día', y='Nivel del lago') +
            p9.geom_line() +
            p9.geom_point() +
            p9.labs(title='Nivel del lago por día', x='Día', y='Nivel del lago (m)'))
    
    p.show()
    



dias = int(input("Ingrese el número de días que desea simular: "))

nivel_del_lago = int(input("Ingrese el nivel del lago en metros: "))

simular_represa(dias=dias, nivel_del_lago=nivel_del_lago, seed=12344)


