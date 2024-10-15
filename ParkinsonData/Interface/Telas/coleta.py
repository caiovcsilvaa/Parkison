import tkinter as tk
import numpy as np
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import seaborn as sns
import threading

class JanelaColeta:
    def __init__(self, root):
        self.root = root
        self.janela = tk.Toplevel(root)  #Criação do Toplevel para a nova janela
        self.janela.title("Coleta de Dados")

        self.frame_coleta = ttk.Frame(self.janela, padding="20")  # Frame dentro do Toplevel
        self.frame_coleta.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.configurar_interface_coleta()

    def configurar_interface_coleta(self):
        self.gravando = False
        self.status_conexao = tk.StringVar(value="Desconectado - Erro na conexão do Arduino X")

        sns.set(style="whitegrid")
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 8))
        plt.subplots_adjust(hspace=0.5)

        self.leitura1, self.leitura2, self.leitura3 = [], [], []
        self.interp_leitura1, self.interp_leitura2, self.interp_leitura3 = [], [], []

        # Controles
        frame_controles = ttk.Frame(self.frame_coleta, padding="10")
        frame_controles.grid(row=0, column=0, sticky=(tk.W, tk.E))

        botao_iniciar = ttk.Button(frame_controles, text="Iniciar Gravação", command=self.iniciar_gravacao)
        botao_iniciar.grid(row=0, column=0, padx=5, pady=5)

        botao_parar = ttk.Button(frame_controles, text="Parar Gravação", command=self.parar_gravacao)
        botao_parar.grid(row=0, column=1, padx=5, pady=5)

        status_label = ttk.Label(frame_controles, text="Status da Conexão:")
        status_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        status_value = ttk.Label(frame_controles, textvariable=self.status_conexao)
        status_value.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Embedding Matplotlib Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_coleta)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

        self.anim = FuncAnimation(self.fig, self.atualizar_grafico, interval=200, cache_frame_data=False)

        # Botão Voltar ao Menu
        botao_voltar_menu = ttk.Button(self.frame_coleta, text="Voltar ao Menu", command=self.voltar_para_menu)
        botao_voltar_menu.grid(row=3, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

    def iniciar_gravacao(self):
        self.configurar_conexao_serial()
        self.gravando = True
        self.status_conexao.set("Esperando início da gravação")
        threading.Thread(target=self.receber_dados).start()

    def parar_gravacao(self):
        self.gravando = False
        self.status_conexao.set("Gravação Parada")

    def mostrar_tela_coleta(self):
        self.janela.deiconify()  # Garante que o Toplevel seja mostrado
        self.status_conexao.set("Arduino Pronto para coleta ✓\nSem problemas no Sistema ✓")

    def voltar_para_menu(self):
        self.janela.withdraw()  # Oculta a janela de coleta

    def atualizar_grafico(self, frame):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.ax1.plot(self.interp_leitura1, label='Leitura 1', color='r')
        self.ax2.plot(self.interp_leitura2, label='Leitura 2', color='g')
        self.ax3.plot(self.interp_leitura3, label='Leitura 3', color='b')

        self.ax1.set_ylim(0, 10000)
        self.ax2.set_ylim(0, 10000)
        self.ax3.set_ylim(0, 10000)

        for ax, leitura in zip([self.ax1, self.ax2, self.ax3], [self.leitura1, self.leitura2, self.leitura3]):
            if leitura:
                ax.text(0.02, 0.95, f'Leitura: {leitura[-1]:.2f}', transform=ax.transAxes, va='top')

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

                        self.interp_leitura1 = np.interp(np.linspace(0, len(self.leitura1) - 1, 500),
                                                         np.arange(len(self.leitura1)), self.leitura1)
                        self.interp_leitura2 = np.interp(np.linspace(0, len(self.leitura2) - 1, 500),
                                                         np.arange(len(self.leitura2)), self.leitura2)
                        self.interp_leitura3 = np.interp(np.linspace(0, len(self.leitura3) - 1, 500),
                                                         np.arange(len(self.leitura3)), self.leitura3)
                except ValueError:
                    pass

            self.root.after(100, self.receber_dados)

    def fechar_conexao(self):
        self.gravando = False
        if hasattr(self, 'ser'):
            self.ser.close()
        self.root.destroy()