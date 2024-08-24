import serial
import time
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

#Configuração inicial do Tkinter
root = tk.Tk()
root.title("Interface de Coleta de Dados do Arduino")

#Variáveis de controle
gravando = False
status_conexao = tk.StringVar(value="Desconectado")

#Setup da porta serial
porta_serial = 'COM4'
baud_rate = 9600
timeout = 0.1

#Configuração inicial do Matplotlib
plt.ion()
fig, ax = plt.subplots()
sns.set(style="whitegrid")

#Arrays para armazenar os dados
leitura1 = []
leitura2 = []
leitura3 = []

#Função para ler os dados do Arduino
def ler_dados_arduino():
    if ser.is_open:
        linha = ser.readline().decode('utf-8').strip()
        return linha
    else:
        return None

#Função para atualizar o gráfico
def atualizar_grafico():
    ax.clear()
    ax.plot(leitura1, label='Leitura 1')
    ax.plot(leitura2, label='Leitura 2')
    ax.plot(leitura3, label='Leitura 3')
    
    ax.set_ylim(bottom=0, top=10000)
    ax.legend(loc='upper right')

    if leitura1:
        ax.text(0.02, 0.95, f'Leitura 1: {leitura1[-1]:.2f}', transform=ax.transAxes, verticalalignment='top')
    if leitura2:
        ax.text(0.02, 0.90, f'Leitura 2: {leitura2[-1]:.2f}', transform=ax.transAxes, verticalalignment='top')
    if leitura3:
        ax.text(0.02, 0.85, f'Leitura 3: {leitura3[-1]:.2f}', transform=ax.transAxes, verticalalignment='top')

    fig.canvas.draw()
    fig.canvas.flush_events()

#Função para iniciar a gravação
def iniciar_gravacao():
    global gravando
    gravando = True
    status_conexao.set("Conectado")
    receber_dados()

#Função para parar a gravação
def parar_gravacao():
    global gravando
    gravando = False
    status_conexao.set("Desconectado")

#Função para receber os dados do Arduino em loop
def receber_dados():
    while gravando:
        dados = ler_dados_arduino()
        if dados:
            try:
                valores = list(map(float, dados.split('\t')))
                if len(valores) == 3:
                    leitura1.append(valores[0])
                    leitura2.append(valores[1])
                    leitura3.append(valores[2])

                    if len(leitura1) > 100:
                        leitura1.pop(0)
                        leitura2.pop(0)
                        leitura3.pop(0)

                    atualizar_grafico()
            except ValueError:
                pass
        root.update_idletasks()
        root.update()

#Botões e interface do Tkinter
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

botao_iniciar = ttk.Button(frame, text="Iniciar Gravação", command=iniciar_gravacao)
botao_iniciar.grid(row=0, column=0, padx=5, pady=5)

botao_parar = ttk.Button(frame, text="Parar Gravação", command=parar_gravacao)
botao_parar.grid(row=0, column=1, padx=5, pady=5)

status_label = ttk.Label(frame, text="Status da Conexão:")
status_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

status_value = ttk.Label(frame, textvariable=status_conexao)
status_value.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

#Configuração da conexão serial
try:
    ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
    time.sleep(2)
    status_conexao.set("Pronto")
except serial.SerialException:
    messagebox.showerror("Erro", "Não foi possível conectar ao Arduino.")
    root.destroy()

#Inicializa a interface
root.mainloop()

#Finaliza a conexão serial
ser.close()