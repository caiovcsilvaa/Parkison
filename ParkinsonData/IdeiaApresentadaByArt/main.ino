
#include <HX711.h>; // Adiciona a biblioteca ao código

// Configuração dos pinos para o módulo HX711
const int PINO_DT1 = 3;
const int PINO_SCK1 = 2;

const int PINO_DT2 = 7;
const int PINO_SCK2 = 6;

const int PINO_DT3 = 9;
const int PINO_SCK3 = 8;

const int TEMPO_ESPERA = 300; // Declaração da variável de espera

HX711 escala1; // Declaração do objeto escala na classe HX711 da biblioteca
HX711 escala2;
HX711 escala3;

float fator_calibracao = -85000; // Pré-definição da variável de calibração
float fator_calibracao1 = 1.84;
float fator_calibracao2 = 1.88;
float fator_calibracao3 = 1.88;
float gravidade = 9.8;
float area_sensor = 0.00046;

void setup() {
  // Mensagens do monitor serial
  Serial.begin(9600); // Inicializa a comunicação serial com baud rate de 9600

  escala1.begin(PINO_DT1, PINO_SCK1); // Inicialização e definição dos pinos DT e SCK dentro do objeto ESCALA
  escala2.begin(PINO_DT2, PINO_SCK2); // Inicialização e definição dos pinos DT e SCK dentro do objeto ESCALA
  escala3.begin(PINO_DT3, PINO_SCK3);

  escala1.set_scale(fator_calibracao);
  escala2.set_scale(fator_calibracao);
  escala3.set_scale(fator_calibracao);

  escala1.tare(); // Zera a escala
  escala2.tare(); // Zera a escala
  escala3.tare(); // Zera a escala
}

void loop() {
  // Verifica se o módulo está pronto para realizar leituras
  if (escala1.is_ready()) {
    // Mensagens de leitura no monitor serial
    Serial.print("Leitura 1: ");
    Serial.print(((escala1.get_units(10) * fator_calibracao1) * gravidade) / area_sensor, 1); // Retorna a leitura da variável escala com a unidade Newtons
  }
  if (escala2.is_ready()) {
    // Mensagens de leitura no monitor serial
    Serial.print("  Leitura 2: ");
    Serial.print(((escala2.get_units(10) * fator_calibracao2) * gravidade) / area_sensor, 1); // Retorna a leitura da variável escala com a unidade Newtons
  }
  if (escala3.is_ready()) {
    // Mensagens de leitura no monitor serial
    Serial.print("  Leitura 3: ");
    Serial.print(((escala3.get_units(10) * fator_calibracao3) * gravidade) / area_sensor, 1); // Retorna a leitura da variável escala com a unidade Newtons
  }
  Serial.println();   
  delay(TEMPO_ESPERA);
}