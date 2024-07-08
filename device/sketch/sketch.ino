#include <WiFi.h>
#include <HTTPClient.h>

#define WIFI_SSID "Sibur"
#define WIFI_PASSWORD "123456789"

#define DEVICE_UUID "05a3c7d1-e7d0-46c8-bc13-3a0358a0d287"
#define DEVICE_TOKEN "e80b6-98852706392b43b5f6fc15-7-717764ffdb2--2-28-974b24ba4faaab063bd00f8-e1b758d5302--9-54a7f4c-b4"

#define DELAY_MS 10000

uint32_t delta = 0;

void setup() {
  Serial.begin(9600);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting... ");
  while ( WiFi.status() != WL_CONNECTED) {
    delay(10);
  }
  Serial.println("Connected");
  delta = millis();
}

void loop() {
  
}
