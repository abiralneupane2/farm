#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include "ESPAsyncTCP.h"
#include "ESPAsyncWebServer.h"
#include "ArduinoJson.h"
#include "DHTesp.h"
#include <ESP8266HTTPClient.h>


DHTesp dht;
#define STASSID "9860560067_2.4"
#define STAPSK  "CLFBD5BC09"
String humidityValue, temperatureValue;
const int dhtPin=5;
String ssid = "Aditi";
String password =  "0305098076";
const char* device_id = "test";
const char* PARAM_INPUT_1 = "output";
const char* PARAM_INPUT_2 = "state";
const char* host = "http://192.168.1.65:8000/data/";

AsyncWebServer server(80);
HTTPClient http;
bool is_authenticated(AsyncWebServerRequest *request) {
  if(request->hasHeader("Cookie")){
      AsyncWebHeader* h = request->getHeader("Cookie");
      String cookie = h->value().c_str();
      Serial.println(cookie);
      if (cookie.indexOf("ESPSESSIONID=1") != -1) {
        Serial.println("Authentication Successful");
      return true;
      }
    }
  Serial.println("Authentication Failed");
  AsyncWebServerResponse *response = request->beginResponse(401);
  Serial.println("redirect to login");
  request->redirect("/login");
  request->send(response);
}





void dataHandler(AsyncWebServerRequest *request){
  if(is_authenticated(request)){
    Serial.println("Handle data");
    
    
    // GET input1 value on <ESP_IP>/update?output=<inputMessage1>&state=<inputMessage2>
    if (request->hasArg(PARAM_INPUT_1) && request->hasArg(PARAM_INPUT_2)) {
      String inputMessage1;
      String inputMessage2;
      inputMessage1 = request->arg(PARAM_INPUT_1);
      inputMessage2 = request->arg(PARAM_INPUT_2);
      Serial.println(inputMessage1 + ":" + inputMessage2);
      digitalWrite(inputMessage1.toInt(), inputMessage2.toInt());
      request->send(200);
      return;
    }
    request->send(200, "text/plain", "OK");
    return;
  }
  
}




void configurationServer(){
  Serial.println(WiFi.localIP());
  server.on("/state", dataHandler);
  server.begin();
  }
  
void setup(){
  
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  delay(1000);
  while(WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.print(".");
  }
  dht.setup(dhtPin, DHTesp::DHT11);
  Serial.println(dht.getMinimumSamplingPeriod());
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
  configurationServer();

  
  
}
void loop(){
  humidityValue = String(dht.getHumidity());
  temperatureValue = String(dht.getTemperature());
  String post = "id=" + (String)device_id + "&temperature=" + temperatureValue + "&humidity=" + humidityValue;
  sendPostRequest(post);
  Serial.println("Temperature = " + temperatureValue + "\t Humidity = " + humidityValue );
  delay(3000);
}

void sendPostRequest(String post){
    http.begin(host);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); 
    int httpCode = http.POST(post);
    String payload = http.getString();
    Serial.println(httpCode);
    http.end();
  }
