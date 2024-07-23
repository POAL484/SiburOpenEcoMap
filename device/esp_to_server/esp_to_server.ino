#include <ESP8266HTTPClient.h>
#include <ArduinoWiFiServer.h>
#include <BearSSLHelpers.h>
#include <CertStoreBearSSL.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiGratuitous.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiClientSecureBearSSL.h>
#include <WiFiServer.h>
#include <WiFiServerSecure.h>
#include <WiFiServerSecureBearSSL.h>
#include <WiFiUdp.h>
//подключаем библиотеку WiFi и HTTP клиент
#include <SoftwareSerial.h>        //подключение esp по своему сериал
SoftwareSerial espSerial(13, 14);  //передача данных в esp по RX5 и TX6 пинам

const char* ssid = "HUAWEI P20 Pro";  //имя сети
const char* password = "agbdlcid15";  //пароль

//доменное имя с UID
String serverName = "http://siburok.ru:1883/devicelive/872b05d7-f038-45a7-8b74-168fb88ecff3/";
String massage = "LPG=6_C6H6=66_C6H6O=12_C4H1O=72_C3H8=122_temp=24.04_pressure=100907.40";  //тут живут данные от датчиков
String pretext = "";                                                                        //текст в конце сообщения.
unsigned long lastTime = 0;                                                                 //время для периодической отправки данных
unsigned long timerDelay = 30 * 1000;                                                       //интервал отправки данных
int vol;                                                                                    //0 - не надо брать пробы, 1 - пробу осадков, 2 - пробу воды, 3 - пробы.
void setup() {
  pinMode(4, OUTPUT);  // пин набора осадков
  pinMode(5, OUTPUT);  //пин набора воды
  digitalWrite(4, 1);
  digitalWrite(5, 1);
  espSerial.begin(115200);       //открываем UART в ESP на скорости 115200
  Serial.begin(115200);          //настраиваем UART для отправки данных в ПК
  WiFi.begin(ssid, password);    //подключаемся к WiFi
  Serial.println("Connecting");  //говорим о том, что подключаемся
  //пишем точки пока не подключились
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();  //перенос строки
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());  //пишем IP
}

void loop() {
  //отправляем HTTP GET request с заданной периодичностью
  if ((millis() - lastTime) > timerDelay) {
    vol = senddata();     //отправка показаний датчиков на сервер и возрат отбора воды
    lastTime = millis();  //запоминаем время послежней отправки данных
  }
  uarttoesp();  //читаем показания датчиков

  //отправляем ответ на сервер о том, что забираем пробу
  // if (vol > 0) { sendprobe(vol); }  //отправить ответ серверу о том, что инфа о пробе принята
}


//отправляем данные показаний датчиков на сервер
int senddata() {
  //Check WiFi connection status
  String incomm = "";
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    // Your Domain name with URL path or IP address with path
    http.begin(client, serverName + massage);  //тело запроса
    // добавляем хэдэр
    http.addHeader("Token", "872b05d7-f038-45a7-8b74-168fb88ecff3 994f9745b96a19-4--05961-0fd42-c47016b3f79b62-3ca9abf0-034ecc49d5d5cc-efa");
    int httpResponseCode = http.GET();  //делаем GET запрос и получаем статус от сервера
    Serial.println(massage);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);  //печатаем статус ответа от сервера
    incomm = http.getString();         //0 - не надо брать пробу, 1 пробу дождя, 10 пробу воды, 11 все пробы
    Serial.println(incomm);            //выводим необходимость отбора проб из водоема и осадков
    http.end();                        //завершаем передачу данных
  } else {
    Serial.println("WiFi Disconnected");
  }
  //ворачиваем требуемую пробу
  if (incomm == "1") {
    return 1;
  } else if (incomm == "10") {
    return 2;
  } else if (incomm == "11") {
    return 3;
  } else {
    return 0;
  }
}

//принимаем показания датчиков по uart в esp
void uarttoesp() {
  //принимаем посылку от датчиков
  if (espSerial.available()) {
    String temp = "";                       //временное хранение
    for (int i =0; i<20; i++) 
   {
      temp += char(int(espSerial.read()));  //добавляем символ во временную строку
   } 
    while (espSerial.available()) {         //пока есть данные
      temp += char(int(espSerial.read()));  //добавляем символ во временную строку
    }
    
    if (temp[0] == 'L') {
      massage = temp;  //переписываем показания датчиков, если посылка не пустая
      // Serial.println(massage); //выводим посылку
    }
  }
}

void sendprobe(int tip) {
  //tip: 0 - не нужна, 1 - проба дожды, 2 - проба воды, 3 - пробы
  answercol();  //отправляем ответ с ?col=1
                //делаем анимацию набора соответствущей пробы воды
  if (tip == 1) {
    digitalWrite(4, 0);//делаем анимацию набора осадков
  
  } else if (tip == 2) {
    digitalWrite(5, 0); //делаем анимацию набора воды
  } else {
    digitalWrite(4, 0); //делаем анимацию набора осадков
    digitalWrite(5, 0); //делаем анимацию набора воды
  }
  delay(10000); //ждем 20 сек анимации
  //отправляем соответствующий гет
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    // Your Domain name with URL path or IP address with path
    if (tip==1) {http.begin(client, serverName + "rain");}  //тело запроса
    else if (tip==2) {http.begin(client, serverName + "lake");}  //тело запроса
    else {http.begin(client, serverName + "all");}  //тело запроса
    
    // добавляем хэдэр
    http.addHeader("Token", "872b05d7-f038-45a7-8b74-168fb88ecff3 994f9745b96a19-4--05961-0fd42-c47016b3f79b62-3ca9abf0-034ecc49d5d5cc-efa");
    int httpResponseCode = http.GET();  //делаем GET запрос и получаем статус от сервера
    Serial.println(massage);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);  //печатаем статус ответа от сервера
    http.end();                        //завершаем передачу данных
  }
  //ждем от сервера инфу о том, что прилетел дрон
  while (senddata()==0) {delay(10000);}
  //делаем соответствующую анимацию
  digitalWrite(4, 1);
  digitalWrite(5, 1);
  delay(20000);
  answercol();  //отправляем ответ с ?col=1
}

//ответ о том, что начинаем отбор пробы воды
void answercol() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    // Your Domain name with URL path or IP address with path
    http.begin(client, serverName + massage + "?col=1");  //тело запроса
    // добавляем хэдэр
    http.addHeader("Token", "872b05d7-f038-45a7-8b74-168fb88ecff3 994f9745b96a19-4--05961-0fd42-c47016b3f79b62-3ca9abf0-034ecc49d5d5cc-efa");
    int httpResponseCode = http.GET();  //делаем GET запрос и получаем статус от сервера
    Serial.println(massage);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);  //печатаем статус ответа от сервера
    http.end();                        //завершаем передачу данных
  } else {
    Serial.println("WiFi Disconnected");
  }
}