from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import color, Entity

class Player(FirstPersonController):
    def __init__(self, position=(0,1,0), speed=7, gravity=0.7, jump_height=1.5):
        super().__init__(
            origin_y=-0.5,
            speed=speed,
            collider='box',
            position=position
        )
        self._base_gravity = gravity
        self.gravity = gravity
        self.jump_height = jump_height
        self._gravity_enabled = True

    def toggle_gravity(self):
        """Toggle gravity on/off. When off, set gravity to 0; when on restore original gravity."""
        self._gravity_enabled = not self._gravity_enabled
        self.gravity = self._base_gravity if self._gravity_enabled else 0
        print(f"Gravity {'enabled' if self._gravity_enabled else 'disabled'}")

    def update(self):
        """Extend base update: if gravity disabled, allow space to ascend smoothly."""
        super().update()
        if not self._gravity_enabled:
            from ursina import held_keys  # local import to avoid circular
            if held_keys['space']:
                # Ascend at a controlled rate
                self.y += 0.15
