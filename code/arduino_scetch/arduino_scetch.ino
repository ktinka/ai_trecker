#include <Wire.h>

const int MPU_ADDR = 0x68;

float accX, accY, accZ;
int16_t tempRaw;
float gyroX, gyroY, gyroZ;
const float VAL_acc = 16384.0;
const float VAL_gyro = 131.0;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  //MPU-6050 rising
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  //Serial.println("time_ms, accX, accY, accZ, gyroX, gyroY, gyroZ");

}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);

  //Serial.print("Акселерометр: ");

  accX = (Wire.read() << 8 | Wire.read()) / VAL_acc;
  accY = (Wire.read() << 8 | Wire.read()) / VAL_acc;
  accZ = (Wire.read() << 8 | Wire.read()) / VAL_acc;

  float min_border = -0.7;
  float max_border = 1.1;

  //Serial.print("x: ");
  Serial.print(accX);
  Serial.print(",");

  //Serial.print("y: ");
  Serial.print(accY);
  Serial.print(",");

  //Serial.print("z: ");
  Serial.print(accZ);
  Serial.print(",");

  //Serial.print("  Температура: ");
  tempRaw = Wire.read() << 8 | Wire.read();
  Serial.print(tempRaw);
  Serial.print(",");

  //Serial.println(". Героскоп: ");

  gyroX = (Wire.read() << 8 | Wire.read()) / VAL_gyro * (3.14/180.0);
  gyroY = (Wire.read() << 8 | Wire.read()) / VAL_gyro * (3.14/180.0);
  gyroZ = (Wire.read() << 8 | Wire.read()) / VAL_gyro * (3.14/180.0);

  //Serial.print(" ^x: ");
  Serial.print(gyroX);
  Serial.print(",");

  //Serial.print(" ^y: ");
  Serial.print(gyroY);
  Serial.print(",");

  //Serial.print(" ^z: ");
  Serial.print(gyroZ);
  Serial.println();


  delay(30);
}
