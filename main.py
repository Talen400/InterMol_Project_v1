from vpython import *
import random as rr

# ------------------variables--------------------------
# Configurações
run = False  # A simulação começa parada
pause = False
# Vetores
forces = []
# Tempo
dt = 0.01
sim_time = 0
# Outras variáveis
k = 0.001
point = 1

size = 5
n = 200  # Número padrão de partículas
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
    
    # Remove todas as partículas do ambiente
    for particle in particles:
        particle.visible = False
    particles.clear()  # Limpa a lista de partículas

    # Reinicia as variáveis e gráficos
    sim_time = 0
    position.delete()  # Limpa os gráficos
    force_graph.delete()

    # Atualiza o número de partículas
    try:
        n = int(input_particles.text)  # Obtém o valor do campo de entrada
        if n <= 0:  # Evita valores inválidos
            n = 200
    except ValueError:
        n = 200

    create_particles()
    run = True  # Inicia imediatamente após reiniciar

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
scene.title = "Simulação Interativa no VPython"
button(text="Iniciar Simulação", bind=lambda _: start_simulation())
button(text="Parar Simulação", bind=lambda _: stop_simulation())
button(text="Reiniciar Simulação", bind=lambda _: restart_simulation())
button(text="Pausar Simulação", bind=lambda _: paused())
button(text="Colorir por carga", bind=lambda _: color_particles_by_charge())

slider_k = slider(min=0.0001, max=0.01, value=k, length=220, bind=lambda _: update_gravitational_constant(), text="k (Gravitacional)")
wtext(text="\n")

input_particles = winput(bind=None, text=str(n), prompt="Número de Partículas:")
wtext(text="\n")

box_object1 = box(
    pos=vector(0, 0, 0),
    size=vector(size+3, size+3, size+3),
    color=color.white,
    visible=False
)

# ----------------------------graph------------------------------------
graph_position = graph(title='Posição da Partícula', xtitle='t', ytitle='x', xmin=0, xmax=1000, ymin=-size, ymax=size)
position = gcurve(graph=graph_position)

graph_force = graph(title='Força na Partícula', xtitle='t', ytitle='F', xmin=0, xmax=1000, ymin=0, ymax=1)
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

            # Verificação de colisão com a caixa
            box_size = box_object1.size / 2  

            if abs(particles[i].pos.x) > box_size.x - particles[i].radius:
                particles[i].velocity.x *= -1 

            if abs(particles[i].pos.y) > box_size.y - particles[i].radius:
                particles[i].velocity.y *= -1  

            if abs(particles[i].pos.z) > box_size.z - particles[i].radius:
                particles[i].velocity.z *= -1  

        # Monitorar a partícula selecionada
        particles[point].color = color.purple
        position.plot(sim_time, particles[point].pos.x)
        force_graph.plot(sim_time, mag(forces[point]))
