from ursina import Ursina, mouse
from core.player import Player
from worlds.base_world import BaseWorld

app = Ursina()

# Initialize world and player
world = BaseWorld()
player = Player(position=(0,1,0))

mouse.locked = True  # lock mouse to the window
mouse.visible = False  # hide the cursor

# --- Escape key handling ---
def input(key):
    if key == 'escape':
        mouse.locked = not mouse.locked  # toggle mouse lock
        mouse.visible = not mouse.visible  # toggle cursor visibility

app.run()
