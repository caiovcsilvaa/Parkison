import serial
import time
from collections import deque
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

#setup
porta_serial = 'COM5'  
baud_rate = 9600
timeout = 1

#recebimento da serial
ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
time.sleep(2)  

#ler dados 
def ler_dados_arduino():
    linha = ser.readline().decode('utf-8').strip()
    return linha

app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Leituras do Arduino")
win.resize(1000, 600)
win.setWindowTitle('Leituras do Arduino')

pg.setConfigOptions(antialias=True)

p1 = win.addPlot(title="Leitura 1")
curve1 = p1.plot(pen='r')
p2 = win.addPlot(title="Leitura 2")
curve2 = p2.plot(pen='g')
p3 = win.addPlot(title="Leitura 3")
curve3 = p3.plot(pen='b')

leitura1 = deque(maxlen=100)
leitura2 = deque(maxlen=100)
leitura3 = deque(maxlen=100)

def update():
    global leitura1, leitura2, leitura3
    dados = ler_dados_arduino()
    if dados:
        try:
            valores = list(map(float, dados.split('\t')))
            if len(valores) == 3:
                leitura1.append(valores[0])
                leitura2.append(valores[1])
                leitura3.append(valores[2])

                curve1.setData(leitura1)
                curve2.setData(leitura2)
                curve3.setData(leitura3)

        except ValueError:
            pass

#Atualiza o gráfico a cada 100 milissegundos - tentei reduzir no proprio arduino mas n ficou legal
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

#Fechar a conexão serial ao fechar a janela
def close():
    ser.close()
    timer.stop()
    app.quit()

win.closeEvent = lambda event: close()

#Iniciar o loop do aplicativo
QtWidgets.QApplication.instance().exec_()