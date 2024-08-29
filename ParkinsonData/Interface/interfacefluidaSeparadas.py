import serial
import threading
import time
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

class ArduinoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface de Coleta de Dados do Arduino")

        #Variáveis de controle
        self.gravando = False
        self.status_conexao = tk.StringVar(value="Desconectado")

        #Setup da porta serial
        self.porta_serial = 'COM5'
        self.baud_rate = 115200
        self.timeout = 0.1

        #Configuração inicial do Matplotlib
        sns.set(style="whitegrid")
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 8))
        plt.subplots_adjust(hspace=0.5)  # Espaçamento entre os gráficos

        #Arrays para armazenar os dados
        self.leitura1 = []
        self.leitura2 = []
        self.leitura3 = []

        #Arrays para armazenar os dados interpolados
        self.interp_leitura1 = []
        self.interp_leitura2 = []
        self.interp_leitura3 = []

        #Configuração da interface gráfica
        self.configurar_interface()

        #Configuração da conexão serial
        self.configurar_conexao_serial()

        #Configuração da animação
        self.anim = FuncAnimation(self.fig, self.atualizar_grafico, interval=200, cache_frame_data=False)

    def configurar_interface(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        botao_iniciar = ttk.Button(frame, text="Iniciar Gravação", command=self.iniciar_gravacao)
        botao_iniciar.grid(row=0, column=0, padx=5, pady=5)

        botao_parar = ttk.Button(frame, text="Parar Gravação", command=self.parar_gravacao)
        botao_parar.grid(row=0, column=1, padx=5, pady=5)

        status_label = ttk.Label(frame, text="Status da Conexão:")
        status_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        status_value = ttk.Label(frame, textvariable=self.status_conexao)
        status_value.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        #Embedding Matplotlib figure into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

    def configurar_conexao_serial(self):
        try:
            self.ser = serial.Serial(self.porta_serial, self.baud_rate, timeout=self.timeout)
            time.sleep(2)
            self.status_conexao.set("Pronto")
        except serial.SerialException:
            messagebox.showerror("Erro", "Não foi possível conectar ao Arduino.")
            self.root.destroy()

    def ler_dados_arduino(self):
        if self.ser.is_open:
            linha = self.ser.readline().decode('utf-8').strip()
            return linha
        else:
            return None

    def atualizar_grafico(self, frame):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        #Atualizar os gráficos com os dados interpolados
        self.ax1.plot(self.interp_leitura1, label='Leitura 1', color='r')
        self.ax2.plot(self.interp_leitura2, label='Leitura 2', color='g')
        self.ax3.plot(self.interp_leitura3, label='Leitura 3', color='b')

        self.ax1.set_ylim(bottom=0, top=10000)
        self.ax2.set_ylim(bottom=0, top=10000)
        self.ax3.set_ylim(bottom=0, top=10000)

        self.ax1.legend(loc='upper right')
        self.ax2.legend(loc='upper right')
        self.ax3.legend(loc='upper right')

        if self.leitura1:
            self.ax1.text(0.02, 0.95, f'Leitura 1: {self.leitura1[-1]:.2f}', transform=self.ax1.transAxes, verticalalignment='top')
        if self.leitura2:
            self.ax2.text(0.02, 0.95, f'Leitura 2: {self.leitura2[-1]:.2f}', transform=self.ax2.transAxes, verticalalignment='top')
        if self.leitura3:
            self.ax3.text(0.02, 0.95, f'Leitura 3: {self.leitura3[-1]:.2f}', transform=self.ax3.transAxes, verticalalignment='top')



    def iniciar_gravacao(self):
        self.gravando = True
        self.status_conexao.set("Conectado")
        threading.Thread(target=self.receber_dados).start()  # Iniciar uma thread separada para a leitura serial


    def parar_gravacao(self):
        self.gravando = False
        self.status_conexao.set("Desconectado")

    def receber_dados(self):
        if self.gravando:
            dados = self.ler_dados_arduino()
            if dados:
                try:
                    valores = list(map(float, dados.split('\t')))
                    if len(valores) == 3:
                        self.leitura1.append(valores[0])
                        self.leitura2.append(valores[1])
                        self.leitura3.append(valores[2])

                        if len(self.leitura1) > 100:
                            self.leitura1.pop(0)
                            self.leitura2.pop(0)
                            self.leitura3.pop(0)

                        #Interpolação linear para suavizar as transições entre os dados
                        self.interp_leitura1 = np.interp(np.linspace(0, len(self.leitura1) - 1, 500), np.arange(len(self.leitura1)), self.leitura1)
                        self.interp_leitura2 = np.interp(np.linspace(0, len(self.leitura2) - 1, 500), np.arange(len(self.leitura2)), self.leitura2)
                        self.interp_leitura3 = np.interp(np.linspace(0, len(self.leitura3) - 1, 500), np.arange(len(self.leitura3)), self.leitura3)

                except ValueError:
                    pass

            self.root.after(100, self.receber_dados)  # Reagendar a função para ser chamada novamente em 100ms

    def fechar_conexao(self):
        self.gravando = False
        self.ser.close()
        self.root.destroy()

#Inicializa a interface
if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar_conexao)  # Garante que a conexão será fechada ao sair
    root.mainloop()
