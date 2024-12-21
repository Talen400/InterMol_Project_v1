from vpython import *
import random as rr

# ------------------variables--------------------------
#configs
run = True
pause = False
# vectors
forces = []
# time
dt = 0.01
sim_time = 0
#others variables
k = 0.001
point = 1

size = 5
n = 200
particles = []
rv = 2

original_colors = [] 


# -----------------------------defs------------------------------
def stop_simulation():
    global run
    run = False

def paused() :
    global pause
    pause = not pause

def calculate_gravitational_force(p1, p2):
    r_vec = p2.pos - p1.pos
    distance = mag(r_vec)
    if distance <= 0:
        return vector(0, 0, 0) 
    force_non = k * ( (p1.mass*p2.mass)/ ((distance)**2) )
    return force_non * norm(r_vec)


def calculate_collision(p1, p2):
    r_vec = p1.pos - p2.pos
    distance = mag(r_vec)

    if distance <= (p1.radius + p2.radius):
        normal = norm(r_vec)
        relative_velocity = p1.velocity - p2.velocity
        speed = dot(relative_velocity, normal)

        if speed < 0:
            m1, m2 = p1.mass, p2.mass
            impulse = (2 * speed) / (m1 + m2)
            p1.velocity -= (impulse * m2) * normal
            p2.velocity += (impulse * m1) * normal

def update_gravitational_constant(evt):
    global k
    try:
        k = float(evt.number) 
    except ValueError:
        pass

def color_particles_by_charge():
    for particle in particles:
        if particle.mass > 0:
            particle.color = color.blue  # Positive mass: blue
        else:
            particle.color = color.red  # Negative mass: red

# --------------------------scene creation---------------------------------

scene.title = "Simulação da Bola com Dados"
button(text="Parar Simulação", bind=lambda _: stop_simulation())
button(text="Pausar Simulação", bind=lambda _: paused())
button(text="Colorir por carga", bind=lambda _: color_particles_by_charge())

input_field = winput(bind=update_gravitational_constant, prompt="k:", text=str(k), pos=vector(0, 8, 0))

box_object1 = box(
    pos=vector(0, 0, 0),  
    size=vector(size+3, size+3, size+3),  
    color=color.white,
    visible=False  
)

# ----------------------------graph------------------------------------

graph_position = graph(title='Part', xtitle='t', ytitle='x', xmin=-20, ymin=-20, xmax=1000, ymax=20)
position = gcurve(graph=graph_position)

graph_force = graph(title='Force', xtitle='t', ytitle='x')
force_graph = gcurve(graph=graph_force)

# --------------------------objects------------------------------------------


for i in range(n):
    particle = sphere(
        pos=vector(rr.uniform(-size, size), rr.uniform(-size, size), rr.uniform(-size, size)),
        radius=0.3,
        color=vector(rr.uniform(0, 1), rr.uniform(0, 1), rr.uniform(0, 1)),
    )
    particle.mass = rr.uniform(-1, 1)
    particle.velocity = vector (rr.uniform(-rv, rv), rr.uniform(-rv, rv), rr.uniform(-rv, rv))
    particles.append(particle)

# ----------------------- run sim -------------------------------------------

while run :
    rate(30)
    if not pause :
        sim_time += dt
        
        forces = [vector(0, 0, 0) for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    forces[i] += calculate_gravitational_force(particles[i], particles[j])

        for i in range(n):
            for j in range(i + 1, n):
                calculate_collision(particles[i], particles[j])


        for i in range(n):

            
            '''for j in range(n):
                calculate_colision(particles[i], particles[j])'''

            acceleration = forces[i] / particles[i].mass
            particles[i].velocity += acceleration * dt
            particles[i].pos += particles[i].velocity * dt

            # Verification colision box

            box_size = box_object1.size / 2  

            if abs(particles[i].pos.x) > box_size.x - particles[i].radius:
                particles[i].velocity.x *= -1 

            if abs(particles[i].pos.y) > box_size.y - particles[i].radius:
                particles[i].velocity.y *= -1  

            if abs(particles[i].pos.z) > box_size.z - particles[i].radius:
                particles[i].velocity.z *= -1  

            # Verification colision particules 


        particles[point].color = color.purple
        position.plot(sim_time, particles[point].pos.x)
        force_graph.plot(sim_time, mag(forces[point]))