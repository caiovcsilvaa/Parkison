import serial
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#setup
porta_serial = 'COM5'  
baud_rate = 9600
timeout = 1

#recebimento da porta serial
ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
time.sleep(2)  #aguarda conexão

#função para ler os dados do Arduino
def ler_dados_arduino():
    linha = ser.readline().decode('utf-8').strip()
    return linha

#Configuração inicial do gráfico
plt.ion()  #iteratividade
fig, ax = plt.subplots()
sns.set(style="whitegrid")

#arrays para armazenar os dados
leitura1 = []
leitura2 = []
leitura3 = []

#função para atualizar o gráfico
def atualizar_grafico():
    #atualiza o df
    df = pd.DataFrame({
        'Leitura 1': leitura1[-1:],
        'Leitura 2': leitura2[-1:],
        'Leitura 3': leitura3[-1:]
    })

    #limpa o grafico para reescrever novamente
    ax.clear()

    #Plota o gráfico de barras
    df.plot(kind='bar', ax=ax)
    ax.set_ylim(bottom=0)
    ax.set_xticklabels(['Leituras'])
    ax.legend(['Leitura 1', 'Leitura 2', 'Leitura 3'])

    #Adiciona os valores exatos ao lado das barras
    for i, (val1, val2, val3) in enumerate(zip(leitura1[-1:], leitura2[-1:], leitura3[-1:])):
        ax.annotate(f'({val1:.2f}, {val2:.2f}, {val3:.2f})', xy=(i, max(val1, val2, val3)), xytext=(i, max(val1, val2, val3) + 0.05),
                    ha='center', va='bottom', color='black')

    #Atualiza o gráfico
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)

try:
    while True:
        dados = ler_dados_arduino()
        if dados:
            try:
                valores = list(map(float, dados.split('\t')))
                if len(valores) == 3:
                    leitura1.append(valores[0])
                    leitura2.append(valores[1])
                    leitura3.append(valores[2])

                    # Limita aos últimos 100 valores recebidos
                    if len(leitura1) > 100:
                        leitura1.pop(0)
                        leitura2.pop(0)
                        leitura3.pop(0)

                    # Chama a função para atualizar o gráfico
                    atualizar_grafico()

            except ValueError:
                pass

except KeyboardInterrupt:
    print("Programa interrompido pelo usuário")

finally:
    ser.close()
    plt.ioff()
    plt.show()