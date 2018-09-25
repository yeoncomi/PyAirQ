import machine
import ssd1306
import dht
import time
i2c = machine.I2C(-1, machine.Pin(4), machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT22(machine.Pin(6))
dust = machine.ADC(0)
#initialization
oled.fill(0)
def print_text(text, x, y):
    oled.text(str(text),x,y)
def flush():
    oled.show()
class led:
    def __init__(self, pin_r, pin_g, pin_b):
            self.pin_r = machine.PWM(machine.Pin(pin_r))
            self.pin_g = machine.PWM(machine.Pin(pin_g))
            self.pin_b = machine.PWM(machine.Pin(pin_b))
    def setup(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.duty()
    def duty(self):
        self.pin_r.duty(self.duty_translate(self.r))
        self.pin_g.duty(self.duty_translate(self.g))
        self.pin_b.duty(self.duty_translate(self.b))
    def duty_translate(self, n):
        return int((float(n) / 255)*1023)
LED = led(Pin_R, Pin_G, Pin_B)
dust_d = dust.read()
while True:
    d.measure
    temp = d.temperature()
    humd = d.humidity()
    print_text(temp+"℃",0 ,0)
    print_text(humd+"%",0 ,10)
    dustdensity = (0.172*(dust_d*(5/1024.0))-0.0999)*1000
    print_text(dustdensity+"ug/m3 ", 0, 20)
    if dustdensity > 25 :
        led.setup(255,0,0)
    elif dustdensity < 25 :
        if dustdensity < 15:
            if dustdensity < 5:
                led.setup(0,0,255)
            if dustdensity > 5:
                led.setup(0,255,0)
        if dustdensity > 15:
            led.setup(0,255,0)
    flush()
    time.sleep(1)
