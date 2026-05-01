from machine import Pin, I2C
import bme280

def init_sensor():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
    sensor = bme280.BME280(i2c=i2c, address=0x76)
    return sensor

def read_sensor(sensor):
    temp, pressure, humidity = sensor.values
    return {
        "temp": temp,
        "pressure": pressure,
        "humidity": humidity
    }
