import Jetson.GPIO as GPIO
import time
## this if enoder plug directly to jetson
ABS_PIN = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ABS_PIN, GPIO.IN)

def measure_duty_cycle(pin):
    # timeout is positional, in milliseconds
    result = GPIO.wait_for_edge(pin, GPIO.RISING, timeout=50)
    if result is None:
        return None
    t_rise = time.perf_counter()

    result = GPIO.wait_for_edge(pin, GPIO.FALLING, timeout=50)
    if result is None:
        return None
    t_fall = time.perf_counter()

    result = GPIO.wait_for_edge(pin, GPIO.RISING, timeout=50)
    if result is None:
        return None
    t_next_rise = time.perf_counter()

    pulse_width = t_fall - t_rise
    period = t_next_rise - t_rise

    if period <= 0:
        return None

    duty = pulse_width / period
    angle_deg = duty * 360.0
    return angle_deg

try:
    while True:
        angle = measure_duty_cycle(ABS_PIN)
        if angle is not None:
            print(f"Angle: {angle:.1f}°")
        else:
            print("No signal detected — check wiring")
        time.sleep(0.05)
finally:
    GPIO.cleanup()