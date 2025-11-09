from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import color, Entity

class Player(FirstPersonController):
    def __init__(self, position=(0,1,0), speed=7, gravity=0.7, jump_height=1.5):
        super().__init__(
            model='cube',
            color=color.azure,
            origin_y=-0.5,
            speed=speed,
            collider='box',
            position=position
        )
        self.gravity = gravity
        self.jump_height = jump_height
