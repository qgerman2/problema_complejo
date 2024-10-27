#include <esp_now.h>
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  struct {
    float latitude;
    float longitude;
    float altitude;
  } msg;
  if (len != sizeof(msg)) {return;}
  memcpy(&msg, incomingData, len);
  Serial.println(msg.latitude, 8);
  Serial.println(msg.longitude, 8);
  Serial.println(msg.altitude, 8);
}

void loop() {

}
