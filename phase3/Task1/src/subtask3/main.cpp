#include <Arduino.h>
#include <avr/interrupt.h>

ISR(INT0_vect) {
  PORTB ^= (1 << PB0);
}

int main(void){
  DDRB |= (1 << PB0);

  PORTD |= (1 << PD2);
  MCUCR |= (1 << ISC01);
  MCUCR &= ~(1 << ISC00);
  
  GICR |= (1 << INT0);
  sei();

  while (1) {
  }
}
