import serial
import time
import tkinter as tk

class SerialHandler:
    def __init__(self, porta='COM5', baud_rate=9600):
        self.porta = porta
        self.baud_rate = baud_rate
        self.conexao = None

    def configurar_conexao_serial(self):
        try:
            self.ser = serial.Serial(self.porta_serial, self.baud_rate, timeout=self.timeout)
            time.sleep(2)
            self.status_conexao.set("Pronto")
        except serial.SerialException:
            self.status_conexao.set("Erro de Conexão")
            tk.messagebox.showerror("Erro", "Não foi possível conectar ao Arduino.")
            

    def ler_dados_arduino(self):
        if self.ser.is_open:
            linha = self.ser.readline().decode('utf-8').strip()
            return linha
        else:
            return None