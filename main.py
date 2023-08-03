# Importing the Taichi module to be able to compile the Python code
import taichi as ti

# Initialising Taichi and telling it to use the GPU rather than the CPU.
ti.init(arch=ti.gpu)

# Set up the basic vairables like the time difference(dt), number of substeps in the simulation.
n = 128
dt = 4e-2 / n
substeps = int(1 / 60 // dt)

# Setting up the properties of the ball
# The centre of the ball is a vector and contained in a datatype called a vector field of floats.
ball_radius = 0.03
ball_centre = ti.Vector.field(3, dtype=float, shape=(1, ))
ball_centre[0] = [0, 0, 0]

# Creating a window of size 1024x1024 with black background
window = ti.ui.Window("Fluid Simulator",
                      (1024, 1024), vsync=True)
canvas = window.get_canvas()
canvas.set_background_color((0, 0, 0))
scene = ti.ui.Scene()
camera = ti.ui.Camera()

# Initialise the current time to be 0(i.e simulation starts now)
current_t = 0.0

while window.running:

    # Setup the position of the camera and determine which direction it looks in(in this case straight ahead).
    camera.position(0.0, 0.0, 3)
    camera.lookat(0.0, 0.0, 0)
    scene.set_camera(camera)

    # Give a direction of where to point the light from and what colour it should look like.
    scene.point_light(pos=(1, 1, 1), color=(1, 1, 1))
    scene.ambient_light((0.5, 0.5, 0.5))

    # Draw the ball.
    scene.particles(ball_centre, radius=ball_radius *
                    0.95, color=(0.0, 0.0, 1))

    # Set the Scene to the new scene with ball in it.
    canvas.scene(scene)

    # Show the window so that the scene is rendered.
    window.show()
