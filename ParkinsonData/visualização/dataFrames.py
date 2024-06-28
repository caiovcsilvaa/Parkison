import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#setup
porta_serial = 'COM5'  
baud_rate = 9600
timeout = 1

#aguarda o recebimento
ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
time.sleep(2)  #Aguarda a inicialização da conexão

#ler dados
def ler_dados_arduino():
    linha = ser.readline().decode('utf-8').strip()
    return linha

#conf graph
plt.ion()  
fig, ax = plt.subplots()
sns.set(style="whitegrid")

#Arrays para armazenar os dados
leitura1 = []
leitura2 = []
leitura3 = []

try:
    while True:
        dados = ler_dados_arduino()
        if dados:
            try:
                valores = list(map(float, dados.split('\t')))
                if len(valores) == 3:
                    leitura1.append(valores[0])
                    leitura2.append(valores[1])
                    leitura3.append(valores[2])

                    #ideia condicionada
                    if len(leitura1) > 100:
                        leitura1.pop(0)
                        leitura2.pop(0)
                        leitura3.pop(0)

                    #atualiza o df
                    df = pd.DataFrame({
                        'Leitura 1': leitura1,
                        'Leitura 2': leitura2,
                        'Leitura 3': leitura3
                    })

                    #limpa para reescrita
                    ax.clear()
                    sns.lineplot(data=df, ax=ax)
                    plt.pause(0.01)

            except ValueError:
                pass

except KeyboardInterrupt:
    print("interrompido pelo teclado")

finally:
    ser.close()
    plt.ioff()
    plt.show()