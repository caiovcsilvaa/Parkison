#include <HX711.h>

const int PINO_DT1 = 3;
const int PINO_SCK1 = 2;
const int PINO_DT2 = 7;
const int PINO_SCK2 = 6;
const int PINO_DT3 = 9;
const int PINO_SCK3 = 8;

const int TEMPO_ESPERA = 50; // Delay reduzido

HX711 escala1;
HX711 escala2;
HX711 escala3;

float fator_calibracao = -85000;
float fator_calibracao1 = 1.84;
float fator_calibracao2 = 1.88;
float fator_calibracao3 = 1.88;
float gravidade = 9.8;
float area_sensor = 0.00046;

void setup() {
  Serial.begin(115200); // Baudrate aumentado

  escala1.begin(PINO_DT1, PINO_SCK1);
  escala2.begin(PINO_DT2, PINO_SCK2);
  escala3.begin(PINO_DT3, PINO_SCK3);

  escala1.set_scale(fator_calibracao);
  escala2.set_scale(fator_calibracao);
  escala3.set_scale(fator_calibracao);

  escala1.tare();
  escala2.tare();
  escala3.tare();
}

void loop() {
  float leitura1 = 0;
  float leitura2 = 0;
  float leitura3 = 0;

  if (escala1.is_ready()) {
    leitura1 = ((escala1.get_units(10) * fator_calibracao1) * gravidade) / area_sensor;
  }
  if (escala2.is_ready()) {
    leitura2 = ((escala2.get_units(10) * fator_calibracao2) * gravidade) / area_sensor;
  }
  if (escala3.is_ready()) {
    leitura3 = ((escala3.get_units(10) * fator_calibracao3) * gravidade) / area_sensor;
  }

  Serial.print(leitura1, 1);
  Serial.print("\t");
  Serial.print(leitura2, 1);
  Serial.print("\t");
  Serial.println(leitura3, 1);

  delay(TEMPO_ESPERA); // Delay reduzido
}