import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import pandas as pd

# setup
porta_serial = 'COM4'
baud_rate = 9600
timeout = 1

# recebimento da porta serial
ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
time.sleep(2)  # aguarda conexão

# função para ler os dados do Arduino
def ler_dados_arduino():
    linha = ser.readline().decode('utf-8').strip()
    return linha

# Configuração inicial do gráfico
plt.ion()  # iteratividade
fig, ax = plt.subplots()
sns.set(style="whitegrid")

# arrays para armazenar os dados
leitura1 = []
leitura2 = []
leitura3 = []

# Inicialização das barras
bars = ax.bar([0, 1, 2], [0, 0, 0], color=['blue', 'green', 'red'])
ax.set_ylim(0, 8000)  # Define a escala fixa do eixo y de 0 a 8000
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Leitura 1', 'Leitura 2', 'Leitura 3'])
ax.set_ylabel('Valor')
ax.set_title('Atualização dos Dados em Tempo Real')

# função para atualizar o gráfico
def atualizar_grafico():
    if leitura1 and leitura2 and leitura3:
        # Atualiza as alturas das barras
        valores = [leitura1[-1], leitura2[-1], leitura3[-1]]
        for bar, val in zip(bars, valores):
            bar.set_height(val)

        # Remove textos antigos para evitar sobreposição
        for txt in ax.texts:
            txt.remove()

        # Adiciona os valores exatos ao lado das barras
        for bar, val in zip(bars, valores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                    f'{val:.2f}', ha='center', va='bottom', color='black')

# Função para obter novos dados e animar o gráfico
def animate(frame):
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

                # Atualiza o gráfico
                atualizar_grafico()

        except ValueError:
            pass

ani = FuncAnimation(fig, animate, blit=False, interval=50)

try:
    plt.show(block=True)
except KeyboardInterrupt:
    print("Programa interrompido pelo usuário")
finally:
    ser.close()
    plt.ioff()
    plt.show()