from ursina import Entity, color, Sky
import random

class BaseWorld:
    def __init__(self):
        self.create_ground()
        self.create_sky()
        self.create_objects()

    def create_ground(self):
        self.ground = Entity(
            model='plane',
            scale=100,
            color=color.green,
            texture='grass',
            collider='box'
        )

    def create_sky(self):
        self.sky = Sky(texture='sky_sunset')

    def create_objects(self):
        self.objects = []
        for i in range(10):
            obj = Entity(
                model='cube',
                color=color.random_color(),
                scale=2,
                position=(random.randint(-20, 20), 1, random.randint(-20, 20)),
                collider='box'
            )
            self.objects.append(obj)
