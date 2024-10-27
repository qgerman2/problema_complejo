#include <esp_now.h>
#include <WiFi.h>
#include "structs.h"

struct {
    AP::baro_data_message_t baro;
    AP::mag_data_message_t mag;
    AP::gps_data_message_t gps;
    AP::ins_data_message_t ins;
    AP::airspeed_data_message_t aspd;
    float q[4];
    EFI_State efi;
  } ahrs_msg;

uint8_t buffer[600];
unsigned long pos = 0;

unsigned long last_message_time = 0;

uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
esp_now_peer_info_t peerInfo;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}

void send_ping() {
  char ping_msg[21] = "PINGHITLPINGHITLPING";
  struct _header header;
  struct _footer footer;
  header.type = 0;
  Serial.write(reinterpret_cast<uint8_t *>(&header), sizeof(header));
  Serial.write(reinterpret_cast<uint8_t *>(&ping_msg[0]), sizeof(ping_msg));
  footer.len = sizeof(header) + sizeof(ping_msg);
  Serial.write(reinterpret_cast<uint8_t *>(&footer), sizeof(footer));
}

void read() {
  struct _header header;
  struct _footer footer;
  while (Serial.available() > 0) {
    // read a single byte into the buffer
    if (!Serial.readBytes(&buffer[pos], 1)) {
        continue;
    }
    // check if the first bytes of the message match the preamble
    if (pos < sizeof(header.preamble)) {
        if (buffer[pos] != header.preamble[pos]) {
            pos = 0;
            continue;
        }
    }
    // if we get to this point it means the first bytes have matched the
    // header so far
    pos++;
    if (pos == sizeof(header)) {
      memcpy(&header, buffer, sizeof(header));
      if (header.type == 1) {
          pos = 0;
      }
    } else if (pos == sizeof(ahrs_msg) + sizeof(header) + sizeof(footer)) {
      pos = 0;
      memcpy(&header, buffer, sizeof(header));
      memcpy(&footer, &buffer[sizeof(header) + sizeof(ahrs_msg)], sizeof(footer));
      if (header.type != 0) { continue; }
      if (footer.len != sizeof(header) + sizeof(ahrs_msg)) { continue; }
      if (strncmp(footer.postamble, "END", 3) != 0) { continue; };
      memcpy(&ahrs_msg, &buffer[sizeof(header)], sizeof(ahrs_msg));
      on_ahrs();
    }
  }
}

void on_ahrs() {
  last_message_time = millis();
  struct {
    float latitude = ahrs_msg.gps.latitude / 10e6;
    float longitude = ahrs_msg.gps.longitude / 10e6;
    float altitude = ahrs_msg.gps.msl_altitude / 100;
  } msg;
  esp_err_t result = esp_now_send(broadcastAddress, reinterpret_cast<uint8_t*>(&msg), sizeof(msg));
}

void loop() {
  if (millis() - last_message_time > 2000) {
    send_ping();
    neopixelWrite(12, 0, 0, 64);
    delay(100);
    neopixelWrite(12, 0, 0, 0);
    delay(100);
  } else {
    neopixelWrite(12, 0, 64, 0);
  }
  read();
}

