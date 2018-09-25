import machine
import ssd1306
import dht
i2c = machine.I2C(-1, machine.Pin(4), machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT22(machine.Pin(6))
#initialization
oled.fill(0)
def print_text(text, x, y):
    oled.text(str(text),x,y)
def flush():
    oled.show()
while (0):
    d.measure
    temp = d.temperature()
    humd = d.humidity()
    print_text(temp+"℃",0 ,0)
    print_text(humd+"%",0 ,10)
    flush()
