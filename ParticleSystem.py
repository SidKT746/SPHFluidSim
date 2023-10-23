import taichi as ti


class ParticleSystem():
    def __init__(self, particleRadius, numParticles):
        # Setting up the properties of the ball
        # The center of the ball is a vector and contained in a datatype called a vector field of floats.
        self.particleRadius = particleRadius
        self.numParticles = numParticles
        self.particleCenters = ti.Vector.field(
            3, dtype=float, shape=(self.numParticles,))

        for i in range(self.numParticles):
            self.particleCenters[i] = [i/50, i/50, i/50]
