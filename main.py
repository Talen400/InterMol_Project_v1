from vpython import *  
import random as rr  

# ------------------variables--------------------------  
# Settings  
run = False  # The simulation starts paused  
pause = False  
# Vectors  
forces = []  
# Time  
dt = 0.01  
sim_time = 0  
# Other variables  
k = 0.001  
point = 1  

size = 5  
n = 200  # Default number of particles  
particles = []  
rv = 2  

# -----------------------------defs------------------------------  
def start_simulation():  
    global run  
    run = True  

def stop_simulation():  
    global run  
    run = False  

def restart_simulation():  
    global particles, sim_time, forces, run, n  
    stop_simulation()  
    
    # Remove all particles from the environment  
    for particle in particles:  
        particle.visible = False  
    particles.clear()  # Clear the particle list  

    # Reset variables and graphs  
    sim_time = 0  
    position.delete()  # Clear the graphs  
    force_graph.delete()  

    # Update the number of particles  
    try:  
        n = int(input_particles.text)  # Get the value from the input field  
        if n <= 0:  # Avoid invalid values  
            n = 200  
    except ValueError:  
        n = 200  

    create_particles()  
    run = True  # Start immediately after restart  

def paused():  
    global pause  
    pause = not pause  

def calculate_gravitational_force(p1, p2):  
    r_vec = p2.pos - p1.pos  
    distance = mag(r_vec)  
    if distance <= 0:  
        return vector(0, 0, 0)  
    force_non = k * ((p1.mass * p2.mass) / (distance**2))  
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

def update_gravitational_constant():  
    global k  
    k = float(slider_k.value)  

def color_particles_by_charge():  
    for particle in particles:  
        if particle.mass > 0:  
            particle.color = color.blue  
        else:  
            particle.color = color.red  

def create_particles():  
    global particles  
    for i in range(n):  
        particle = sphere(  
            pos=vector(rr.uniform(-size, size), rr.uniform(-size, size), rr.uniform(-size, size)),  
            radius=0.3,  
            color=vector(rr.uniform(0, 1), rr.uniform(0, 1), rr.uniform(0, 1)),  
        )  
        particle.mass = rr.uniform(-1, 1)  
        particle.velocity = vector(rr.uniform(-rv, rv), rr.uniform(-rv, rv), rr.uniform(-rv, rv))  
        particles.append(particle)  

# --------------------------scene creation---------------------------------  
scene.title = "Interactive Simulation in VPython"  
button(text="Start Simulation", bind=lambda _: start_simulation())  
button(text="Stop Simulation", bind=lambda _: stop_simulation())  
button(text="Restart Simulation", bind=lambda _: restart_simulation())  
button(text="Pause Simulation", bind=lambda _: paused())  
button(text="Color by Charge", bind=lambda _: color_particles_by_charge())  

slider_k = slider(min=0.0001, max=0.01, value=k, length=220, bind=lambda _: update_gravitational_constant(), text="k (Gravitational Constant)")  
wtext(text="\n")  

input_particles = winput(bind=None, text=str(n), prompt="Number of Particles:")  
wtext(text="\n")  

box_object1 = box(  
    pos=vector(0, 0, 0),  
    size=vector(size+3, size+3, size+3),  
    color=color.white,  
    visible=False  
)  

# ----------------------------graph------------------------------------  
graph_position = graph(title='Particle Position', xtitle='t', ytitle='x', xmin=0, xmax=1000, ymin=-size, ymax=size)  
position = gcurve(graph=graph_position)  

graph_force = graph(title='Force on Particle', xtitle='t', ytitle='F', xmin=0, xmax=1000, ymin=0, ymax=1)  
force_graph = gcurve(graph=graph_force)  

# --------------------------objects------------------------------------------  
create_particles()  

# ----------------------- run sim -------------------------------------------  
while True:  
    rate(30)  
    if run and not pause:  
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
            acceleration = forces[i] / particles[i].mass  
            particles[i].velocity += acceleration * dt  
            particles[i].pos += particles[i].velocity * dt  

            # Check for collision with the box  
            box_size = box_object1.size / 2  

            if abs(particles[i].pos.x) > box_size.x - particles[i].radius:  
                particles[i].velocity.x *= -1  

            if abs(particles[i].pos.y) > box_size.y - particles[i].radius:  
                particles[i].velocity.y *= -1  

            if abs(particles[i].pos.z) > box_size.z - particles[i].radius:  
                particles[i].velocity.z *= -1  

        # Monitor the selected particle  
        particles[point].color = color.purple  
        position.plot(sim_time, particles[point].pos.x)  
        force_graph.plot(sim_time, mag(forces[point]))  