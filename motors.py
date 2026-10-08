from microbit import pin0, pin1, pin2, sleep, button_a, button_b

pin0.set_analog_period(20)
pin1.set_analog_period(20)
pin2.set_analog_period(20)

bucket_angle = 0
s2_running = False
s3_running = False

def angle_to_analog(angle):
    angle = max(0, min(180, angle))
    return int(25 + (angle / 180.0) * 100)

def set_bucket(angle):
    global bucket_angle
    bucket_angle = max(0, min(90, angle))
    pin0.write_analog(angle_to_analog(bucket_angle))

def bucket_down():
    bucket_smooth(0)

def bucket_smooth(target_angle, delay_ms=15):
    global bucket_angle
    target_angle = max(0, min(90, target_angle))
    step = 1 if target_angle > bucket_angle else -1
    for a in range(bucket_angle, target_angle + step, step):
        set_bucket(a)
        sleep(delay_ms)

def toggle_bucket():
    if bucket_angle < 45: bucket_smooth(90)
    else: bucket_smooth(0)

def toggle_left_wheel():
    global s2_running
    s2_running = not s2_running
    pin1.write_analog(angle_to_analog(40 if s2_running else 90))

def toggle_right_wheel():
    global s3_running
    s3_running = not s3_running
    pin2.write_analog(angle_to_analog(140 if s3_running else 90))

def stop():
    global s2_running, s3_running
    s2_running = False
    s3_running = False
    pin1.write_analog(angle_to_analog(90))
    pin2.write_analog(angle_to_analog(90))

# --- ИСПРАВЛЕННЫЕ НАПРАВЛЕНИЯ ДВИЖЕНИЯ ---

def forward(speed=80):
    """Езда ВПЕРЁД"""
    pin1.write_analog(angle_to_analog(90 + int(speed * 0.7)))
    pin2.write_analog(angle_to_analog(90 - int(speed * 0.7)))

def backward(speed=80):
    """Езда НАЗАД"""
    pin1.write_analog(angle_to_analog(90 - int(speed * 0.7)))
    pin2.write_analog(angle_to_analog(90 + int(speed * 0.7)))

def turn_left(speed=80):
    """Разворот НАЛЕВО на месте"""
    pin1.write_analog(angle_to_analog(90 - int(speed * 0.7)))
    pin2.write_analog(angle_to_analog(90 - int(speed * 0.7)))

def turn_right(speed=80):
    """Разворот НАПРАВО на месте"""
    pin1.write_analog(angle_to_analog(90 + int(speed * 0.7)))
    pin2.write_analog(angle_to_analog(90 + int(speed * 0.7)))

def run_app(oled):
    ITEMS = ["S1 BUCKET", "S2 LEFT", "S3 RIGHT", "EXIT"]
    cur = 0
    button_a.was_pressed()
    button_b.was_pressed()

    def draw_ui():
        oled.fill(0)
        oled.fill_rect(0, 0, 128, 11, 1)
        oled.text("-- SERVO TEST --", 14, 2, 0)
        for i in range(len(ITEMS)):
            p = "> " if i == cur else "  "
            if i == 0: st = "[UP]" if bucket_angle > 45 else "[DOWN]"
            elif i == 1: st = "[ON]" if s2_running else "[OFF]"
            elif i == 2: st = "[ON]" if s3_running else "[OFF]"
            else: st = ""
            oled.text(p + ITEMS[i] + " " + st, 4, 16 + i * 12)
        oled.show()

    draw_ui()

    while True:
        if button_a.was_pressed():
            cur = (cur + 1) % len(ITEMS)
            draw_ui()
            sleep(150)

        if button_b.was_pressed():
            if cur == 0:
                toggle_bucket()
                draw_ui()
            elif cur == 1:
                toggle_left_wheel()
                draw_ui()
            elif cur == 2:
                toggle_right_wheel()
                draw_ui()
            elif cur == 3:
                stop()
                break
            sleep(180)

        sleep(40)