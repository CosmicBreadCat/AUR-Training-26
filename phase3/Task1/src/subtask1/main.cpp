#include <Arduino.h>
#include <avr/io.h>

void T0_setup_CTC() {
  OCR0 = 124;
  TCCR0 = (1 << WGM01) | (1 << CS01) | (1 << CS00);
}

void T0_wait_1ms() {
  while ((TIFR & (1 << OCF0)) == 0)
    ;
  TIFR = (1 << OCF0);
}

int main(void) {
  T0_setup_CTC();
  DDRB |= (1 << PB0);

  while (1) {

    PORTB ^= (1 << PB0);

    for (uint16_t i = 0; i < 500; i++) {
      T0_wait_1ms();
    }
  }
}