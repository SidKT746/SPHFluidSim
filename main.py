# Importing the Taichi module to be able to compile the Python code
import taichi as ti

# Initialising Taichi and telling it to use the GPU rather than the CPU.
ti.init(arch=ti.gpu)

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

verticalLines = [ti.Vector.field(3, dtype=ti.f32, shape=2) for x in range(4)]
horizontalLines = [ti.Vector.field(3, dtype=ti.f32, shape=2) for x in range(4)]


@ti.kernel
def init_points_pos():
    verticalLines[0][0] = [10, 0, 0]
    verticalLines[0][1] = [10, 10, 0]
    verticalLines[1][0] = [5, 0, 0]
    verticalLines[1][1] = [5, 10, 0]
    verticalLines[2][0] = [10, 0, -5]
    verticalLines[2][1] = [10, 10, -5]
    verticalLines[3][0] = [5, 0, -5]
    verticalLines[3][1] = [5, 10, -5]

    horizontalLines[0][0] = [10, 0, 0]
    horizontalLines[0][1] = [5, 0, 0]
    horizontalLines[1][0] = [5, 0, 0]
    horizontalLines[1][1] = [5, 0, -5]
    horizontalLines[2][0] = [5, 0, -5]
    horizontalLines[2][1] = [10, 0, -5]
    horizontalLines[3][0] = [10, 0, -5]
    horizontalLines[3][1] = [10, 0, 0]


init_points_pos()

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

    # Draw the line between the two points
    for i in range(4):
        scene.lines(verticalLines[i], color=(0.28, 0.68, 0.99), width=5.0)
        scene.lines(horizontalLines[i], color=(0.28, 0.68, 0.99), width=5.0)

    # Set the Scene to the new scene with the ball and line in it.
    canvas.scene(scene)

    # Show the window so that the scene is rendered.
    window.show()
