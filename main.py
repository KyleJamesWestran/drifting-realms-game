from ursina import Ursina, mouse
from core.player import Player
from worlds.base_world import BaseWorld
import time

app = Ursina()

# Initialize world and player with a time-based seed
initial_seed = int(time.time()) % 1_000_000
world = BaseWorld(seed=initial_seed)
player = Player(position=(0,1,0))

mouse.locked = True  # lock mouse to the window
mouse.visible = False  # hide the cursor

# --- Escape key handling ---
def input(key):
    if key == 'escape':
        mouse.locked = not mouse.locked  # toggle mouse lock
        mouse.visible = not mouse.visible  # toggle cursor visibility
    if key == 'r':  # regenerate terrain with new random seed
        new_seed = world.regenerate()
        print(f"World regenerated with seed {new_seed}")
    if key == 'g':  # toggle gravity
        player.toggle_gravity()

app.run()
