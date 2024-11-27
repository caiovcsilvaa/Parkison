import tkinter as tk
from tkinter import ttk, messagebox

class JanelaCadastro:
    def __init__(self, root, lista_pacientes):
        self.root = root
        self.janela = tk.Toplevel(root)
        self.janela.title("Cadastro de Paciente")
        self.lista_pacientes = lista_pacientes  # Referência para a lista global de pacientes
        self.mostrar_cadastro_paciente()

    def mostrar_cadastro_paciente(self):
        # Nome
        label_nome = ttk.Label(self.janela, text="Nome do Paciente:")
        label_nome.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entrada_nome = ttk.Entry(self.janela, width=30)
        entrada_nome.grid(row=0, column=1, padx=10, pady=10)

        # Sexo
        label_sexo = ttk.Label(self.janela, text="Sexo:")
        label_sexo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        combo_sexo = ttk.Combobox(self.janela, values=["Masculino", "Feminino", "Outro"], width=27)
        combo_sexo.grid(row=1, column=1, padx=10, pady=10)

        # Idade
        label_idade = ttk.Label(self.janela, text="Idade:")
        label_idade.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        combo_idade = ttk.Combobox(self.janela, values=["30 a 44", "45 a 59", "60 a 74", "75 a 84", "Maior que 85"], width=27)
        combo_idade.grid(row=2, column=1, padx=10, pady=10)

        # Nível de instrução
        label_instrucao = ttk.Label(self.janela, text="Nível de Instrução:")
        label_instrucao.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        combo_instrucao = ttk.Combobox(self.janela, values=[ 
            "Sem instrução", "Fundamental incompleto", "Fundamental completo e médio incompleto",
            "Médio completo e superior incompleto", "Superior completo", "Não definido"
        ], width=27)
        combo_instrucao.grid(row=3, column=1, padx=10, pady=10)

        # Sintomas motores
        label_sintomas_motor = ttk.Label(self.janela, text="Sintomas Motores:")
        label_sintomas_motor.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        motor_frame = tk.Frame(self.janela)
        motor_frame.grid(row=0, column=3, rowspan=4, padx=10, pady=10, sticky="n")
        sintomas_motor = ["Tremor", "Rigidez", "Bradicinesia", "Instabilidade postural", "Marcha festinante",
                          "Alterações na fala", "Micrografia"]
        motor_vars = [tk.BooleanVar() for _ in sintomas_motor]
        for sintoma, var in zip(sintomas_motor, motor_vars):
            tk.Checkbutton(motor_frame, text=sintoma, variable=var).pack(anchor="w")

        # Sintomas não motores
        label_sintomas_nao_motor = ttk.Label(self.janela, text="Sintomas Não Motores:")
        label_sintomas_nao_motor.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        nao_motor_frame = tk.Frame(self.janela)
        nao_motor_frame.grid(row=4, column=3, rowspan=3, padx=10, pady=10, sticky="n")
        sintomas_nao_motor = ["Depressão", "Ansiedade", "Insônia", "Constipação", "Fadiga",
                              "Problemas de memória e cognição"]
        nao_motor_vars = [tk.BooleanVar() for _ in sintomas_nao_motor]
        for sintoma, var in zip(sintomas_nao_motor, nao_motor_vars):
            tk.Checkbutton(nao_motor_frame, text=sintoma, variable=var).pack(anchor="w")

        # Tempo de diagnóstico
        label_diagnostico = ttk.Label(self.janela, text="Tempo de Diagnóstico:")
        label_diagnostico.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        combo_diagnostico = ttk.Combobox(self.janela, values=["0 a 3 anos", "5 a 10 anos", "Mais de 10 anos"], width=27)
        combo_diagnostico.grid(row=5, column=1, padx=10, pady=10)

        # Tratamento medicamentoso
        label_tratamento = ttk.Label(self.janela, text="Tratamento Medicamentoso:")
        label_tratamento.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        combo_tratamento = ttk.Combobox(self.janela, values=["Sim", "Não"], width=27)
        combo_tratamento.grid(row=6, column=1, padx=10, pady=10)

        # Nome da medicação
        label_medicacao = ttk.Label(self.janela, text="Qual medicação?")
        entrada_medicacao = ttk.Entry(self.janela, width=30)
        label_medicacao.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        entrada_medicacao.grid(row=7, column=1, padx=10, pady=10)

        # Terapia de reabilitação
        label_terapia = ttk.Label(self.janela, text="Terapia de Reabilitação:")
        label_terapia.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        combo_terapia = ttk.Combobox(self.janela, values=["Sim", "Não"], width=27)
        combo_terapia.grid(row=8, column=1, padx=10, pady=10)

        # Tipo de Terapia
        label_tipo_terapia = ttk.Label(self.janela, text="Tipo de Terapia:")
        label_tipo_terapia.grid(row=9, column=0, padx=10, pady=10, sticky="w")
        terapia_frame = tk.Frame(self.janela)
        terapia_frame.grid(row=9, column=1, padx=10, pady=10, sticky="w")
        tipo_terapia = ["Fisioterapia", "Terapia Ocupacional", "Fonoaudiologia"]
        terapia_vars = [tk.BooleanVar() for _ in tipo_terapia]
        for tipo, var in zip(tipo_terapia, terapia_vars):
            tk.Checkbutton(terapia_frame, text=tipo, variable=var).pack(anchor="w")

        # Botão de salvar
        botao_salvar_paciente = ttk.Button(self.janela, text="Salvar Paciente", 
                                           command=lambda: self.salvar_paciente(entrada_nome.get(), combo_sexo.get(),
                                                                                combo_idade.get(), combo_instrucao.get(),
                                                                                motor_vars, nao_motor_vars, 
                                                                                combo_diagnostico.get(), combo_tratamento.get(),
                                                                                entrada_medicacao.get(), combo_terapia.get(), 
                                                                                terapia_vars))
        botao_salvar_paciente.grid(row=10, column=0, columnspan=4, pady=20)

    def salvar_paciente(self, nome, sexo, idade, instrucao, motor_vars, nao_motor_vars, diagnostico, tratamento, medicacao, terapia, terapia_vars):
        # Dados do paciente em um dicionário
        paciente = {
            "nome": nome,
            "sexo": sexo,
            "idade": idade,
            "instrucao": instrucao,
            "sintomas_motor": [sintoma for sintoma, var in zip(
                ["Tremor", "Rigidez", "Bradicinesia", "Instabilidade postural", "Marcha festinante",
                 "Alterações na fala", "Micrografia"], motor_vars) if var.get()],
            "sintomas_nao_motor": [sintoma for sintoma, var in zip(
                ["Depressão", "Ansiedade", "Insônia", "Constipação", "Fadiga", "Problemas de memória e cognição"], nao_motor_vars) if var.get()],
            "diagnostico": diagnostico,
            "tratamento": {"sim_nao": tratamento, "medicacao": medicacao},
            "terapia": {"sim_nao": terapia, "tipo": [tipo for tipo, var in zip(
                ["Fisioterapia", "Terapia Ocupacional", "Fonoaudiologia"], terapia_vars) if var.get()] }
        }

        # Verificação de campos obrigatórios
        if not nome or not sexo or not idade or not instrucao:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        # Adiciona o paciente à lista de pacientes
        self.lista_pacientes.append(paciente)

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", f"Paciente {nome} cadastrado com sucesso!")

        # Fecha a janela de cadastro
        self.janela.destroy()