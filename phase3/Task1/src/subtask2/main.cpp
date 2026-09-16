#include <Arduino.h>
#include <avr/io.h>
#include <util/delay.h>

void PWM0_Fast_Init() {
  DDRB |= (1 << PB3);
  OCR0 = 64;

  // f_PWM = F_CPU / (Prescaler * 256) = 8,000,000 / (8 * 256) = 3906.25 Hz
  TCCR0 = (1 << WGM00) | (1 << WGM01) |
          (1 << COM01) | (1 << CS01);
}

int main(void) {
  PWM0_Fast_Init();

  while (1) {

    for (uint8_t duty = 64; duty < 255; duty++) {
      OCR0 = duty;
      _delay_ms(10);
    }

    OCR0 = 64;
  }
}