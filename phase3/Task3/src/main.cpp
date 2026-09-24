#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <queue.h>

#define MAX_MSG_LEN 32

QueueHandle_t messageQueue;

typedef struct {
  char text[MAX_MSG_LEN];
  int delayMs;
} MessageConfig;

void TaskMessanger(void *pvParameters) {
  MessageConfig *config = (MessageConfig *)pvParameters;

  for (;;) {
    xQueueSend(messageQueue, config->text, portMAX_DELAY);
    vTaskDelay(pdMS_TO_TICKS(config->delayMs));
  }
}

void TaskConsumer(void *pvParameters) {
  char received[MAX_MSG_LEN];
  for (;;) {
    if (xQueueReceive(messageQueue, &received, portMAX_DELAY) == pdTRUE) {
      Serial.println(received);
    }
  }
}

void setup() {
  Serial.begin(9600);
  messageQueue = xQueueCreate(5, MAX_MSG_LEN);

  xTaskCreate(TaskConsumer, "Consumer", 128, NULL, 1, NULL);

  static MessageConfig messageConfig1 = {"Task one is working", 1000};
  static MessageConfig messageConfig2 = {"Task two is working", 2500};

  xTaskCreate(TaskMessanger, "Messanger 1", 128, &messageConfig1, 1, NULL);
  xTaskCreate(TaskMessanger, "Messanger 2", 128, &messageConfig2, 1, NULL);
}

void loop() {}