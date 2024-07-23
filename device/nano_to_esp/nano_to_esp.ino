#include <GyverBME280.h>         //подключение барометра 
#include <SoftwareSerial.h>      //подключение esp по своему сериал 
GyverBME280 bme;                 //создаем объект класса с имененем bme 
SoftwareSerial espSerial(5, 6);  //передача данных в esp по 5 и 6 пинам 
String str;                      //сюда пишем посылку 
void setup() { 
  espSerial.begin(115200);     //открываем UART в ESP на скорости 115200 
  Serial.begin(9600);          //открываем UART в комп на скорости 9600 
  Serial.println("START");     //пишем посылку в комп 
  delay(500);                  //ждем 
  if (!bme.begin(0x76)) {      //проверяем адрес 76 
    Serial.println("Error!");  //пишем посылку 
  } else { 
    Serial.println("OK");  //пишем посылку 
  } 
} 
 
void loop() { 
  //составляем посылку 
  str = "LPG=" + String(analogRead(A0)) + "_C6H6=" + String(analogRead(A1)) + "_C6H6O=" + String(analogRead(A2)) + "_C4H10=" + String(analogRead(A3)) + "_C3H8=" + String(analogRead(A7)) + "_temp=" + String(bme.readTemperature()) + "_pressure=" + String(bme.readPressure()); 
  Serial.println(str);     //отправляем посылку в комп 
  espSerial.println(str);  //отправляем посылку в esp 
  delay(1000);              //ждем 
}