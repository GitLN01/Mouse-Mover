import time
import threading
import pynput.mouse
import math
from flask import Flask, render_template
from screeninfo import get_monitors

app = Flask(__name__)

mouse = pynput.mouse.Controller()
moving = False
thread = None

@app.route('/')
def index():
    return render_template('index.html')

def move_mouse():
    screen_width, screen_height = get_screen_dimensions()
    interval = 0.05  # Time in seconds between each mouse movement
    radius = min(screen_width, screen_height) / 3
    angle = 0

    while moving:
        # Calculate new position for the mouse along a circular path
        new_x = int(screen_width / 2 + radius * math.cos(angle))
        new_y = int(screen_height / 2 + radius * math.sin(angle))

        # Move the mouse
        mouse.position = (new_x, new_y)
        angle += 0.01  # Increment angle for next position

        time.sleep(interval)

def on_click(x, y, button, pressed):
    global moving, thread
    if pressed:
        moving = False
        thread.join()
        return False  # Stop listener

def get_screen_dimensions():
    monitor = get_monitors()[0]  # Get the primary monitor
    return monitor.width, monitor.height

@app.route('/start')
def start_mouse_movement():
    global moving, thread
    if not moving:
        moving = True
        thread = threading.Thread(target=move_mouse)
        thread.start()

        listener_thread = threading.Thread(target=listen_for_mouse_events)
        listener_thread.start()

        return "Mouse movement started"
    return "Mouse movement is already started"

def listen_for_mouse_events():
    with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == '__main__':
    app.run(debug=True)
