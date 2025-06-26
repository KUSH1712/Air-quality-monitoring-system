


//gas detection simulation on streamlit


#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Air6952";
const char* password = "113344";
const char* serverURL = "http://192.168.1.9:5000/upload"; 

const int mq135Pin = 34;  // pin definition

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  int sensorValue = analogRead(mq135Pin);
  float voltage = sensorValue * (3.3 / 4095.0); // formula to convert voltage value

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"value\":" + String(voltage, 2) + "}";
    Serial.print("Sending: ");
    Serial.println(payload);

    int httpCode = http.POST(payload);
    Serial.print("HTTP Code: ");
    Serial.println(httpCode);
    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response);
    }
    http.end();
  }

  delay(5000); // 5000=5sec
}

