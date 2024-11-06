import machine
import utime

# Define sensor and motor control pins
right_sensor = machine.ADC(26)
center_sensor = machine.ADC(27)
left_sensor = machine.ADC(28)

left_motor_fwd = machine.Pin(20, machine.Pin.OUT)
left_motor_rev = machine.Pin(19, machine.Pin.OUT)
right_motor_fwd = machine.Pin(6, machine.Pin.OUT)
right_motor_rev = machine.Pin(7, machine.Pin.OUT)

left_motor_pwm_fwd = machine.PWM(left_motor_fwd)
right_motor_pwm_fwd = machine.PWM(right_motor_fwd)
left_motor_pwm_rev = machine.PWM(left_motor_rev)
right_motor_pwm_rev = machine.PWM(right_motor_rev)

# Set PWM frequency for motors
for pwm in [left_motor_pwm_fwd, right_motor_pwm_fwd, left_motor_pwm_rev, right_motor_pwm_rev]:
    pwm.freq(110)

# Button setup
toggle_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Motor speed control functions
def set_forward_speed(left_speed, right_speed):
    left_motor_pwm_fwd.duty_u16(left_speed)
    right_motor_pwm_fwd.duty_u16(right_speed)

def set_reverse_speed(left_reverse_speed, right_reverse_speed):
    left_motor_pwm_rev.duty_u16(left_reverse_speed)
    right_motor_pwm_rev.duty_u16(right_reverse_speed)

# Sensor reading function
def get_sensor_value(sensor):
    return sensor.read_u16()

# Movement functions
def move_forward():
    set_forward_speed(45000, 45000)
    set_reverse_speed(15000, 15000)

def turn_left():
    set_forward_speed(0, 12000)
    set_reverse_speed(15000, 5000)

def turn_right():
    set_forward_speed(12000, 0)
    set_reverse_speed(5000, 15000)

def halt():
    set_forward_speed(0, 0)
    set_reverse_speed(0, 0)

# Main loop with toggle button control
toggle_active = False
while True:
    left_val = get_sensor_value(left_sensor)
    center_val = get_sensor_value(center_sensor)
    right_val = get_sensor_value(right_sensor)
    print(f"Center: {center_val}  Left: {left_val}  Right: {right_val}")

    # Toggle button logic
    if toggle_button.value() == 1:
        toggle_active = not toggle_active
        print("Toggle on" if toggle_active else "Toggle off")
        utime.sleep(0.2)  # Debounce delay

    # Movement logic based on sensor values
    if toggle_active:
        if left_val > center_val + 2000 and left_val > right_val + 2000:
            turn_left()
        elif right_val > center_val + 2000 and right_val > left_val + 2000:
            turn_right()
        else:
            move_forward()
    else:
        halt()

    utime.sleep(0.01)
