import pyglet
from pyglet.gl import *
import math

# Window settings
WIDTH, HEIGHT = 900, 700
window = pyglet.window.Window(WIDTH, HEIGHT, "Animated Background")

# Wave animation variables
wave_offset = 0
wave_speed = 0.1
amplitude = 50  # Wave height
frequency = 0.05  # Wave frequency

@window.event
def on_draw():
    global wave_offset
    window.clear()
    glBegin(GL_POINTS)
    for y in range(0, HEIGHT, 20):  # Wave spacing
        for x in range(0, WIDTH, 10):  # Point spacing
            wave = math.sin((x * frequency) + wave_offset) * amplitude
            glVertexP2ui(x, y + wave)
    glEnd()
    wave_offset += wave_speed

# Run the application
pyglet.app.run()
