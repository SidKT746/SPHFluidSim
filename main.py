# Importing the Taichi module to be able to compile the Python code
import taichi as ti

# Importing the Particle class
from Particle import Particle

# Initialising Taichi and telling it to use the GPU rather than the CPU.
ti.init(arch=ti.gpu)

Particles = []

# Set up the basic variables like the time difference (dt), number of substeps in the simulation.
n = 128
dt = 4e-2 / n
substeps = int(1 / 60 // dt)

# Setting up the properties of the ball
# The center of the ball is a vector and contained in a datatype called a vector field of floats.
ball_radius = 0.03
ball_center = ti.Vector.field(3, dtype=float, shape=(1,))
ball_center[0] = [0, 0, 0]

# Creating a window of size 1024x1024 with a black background
window = ti.ui.Window("Fluid Simulator", (1024, 1024), vsync=True)
canvas = window.get_canvas()
canvas.set_background_color((0, 0, 0))
scene = ti.ui.Scene()
camera = ti.ui.Camera()

# Creating a field for all the horizontal and vertical lines that define the domain of the fluid.
VerticalLines = [ti.Vector.field(3, dtype=ti.f32, shape=2) for x in range(4)]
HorizontalLines = [ti.Vector.field(3, dtype=ti.f32, shape=2) for x in range(4)]

# Set the co-ordinates of the lines so that the domain can be seen.


@ti.kernel
def InitPointsPos(Particles: list[]):
    VerticalLines[0][0] = [10, 0, 0]
    VerticalLines[0][1] = [10, 100, 0]
    VerticalLines[1][0] = [5, 0, 0]
    VerticalLines[1][1] = [5, 100, 0]
    VerticalLines[2][0] = [10, 0, -5]
    VerticalLines[2][1] = [10, 100, -5]
    VerticalLines[3][0] = [5, 0, -5]
    VerticalLines[3][1] = [5, 100, -5]

    HorizontalLines[0][0] = [10, 0, 0]
    HorizontalLines[0][1] = [5, 0, 0]
    HorizontalLines[1][0] = [5, 0, 0]
    HorizontalLines[1][1] = [5, 0, -5]
    HorizontalLines[2][0] = [5, 0, -5]
    HorizontalLines[2][1] = [10, 0, -5]
    HorizontalLines[3][0] = [10, 0, -5]
    HorizontalLines[3][1] = [10, 0, 0]

    InitParticles(Particles)


InitPointsPos(Particles)


@ti.func
def InitParticles(Particles):
    # Setting up the properties of the ball
    # The center of the ball is a vector and contained in a datatype called a vector field of floats.
    ParticleRadius = 0.02

    for i in range(1000):
        ParticleCenter = ti.Vector.field(3, dtype=float, shape=(1,))
        ParticleCenter[0] = [0.02 * (i * 1000//250), 1000 // 250, 1000 // 250]
        Particles.append(Particle(ParticleCenter[0], colour=(0.0, 0.0, 1)))


# Initialize the current time to be 0 (i.e. simulation starts now)
current_t = 0.0

while window.running:
    # Setup the position of the camera and determine which direction it looks in (in this case straight ahead).
    camera.position(-5, 2, 2)
    camera.lookat(0.0, 2, 0)
    scene.set_camera(camera)

    # Give a direction of where to point the light from and what color it should look like.
    scene.point_light(pos=(1, 1, 1), color=(1, 1, 1))
    scene.ambient_light((0.5, 0.5, 0.5))

    # Draw the ball.
    scene.particles(ball_center, radius=ball_radius *
                    0.95, color=(0.0, 0.0, 1))

    for i in Particles:
        # Draw the Sphere.
        scene.particles(i.position, radius=i.radius, color=i.colour)

    # Draw the line between the two points
    for i in range(4):
        scene.lines(VerticalLines[i], color=(0.28, 0.68, 0.99), width=5.0)
        scene.lines(HorizontalLines[i], color=(0.28, 0.68, 0.99), width=5.0)

    # Set the Scene to the new scene with the ball and line in it.
    canvas.scene(scene)

    # Show the window so that the scene is rendered.
    window.show()
