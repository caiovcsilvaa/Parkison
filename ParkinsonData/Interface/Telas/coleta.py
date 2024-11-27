import tkinter as tk
from tkinter import ttk
import numpy as np
import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import seaborn as sns
import threading

class JanelaColeta:
    def __init__(self, root, menu_principal):

        self.menu_principal = menu_principal
        self.gravando = False
        self.status_conexao = tk.StringVar(value=" Desconectado - Erro na conexão do Arduino X")

        self.porta_serial = 'COM5'
        self.baud_rate = 9600
        self.timeout = 0.05
        
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
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(7, 7))
        plt.subplots_adjust(hspace=0.5)

        self.leitura1, self.leitura2, self.leitura3 = [], [], []
        self.interp_leitura1, self.interp_leitura2, self.interp_leitura3 = [], [], []

        #Controles
        frame_controles = ttk.Frame(self.frame_coleta, padding="10")
        frame_controles.grid(row=0, column=0, sticky=(tk.W, tk.E))

        botao_iniciar = ttk.Button(frame_controles, text="Iniciar Gravação", command=self.iniciar_gravacao)
        botao_iniciar.grid(row=0, column=0, padx=5, pady=5)

        botao_parar = ttk.Button(frame_controles, text="Parar Gravação", command=self.parar_gravacao)
        botao_parar.grid(row=0, column=1, padx=5, pady=5)

        botao_gerar_relatorio = ttk.Button(self.janela, text="Gerar Relatório", command= self.gerar_relatorio)
        botao_gerar_relatorio.grid(row=0, column=2,padx=5, pady=5)

        status_label = ttk.Label(frame_controles, text="Status da Conexão:")
        status_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        
        #Botão Voltar ao Menu
        botao_voltar_menu = ttk.Button(self.frame_coleta, text="Voltar ao Menu", command=self.voltar_para_menu)
        botao_voltar_menu.grid(row=3, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

        status_value = ttk.Label(frame_controles, textvariable=self.status_conexao)
        status_value.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        #Embedding Matplotlib Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_coleta)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

    def configurar_conexao_serial(self):
        try:
            self.ser = serial.Serial(self.porta_serial, self.baud_rate, timeout=self.timeout)
            time.sleep(2)
            self.status_conexao.set("Pronto")
        except serial.SerialException:
            self.status_conexao.set("Erro de Conexão")
            tk.messagebox.showerror("Erro", "Não foi possível conectar ao Arduino.")
            

    def iniciar_gravacao(self):
        self.configurar_conexao_serial()
        self.gravando = True
        self.status_conexao.set("Esperando início da gravação")
        threading.Thread(target=self.receber_dados).start()

    def parar_gravacao(self):
        self.gravando = False
        self.status_conexao.set("Gravação Parada")

    def ler_dados_arduino(self):
        if self.ser.is_open:
            linha = self.ser.readline().decode('utf-8').strip()
            return linha
        else:
            return None
        
    def iniciar_gravacao(self):
        #Configuração da conexão serial
        self.configurar_conexao_serial()
        self.gravando = True
        self.status_conexao.set("Esperando início da gravação")
        threading.Thread(target=self.receber_dados).start()

    def parar_gravacao(self):
        self.gravando = False
        self.status_conexao.set("Gravação Parada")
    
    
    def mostrar_tela_coleta(self):
        self.root.withdraw()  # Oculta o menu principal
        JanelaColeta(self.root, self)

    

    def voltar_para_menu(self):
        self.janela.destroy()
        self.menu_principal.root.deiconify()
        self.menu_principal.frame_menu.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def fechar_conexao(self):
        self.gravando = False
        if hasattr(self, 'ser'):
            self.ser.close()
        self.root.destroy()