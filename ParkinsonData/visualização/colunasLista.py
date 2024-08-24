#esse foi o primeiro de todos, parti desse princípio, pode ser descartado.

import serial
import time
import matplotlib.pyplot as plt
import seaborn as sns

#setup 
porta_serial = 'COM4'  
baud_rate = 9600
timeout = 1

#aceita a conexão
ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
time.sleep(2)  

#ler os dados recebidos e transforma em string
def ler_dados_arduino():
    linha = ser.readline().decode('utf-8').strip()
    return linha

#Configuração do gráfico
plt.ion()  #ativa o modo interativo
fig, ax = plt.subplots()
sns.set(style="whitegrid")

#Configurações iniciais do gráfico de barras
labels = ['Leitura 1', 'Leitura 2', 'Leitura 3']
valores = [0, 0, 0]
barras = ax.bar(labels, valores, color=['blue', 'green', 'red'])

#Define o limite inicial do eixo y
ax.set_ylim(0, 1)

try:
    while True:
        dados = ler_dados_arduino()
        if dados:
            try:
                valores = list(map(float, dados.split('\t')))
                if len(valores) == 3:
                    #Atualização do gráfico de barras - apenas a altura
                    for bar, val in zip(barras, valores):
                        bar.set_height(val)
                    
                    #Ajusta dinamicamente o limite superior do eixo y
                    ax.set_ylim(0, max(valores))
                    
                    plt.pause(0.01)
            except ValueError:
                pass

except KeyboardInterrupt:
    print("Programa interrompido pelo usuário")

finally:
    ser.close()
    plt.ioff()
    plt.show()