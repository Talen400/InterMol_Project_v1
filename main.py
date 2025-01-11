from vpython import *
import numpy as np

# configs
run = True
pause = False
# time
dt = 0.01
sim_time = 0
# size of box and spawn balls
bounds = 7

#variables and vectors
n_particles = 1000
positions = np.random.uniform(-5, 5, (n_particles, 3)).astype(np.float32)
velocities = np.random.uniform(-1, 1, (n_particles, 3)).astype(np.float32)
charges = np.random.choice([-1, 1], size=n_particles).astype(np.int16)
k = 0.01
forces = np.zeros((n_particles, 3), dtype=np.float32)
# -----------------------------defs------------------------------

def stop_simulation():
    global run
    run = False

def paused() :
    global pause
    pause = not pause

# --------------------------scene creation---------------------------------

scene.title = "Simulação da Bola com Dados"
button(text="Parar Simulação", bind=lambda _: stop_simulation())
button(text="Pausar Simulação", bind=lambda _: paused())

box_object1 = box(
    pos=vector(0, 0, 0),  
    size=vector(bounds+3, bounds+3, bounds+3),  
    color=color.white,
    visible=False  
)

# ---------------------- objetcs ---------------------------------------
particles = [sphere(pos=vector(*positions[i]), radius=0.2, color=vector(1, 0, 0)) for i in range(n_particles)]
# ---------- run ------------------
while run :
    rate(60)
    if not pause :
        sim_time += dt

        positions += velocities * dt
        
        mask = np.abs(positions) > bounds
        velocities[mask] *= -1
    
        for i in range(n_particles):
            particles[i].pos = vector(*positions[i])