import numpy as np
import matplotlib.pyplot as plt

def simulate_queue(lambda_arrival, mu_service1, mu_service2, c1, c2, num_customers):
    np.random.seed(0)  # Para reproducibilidad
    arrival_times = np.cumsum(np.random.exponential(1/lambda_arrival, num_customers))
    start_service1_times = np.zeros(num_customers)
    end_service1_times = np.zeros(num_customers)
    start_service2_times = np.zeros(num_customers)
    end_service2_times = np.zeros(num_customers)

    service1_end_time = np.zeros(c1)
    service2_end_time = np.zeros(c2)
    
    for i in range(num_customers):
        # Cola de degustación
        if i < c1:
            start_service1_times[i] = arrival_times[i]
        else:
            start_service1_times[i] = max(arrival_times[i], min(service1_end_time))
        
        end_service1_times[i] = start_service1_times[i] + np.random.exponential(1/mu_service1)
        service1_end_time[np.argmin(service1_end_time)] = end_service1_times[i]

        # Cola de encuestas
        if i < c2:
            start_service2_times[i] = end_service1_times[i]
        else:
            start_service2_times[i] = max(end_service1_times[i], min(service2_end_time))
        
        end_service2_times[i] = start_service2_times[i] + np.random.exponential(1/mu_service2)
        service2_end_time[np.argmin(service2_end_time)] = end_service2_times[i]
    
    waiting_times1 = start_service1_times - arrival_times
    waiting_times2 = start_service2_times - end_service1_times
    total_times = end_service2_times - arrival_times

    return waiting_times1, waiting_times2, total_times, arrival_times, start_service1_times, end_service1_times, start_service2_times, end_service2_times

# Parámetros del sistema
lambda_arrival = 1 / 3  # Tasa de llegada (clientes por minuto)
mu_service1 = 1 / 4    # Tasa de servicio degustación (clientes por minuto)
mu_service2 = 1 / 5    # Tasa de servicio encuestas (clientes por minuto)
c1 = 2                # Número de estaciones de degustación
c2 = 3                # Número de estaciones de encuestas
num_customers = 1000  # Número de clientes a simular

# Ejecutar la simulación
waiting_times1, waiting_times2, total_times, arrival_times, start_service1_times, end_service1_times, start_service2_times, end_service2_times = simulate_queue(lambda_arrival, mu_service1, mu_service2, c1, c2, num_customers)

# Calcular estadísticas
mean_waiting_time1 = np.mean(waiting_times1)
mean_waiting_time2 = np.mean(waiting_times2)
mean_total_time = np.mean(total_times)
mean_queue_length1 = mean_waiting_time1 * lambda_arrival
mean_queue_length2 = mean_waiting_time2 * lambda_arrival

print(f"Tiempo medio de espera en cola de degustación: {mean_waiting_time1:.2f} minutos")
print(f"Tiempo medio de espera en cola de encuestas: {mean_waiting_time2:.2f} minutos")
print(f"Tiempo medio total en el sistema: {mean_total_time:.2f} minutos")
print(f"Número medio de clientes en cola de degustación: {mean_queue_length1:.2f}")
print(f"Número medio de clientes en cola de encuestas: {mean_queue_length2:.2f}")

# Graficar histogramas
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.hist(waiting_times1, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma de tiempos de espera en cola de degustación')
plt.xlabel('Tiempo de espera (minutos)')
plt.ylabel('Frecuencia')

plt.subplot(1, 3, 2)
plt.hist(waiting_times2, bins=30, color='salmon', edgecolor='black')
plt.title('Histograma de tiempos de espera en cola de encuestas')
plt.xlabel('Tiempo de espera (minutos)')
plt.ylabel('Frecuencia')

plt.subplot(1, 3, 3)
plt.hist(total_times, bins=30, color='lightgreen', edgecolor='black')
plt.title('Histograma de tiempos totales en el sistema')
plt.xlabel('Tiempo total (minutos)')
plt.ylabel('Frecuencia')

#Graficos de lineas
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(np.arange(num_customers), np.cumsum(waiting_times1), label='Cola de degustación')
plt.plot(np.arange(num_customers), np.cumsum(waiting_times2), label='Cola de encuestas')
plt.xlabel('Número de cliente')
plt.ylabel('Tiempo acumulado de espera')
plt.title('Tiempo acumulado de espera por cliente')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(np.arange(num_customers), np.cumsum(total_times))
plt.xlabel('Número de cliente')
plt.ylabel('Tiempo acumulado total')
plt.title('Tiempo acumulado total por cliente')

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

def plot_clients_in_system(arrival_times, start_service1_times, end_service1_times, start_service2_times, end_service2_times):
    times = np.sort(np.concatenate((arrival_times, end_service1_times, end_service2_times)))
    clients_in_system = []

    for t in times:
        in_system = np.sum((arrival_times <= t) & (end_service2_times > t))
        clients_in_system.append(in_system)
    
    # Suavizado con un promedio móvil
    window_size = 50  # Ajusta este valor según sea necesario
    clients_in_system_smooth = np.convolve(clients_in_system, np.ones(window_size)/window_size, mode='valid')
    times_smooth = times[:len(clients_in_system_smooth)]
    
    plt.figure(figsize=(12, 6))
    plt.plot(times_smooth, clients_in_system_smooth, label='Clientes en el sistema (suavizado)')
    plt.xlabel('Tiempo (minutos)')
    plt.ylabel('Número de clientes en el sistema')
    plt.title('Cantidad de clientes en el sistema en función del tiempo')
    plt.legend()
    plt.show()

# Ejecutar gráfico de la cantidad de clientes en el sistema en función del tiempo
plot_clients_in_system(arrival_times, start_service1_times, end_service1_times, start_service2_times, end_service2_times)
