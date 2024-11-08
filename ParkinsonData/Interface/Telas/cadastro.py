import tkinter as tk
from tkinter import ttk, messagebox

class JanelaCadastro:
    def __init__(self, root):
        self.root = root  #Atribuindo root à instância
        self.janela = tk.Toplevel(root)  #Criando a nova janela
        self.janela.title("Cadastro de Paciente")
        self.mostrar_cadastro_paciente()

    def mostrar_cadastro_paciente(self):
        #Campos para Nome, Sexo e Idade (já criados anteriormente)
        label_nome = ttk.Label(self.janela, text="Nome do Paciente:")
        label_nome.grid(row=0, column=0, padx=10, pady=10)
        entrada_nome = ttk.Entry(self.janela)
        entrada_nome.grid(row=0, column=1, padx=10, pady=10)

        label_sexo = ttk.Label(self.janela, text="Sexo:")
        label_sexo.grid(row=1, column=0, padx=10, pady=10)
        combo_sexo = ttk.Combobox(self.janela, values=["Masculino", "Feminino", "Outro"])
        combo_sexo.grid(row=1, column=1, padx=10, pady=10)

        label_idade = ttk.Label(self.janela, text="Idade:")
        label_idade.grid(row=2, column=0, padx=10, pady=10)
        combo_idade = ttk.Combobox(self.janela, values=["30 a 44", "45 a 59", "60 a 74", "75 a 84", "Maior que 85"])
        combo_idade.grid(row=2, column=1, padx=10, pady=10)

        #Nível de instrução
        label_instrucao = ttk.Label(self.janela, text="Nível de Instrução:")
        label_instrucao.grid(row=3, column=0, padx=10, pady=10)
        combo_instrucao = ttk.Combobox(self.janela, values=[
            "Sem instrução", "Fundamental incompleto", "Fundamental completo e médio incompleto",
            "Médio completo e superior incompleto", "Superior completo", "Não definido"
        ])
        combo_instrucao.grid(row=3, column=1, padx=10, pady=10)

        #Sintomas apresentados - Sintomas motores
        label_sintomas_motor = ttk.Label(self.janela, text="Sintomas Motores:")
        label_sintomas_motor.grid(row=4, column=0, padx=10, pady=10)
        motor_frame = tk.Frame(self.janela)
        motor_frame.grid(row=4, column=1, padx=10, pady=10)
        sintomas_motor = ["Tremor", "Rigidez", "Bradicinesia", "Instabilidade postural", "Marcha festinante",
                        "Alterações na fala", "Micrografia"]
        motor_vars = [tk.BooleanVar() for _ in sintomas_motor]
        for i, sintoma in enumerate(sintomas_motor):
            cb = tk.Checkbutton(motor_frame, text=sintoma, variable=motor_vars[i])
            cb.pack(anchor='w')

        #Sintomas apresentados - Sintomas não motores
        label_sintomas_nao_motor = ttk.Label(self.janela, text="Sintomas Não Motores:")
        label_sintomas_nao_motor.grid(row=5, column=0, padx=10, pady=10)
        nao_motor_frame = tk.Frame(self.janela)
        nao_motor_frame.grid(row=5, column=1, padx=10, pady=10)
        sintomas_nao_motor = ["Depressão", "Ansiedade", "Insônia", "Constipação", "Fadiga",
                            "Problemas de memória e cognição"]
        nao_motor_vars = [tk.BooleanVar() for _ in sintomas_nao_motor]
        for i, sintoma in enumerate(sintomas_nao_motor):
            cb = tk.Checkbutton(nao_motor_frame, text=sintoma, variable=nao_motor_vars[i])
            cb.pack(anchor='w')

        #Tempo de diagnóstico
        label_diagnostico = ttk.Label(self.janela, text="Tempo de Diagnóstico:")
        label_diagnostico.grid(row=6, column=0, padx=10, pady=10)
        combo_diagnostico = ttk.Combobox(self.janela, values=["0 a 3 anos", "5 a 10 anos", "Mais de 10 anos"])
        combo_diagnostico.grid(row=6, column=1, padx=10, pady=10)

        #Tratamento medicamentoso
        label_tratamento = ttk.Label(self.janela, text="Tratamento Medicamentoso:")
        label_tratamento.grid(row=7, column=0, padx=10, pady=10)
        combo_tratamento = ttk.Combobox(self.janela, values=["Sim", "Não"])
        combo_tratamento.grid(row=7, column=1, padx=10, pady=10)

        #Nome da medicação (se tratamento for "Sim")
        label_medicacao = ttk.Label(self.janela, text="Qual medicação?")
        entrada_medicacao = ttk.Entry(self.janela)
        label_medicacao.grid(row=8, column=0, padx=10, pady=10)
        entrada_medicacao.grid(row=8, column=1, padx=10, pady=10)

        #Terapia de reabilitação
        label_terapia = ttk.Label(self.janela, text="Terapia de Reabilitação:")
        label_terapia.grid(row=9, column=0, padx=10, pady=10)
        combo_terapia = ttk.Combobox(self.janela, values=["Sim", "Não"])
        combo_terapia.grid(row=9, column=1, padx=10, pady=10)

        #Tipo de Terapia
        label_tipo_terapia = ttk.Label(self.janela, text="Tipo de Terapia:")
        label_tipo_terapia.grid(row=10, column=0, padx=10, pady=10)
        terapia_frame = tk.Frame(self.janela)
        terapia_frame.grid(row=10, column=1, padx=10, pady=10)
        tipo_terapia = ["Fisioterapia", "Terapia Ocupacional", "Fonoaudiologia"]
        terapia_vars = [tk.BooleanVar() for _ in tipo_terapia]
        for i, tipo in enumerate(tipo_terapia):
            cb = tk.Checkbutton(terapia_frame, text=tipo, variable=terapia_vars[i])
            cb.pack(anchor='w')

        # Botão de salvar os dados do paciente
        botao_salvar_paciente = ttk.Button(self.janela, text="Salvar Paciente", 
                                        command=lambda: self.salvar_paciente(entrada_nome.get(), combo_sexo.get(),
                                                                                combo_idade.get(), combo_instrucao.get(),
                                                                                motor_vars, nao_motor_vars, 
                                                                                combo_diagnostico.get(), combo_tratamento.get(),
                                                                                entrada_medicacao.get(), combo_terapia.get(), 
                                                                                terapia_vars, self.janela))
        botao_salvar_paciente.grid(row=11, column=0, columnspan=2, pady=10)

    def salvar_paciente(self, nome, sexo, idade, instrucao, motor_vars):
        # Obter sintomas motores selecionados
        sintomas_motor_selecionados = [sintoma for sintoma, var in zip(
            ["Tremor", "Rigidez", "Bradicinesia", "Instabilidade postural", 
             "Marcha festinante", "Alterações na fala", "Micrografia"], motor_vars) if var.get()]

        # Validação básica
        if not nome or not sexo or not idade or not instrucao:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        # Montar string com dados
        dados_paciente = (
            f"Nome: {nome}\n"
            f"Sexo: {sexo}\n"
            f"Idade: {idade}\n"
            f"Nível de Instrução: {instrucao}\n"
            f"Sintomas Motores: {', '.join(sintomas_motor_selecionados) if sintomas_motor_selecionados else 'Nenhum'}"
        )

        # Exibir mensagem de sucesso
        messagebox.showinfo("Paciente Cadastrado", f"Paciente cadastrado com sucesso!\n\n{dados_paciente}")

        # Fechar a janela de cadastro
        self.janela.destroy()

    def salvar_paciente(self, nome, sexo, idade, instrucao, motor_vars, nao_motor_vars, diagnostico, tratamento, medicacao, terapia, terapia_vars, janela):
        #Obter os sintomas motores selecionados
        sintomas_motor_selecionados = [sintoma for sintoma, var in zip(
            ["Tremor", "Rigidez", "Bradicinesia", "Instabilidade postural", "Marcha festinante", "Alterações na fala", "Micrografia"], motor_vars) if var.get()]
        
        #Obter os sintomas não motores selecionados
        sintomas_nao_motor_selecionados = [sintoma for sintoma, var in zip(
            ["Depressão", "Ansiedade", "Insônia", "Constipação", "Fadiga", "Problemas de memória e cognição"], nao_motor_vars) if var.get()]
        
        #Obter os tipos de terapia selecionados
        terapias_selecionadas = [tipo for tipo, var in zip(
            ["Fisioterapia", "Terapia Ocupacional", "Fonoaudiologia"], terapia_vars) if var.get()]
        
        #Validação básica de campos obrigatórios
        if not nome or not sexo or not idade or not instrucao or not diagnostico or not tratamento or (tratamento == "Sim" and not medicacao) or not terapia:
            tk.messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return
        
        #Criar uma string com todos os dados coletados
        dados_paciente = (
            f"Nome: {nome}\n"
            f"Sexo: {sexo}\n"
            f"Idade: {idade}\n"
            f"Nível de Instrução: {instrucao}\n"
            f"Sintomas Motores: {', '.join(sintomas_motor_selecionados) if sintomas_motor_selecionados else 'Nenhum'}\n"
            f"Sintomas Não Motores: {', '.join(sintomas_nao_motor_selecionados) if sintomas_nao_motor_selecionados else 'Nenhum'}\n"
            f"Tempo de Diagnóstico: {diagnostico}\n"
            f"Tratamento Medicamentoso: {tratamento}\n"
            f"Medicação: {medicacao if tratamento == 'Sim' else 'Não se aplica'}\n"
            f"Terapia de Reabilitação: {terapia}\n"
            f"Tipos de Terapia: {', '.join(terapias_selecionadas) if terapias_selecionadas else 'Nenhum'}"
        )
        
        #Exibir uma mensagem de confirmação com os dados do paciente
        tk.messagebox.showinfo("Paciente Cadastrado", f"Paciente cadastrado com sucesso!\n\n{dados_paciente}")
        
        #Fechar a janela de cadastro após salvar os dados
        janela.destroy()
