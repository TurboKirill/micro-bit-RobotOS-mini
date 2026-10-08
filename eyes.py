from microbit import sleep, button_a, button_b
import random

EYE_W = 38
EYE_H = 38
EYE_RADIUS = 3
CX1, CY1 = 35, 32
CX2, CY2 = 93, 32
_oled = None

def init(oled_instance):
    global _oled
    _oled = oled_instance

def _draw_round_rect(x, y, w, h, r):
    if h <= 4:
        _oled.fill_rect(x - w // 2, y - h // 2, w, max(h, 1), 1)
        return
    _oled.fill_rect(x - w // 2 + r, y - h // 2, w - 2 * r, h, 1)
    _oled.fill_rect(x - w // 2, y - h // 2 + r, w, h - 2 * r, 1)
    if r > 0:
        _oled.pixel(x - w // 2 + r, y - h // 2 + r, 1)
        _oled.pixel(x + w // 2 - r, y - h // 2 + r, 1)
        _oled.pixel(x - w // 2 + r, y + h // 2 - r, 1)
        _oled.pixel(x + w // 2 - r, y + h // 2 - r, 1)

def draw_eyes(x1, y1, w1, h1, x2, y2, w2, h2):
    _oled.fill(0)
    r1 = EYE_RADIUS if h1 > 8 else 0
    r2 = EYE_RADIUS if h2 > 8 else 0
    _draw_round_rect(x1, y1, w1, h1, r1)
    _draw_round_rect(x2, y2, w2, h2, r2)
    _oled.show()

def center():
    draw_eyes(CX1, CY1, EYE_W, EYE_H, CX2, CY2, EYE_W, EYE_H)

def sleep_mode():
    draw_eyes(CX1, CY1, EYE_W, 2, CX2, CY2, EYE_W, 2)

def wakeup():
    sleep_mode()
    sleep(200)
    for h in range(4, EYE_H + 1, 6):
        draw_eyes(CX1, CY1, EYE_W, h, CX2, CY2, EYE_W, h)
        sleep(20)
    center()

def blink(speed=15):
    center()
    sleep(30)
    draw_eyes(CX1, CY1, EYE_W, 2, CX2, CY2, EYE_W, 2)
    sleep(speed)
    center()

def look_right():
    draw_eyes(CX1 + 12, CY1, EYE_W, EYE_H, CX2 + 12, CY2, EYE_W + 4, EYE_H)
    sleep(600)
    center()

def look_left():
    draw_eyes(CX1 - 12, CY1, EYE_W + 4, EYE_H, CX2 - 12, CY2, EYE_W, EYE_H)
    sleep(600)
    center()

def happy():
    _oled.fill(0)
    _draw_round_rect(CX1, CY1, EYE_W, EYE_H, EYE_RADIUS)
    _draw_round_rect(CX2, CY2, EYE_W, EYE_H, EYE_RADIUS)
    _oled.fill_rect(10, 36, 110, 20, 0)
    _oled.show()

def sad():
    _oled.fill(0)
    _draw_round_rect(CX1, CY1, EYE_W, EYE_H, EYE_RADIUS)
    _draw_round_rect(CX2, CY2, EYE_W, EYE_H, EYE_RADIUS)
    _oled.fill_rect(10, 10, 110, 18, 0)
    _oled.show()

def saccade():
    for _ in range(5):
        dx = random.randint(-6, 6)
        dy = random.randint(-3, 3)
        draw_eyes(CX1 + dx, CY1 + dy, EYE_W, EYE_H, CX2 + dx, CY2 + dy, EYE_W, EYE_H)
        sleep(60)
    center()

def idle_tick():
    r = random.randint(1, 15)
    if r == 1: blink(20)
    elif r == 2: look_right()
    elif r == 3: look_left()
    elif r == 4: saccade()

def run_app():
    ANIMS = [("CENTER", center), ("BLINK", blink), ("HAPPY", happy),
             ("SAD", sad), ("RIGHT", look_right), ("LEFT", look_left),
             ("SACCADE", saccade), ("SLEEP", sleep_mode), ("WAKEUP", wakeup)]
    idx = 0
    center()
    _oled.text(ANIMS[idx][0], 10, 56)
    _oled.show()
    button_a.was_pressed()
    button_b.was_pressed()
    while True:
        if button_a.was_pressed():
            idx = (idx + 1) % len(ANIMS)
            ANIMS[idx][1]()
            _oled.text(ANIMS[idx][0], 10, 56)
            _oled.show()
            sleep(150)
        if button_b.was_pressed():
            break
        sleep(40)