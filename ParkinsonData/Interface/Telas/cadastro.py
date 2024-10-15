import tkinter as tk
from tkinter import ttk, messagebox

class JanelaCadastro:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Cadastro de Paciente")
        self.criar_campos()

    def criar_campos(self):
        ttk.Label(self.janela, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
        self.entrada_nome = ttk.Entry(self.janela)
        self.entrada_nome.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self.janela, text="Salvar", command=self.salvar).grid(row=1, column=0, columnspan=2, pady=10)

    def salvar(self):
        nome = self.entrada_nome.get()
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return
        messagebox.showinfo("Sucesso", f"Paciente {nome} cadastrado com sucesso!")
        self.janela.destroy()