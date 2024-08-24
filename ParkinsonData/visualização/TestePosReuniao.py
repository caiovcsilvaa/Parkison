import serial
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
porta_serial = 'COM4'
baud_rate = 9600
timeout = 0.1

# Recebimento da porta serial
ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
time.sleep(2)  # Aguarda conexão

# Função para ler os dados do Arduino
def ler_dados_arduino():
    linha = ser.readline().decode('utf-8').strip()
    return linha

# Configuração inicial do gráfico
plt.ion()  # Interatividade
fig, ax = plt.subplots()
sns.set(style="whitegrid")

# Arrays para armazenar os dados
leitura1 = []
leitura2 = []
leitura3 = []

# Função para atualizar o gráfico
def atualizar_grafico():
    # Limpa o gráfico para reescrever novamente
    ax.clear()
    
    # Plota as leituras
    ax.plot(leitura1, label='Leitura 1')
    ax.plot(leitura2, label='Leitura 2')
    ax.plot(leitura3, label='Leitura 3')
    
    ax.set_ylim(bottom=0, top=10000)
    ax.legend(loc='upper right')

    # Adiciona texto com os valores mais recentes na parte superior do gráfico
    ax.text(0.02, 0.95, f'Leitura 1: {leitura1[-1]:.2f}' if leitura1 else 'Leitura 1: N/A', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.90, f'Leitura 2: {leitura2[-1]:.2f}' if leitura2 else 'Leitura 2: N/A', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.85, f'Leitura 3: {leitura3[-1]:.2f}' if leitura3 else 'Leitura 3: N/A', transform=ax.transAxes, verticalalignment='top')

    # Atualiza o gráfico
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