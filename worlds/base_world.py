"""Procedural base world.

Generates a small, mostly flat irregular disk with gentle hills using a seed.
"""

from math import atan2, pi, cos, sin
from ursina import Entity, color, Sky, Mesh
from perlin_noise import PerlinNoise
import random


class BaseWorld:
    def __init__(self, seed: int | None = None, radius: int = 50, grid_step: int = 2,
                 height_amp: float = 4.0, height_freq: float = 0.03):
        """Create the world.

        Args:
            seed: Seed for deterministic generation (random if None).
            radius: Approximate radius of the disk (base radius before perturbation).
            grid_step: Spacing between sample points on the XZ grid.
            height_amp: Maximum hill height amplitude.
            height_freq: Frequency scaling for Perlin noise heights.
        """
        self.seed = seed if seed is not None else random.randint(0, 1_000_000)
        self.random = random.Random(self.seed)
        self.radius = radius
        self.grid_step = grid_step
        self.height_amp = height_amp
        self.height_freq = height_freq

        # Noise instances (low frequency for radial distortion, higher for height variation)
        self.height_noise = PerlinNoise(octaves=3, seed=self.seed)
        self.radial_noise = PerlinNoise(octaves=2, seed=self.seed + 1337)

        self.create_ground()
        self.create_sky()

    # ------------------- Generation -------------------
    def _smoothed_radial_profile(self, segments: int) -> list[float]:
        """Generate a smoothed list of radial distances for each angular segment.

        Uses Perlin noise sampled around the circle and applies a simple moving
        average to reduce jaggedness while retaining organic shape.
        """
        raw = []
        for i in range(segments):
            a01 = i / segments
            perturb = self.radial_noise([a01, 0]) * (self.radius * 0.15)
            raw.append(self.radius + perturb)
        # Moving average smoothing (wrap-around)
        window = 3
        smooth = []
        for i in range(segments):
            acc = 0
            for w in range(-window, window + 1):
                acc += raw[(i + w) % segments]
            smooth.append(acc / (2 * window + 1))
        return smooth

    def _height(self, x: float, z: float) -> float:
        # Gentle hills using Perlin noise; center bias keeps middle relatively flat
        h = self.height_noise([x * self.height_freq, z * self.height_freq]) * self.height_amp
        return h

    def create_ground(self):
        """Create a smoothed irregular disk mesh with gentle hills using polar sampling."""
        radial_segments = 64  # angular resolution
        ring_count = int(self.radius / self.grid_step)
        radial_profile = self._smoothed_radial_profile(radial_segments)

        vertices = []
        uvs = []
        # Store indices per ring/segment for triangulation
        index_ring = []

        for ring in range(ring_count + 1):
            ring_indices = []
            t = ring / ring_count  # 0 center -> 1 outer edge
            for seg in range(radial_segments):
                angle = (seg / radial_segments) * 2 * pi
                max_r = radial_profile[seg]
                r = max_r * t
                x = cos(angle) * r
                z = sin(angle) * r
                y = self._height(x, z) * (0.2 + 0.8 * t)  # slight attenuation near center
                idx = len(vertices)
                vertices.append((x, y, z))
                # UV radial projection
                u = (cos(angle) * r + self.radius) / (2 * self.radius)
                v = (sin(angle) * r + self.radius) / (2 * self.radius)
                uvs.append((u, v))
                ring_indices.append(idx)
            index_ring.append(ring_indices)

        triangles = []
        for ring in range(ring_count):
            curr_ring = index_ring[ring]
            next_ring = index_ring[ring + 1]
            for seg in range(radial_segments):
                a = curr_ring[seg]
                b = curr_ring[(seg + 1) % radial_segments]
                c = next_ring[seg]
                d = next_ring[(seg + 1) % radial_segments]
                # Two triangles a,c,d and a,d,b
                triangles.extend((a, c, d, a, d, b))

        mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, static=True)
        mesh.generate_normals()

        self.ground = Entity(
            model=mesh,
            collider='mesh',
            color=color.green.tint(-0.05),
            texture='grass'
        )

    def create_sky(self):
        self.sky = Sky(texture='sky_sunset')

    # ------------------- Public API -------------------
    def regenerate(self, seed: int | None = None):
        """Regenerate terrain with an optional new seed."""
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 1_000_000)
        self.random = random.Random(self.seed)
        self.height_noise = PerlinNoise(octaves=3, seed=self.seed)
        self.radial_noise = PerlinNoise(octaves=2, seed=self.seed + 1337)
        # Destroy old entity
        if hasattr(self, 'ground') and self.ground:
            self.ground.disable()
        self.create_ground()
        return self.seed