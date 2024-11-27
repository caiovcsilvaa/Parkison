import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from cadastro import JanelaCadastro
from coleta import JanelaColeta

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.lista_pacientes = []
        self.root.title("Menu Principal")
        self.frame_menu = ttk.Frame(self.root, padding="20")
        self.frame_menu.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.configurar_menu_inicial()
        self.carregar_logo()

    def carregar_logo(self):
        try:
            #Caminho correto da imagem
            imagem = Image.open(r"C:\Users\caiov\Desktop\parkinson\Parkison\ParkinsonData\Interface\Telas\upelogo.png")
            imagem = imagem.resize((100, 100), Image.LANCZOS)  # Use LANCZOS em vez de ANTIALIAS

            #Converte a imagem para o formato compatível com Tkinter
            self.logo = ImageTk.PhotoImage(imagem)

            #Adiciona a imagem ao menu
            label_logo = ttk.Label(self.frame_menu, image=self.logo)
            label_logo.grid(row=3, column=0, columnspan=5, pady=10)

        except Exception as e:
            print(f"Erro ao carregar a logo: {e}")

    def configurar_menu_inicial(self):
        label_bem_vindo = ttk.Label(self.frame_menu, text="Bem-vindo ao Sistema de Coleta de Dados da Quantificação de Tremores da Doença de Parkinson ", font=("Helvetica", 16))
        label_bem_vindo.grid(row=0, column=0, columnspan=2, pady=10)

        botao_iniciar_coleta = ttk.Button(self.frame_menu, text="Iniciar Coleta de Dados", command=self.mostrar_tela_coleta)
        botao_iniciar_coleta.grid(row=1, column=0, padx=5, pady=10)

        botao_configuracoes = ttk.Button(self.frame_menu, text="Pacientes", command=self.mostrar_cadastro_paciente)
        botao_configuracoes.grid(row=1, column=1, padx=5, pady=10)

        botao_sair = ttk.Button(self.frame_menu, text="Sair", command=self.root.quit)
        botao_sair.grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_tela_coleta(self):
        self.root.withdraw()
        self.frame_menu.grid_forget()
        JanelaColeta(self.root, self)
        

    def mostrar_cadastro_paciente(self):
        JanelaCadastro(self.root, self.lista_pacientes)