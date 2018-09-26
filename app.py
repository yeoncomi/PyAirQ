import machine
import ssd1306
import dht
import time
from ntptime import settime
import network
import utime

i2c = machine.I2C(-1, machine.Pin(4), machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT22(machine.Pin(6))
dust = machine.ADC(0)

tempo = 5
tones = {
    'c': 262,
    'd': 294,
    'e': 330,
    'f': 349,
    'g': 392,
    'a': 440,
    'b': 494,
    'C': 523,
    ' ': 0,
}
beeper = machine.PWM(Pin(7, Pin.OUT), freq=440, duty=512)
melody = 'cdefgabC'
rhythm = [8, 8, 8, 8, 8, 8, 8, 8]

# initialization
oled.fill(0)


def print_text(text, x, y):
    oled.text(str(text), x, y)


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

led.__init__(1, 2, 3)


def do_connect(bssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(str(bssid), str(password))
        while not sta_if.isconnected():
            pass
do_connect("ssid", "password")
# loop
while True:
    d.measure
    temp = d.temperature()
    humd = d.humidity()
    dust_d = dust.read()
    settime()
    (yr, mth, day, hr, m, s, w, yd) = utime.localtime()
    print_text(temp+"℃",  0, 0)
    print_text(humd+"%", 0, 10)
    dustdensity = (0.172*(dust_d*(5/1024.0))-0.0999)*1000
    print_text(dustdensity+"ug/m3 ", 0, 20)
    print_text(yr + '/' + mth + '/' + day, 60, 0)
    print_text(hr+':'+m, 60, 10)
    if dustdensity > 25:
        led.setup(255, 0, 0)
        if dustdensity > 65:
            for tone, length in zip(melody, rhythm):
                beeper.freq(tones[tone])
                time.sleep(tempo/length)
    elif dustdensity < 25:
        if dustdensity < 15:
            if dustdensity < 5:
                led.setup(0, 0, 255)
            if dustdensity > 5:
                led.setup(0, 255, 0)
        if dustdensity > 15:
            led.setup(0, 255, 0)
    flush()
    time.sleep(1)
