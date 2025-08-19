
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg") 
from matplotlib.animation import FuncAnimation
import random
import string

# Parameters
NUM_CITIES = 40
POP_SIZE = 100
GENERATIONS = 500
# MUTATION_RATE = min(0.05, 1.0 / NUM_CITIES)
MUTATION_RATE=0.05
ELITE_SIZE = 1

np.random.seed(42)
# random.seed(42)

cities = np.random.rand(NUM_CITIES, 2) * 150

def generate_city_names(n):
    names = []
    for i in range(n):
        name = ''
        num = i
        while True:
            name = chr(65 + num % 26) + name
            num = num // 26 - 1
            if num < 0:
                break
        names.append(name)
    return names

city_names = generate_city_names(NUM_CITIES)

def dist(a, b):
    return np.linalg.norm(cities[a] - cities[b])

def path_length(path):
    return sum(dist(path[i], path[(i + 1) % NUM_CITIES]) for i in range(NUM_CITIES))

START_CITY = 0

def init_population():
    population = []
    rest = list(range(NUM_CITIES))
    rest.remove(START_CITY)
    for _ in range(POP_SIZE):
        route_rest = random.sample(rest, len(rest))
        route = [START_CITY] + route_rest
        population.append(route)
    print(f"\n=== Initial Population with fixed start city {city_names[START_CITY]} ===")
    for i, path in enumerate(population):
        named = [city_names[c] for c in path]
        print(f"\n{i+1}: {named} -> Distance: {path_length(path):.2f}")
    return population

def crossover(p1, p2):
    a, b = sorted(random.sample(range(1, NUM_CITIES), 2))
    child = [-1]*NUM_CITIES
    child[0] = START_CITY
    child[a:b] = p1[a:b]
    pos = b
    for city in p2:
        if city not in child:
            while child[pos % NUM_CITIES] != -1:
                pos += 1
            child[pos % NUM_CITIES] = city
    # print(f" \n   Crossover: { [city_names[i] for i in p1] } × { [city_names[i] for i in p2] }")
    # print(f" \n   Child: { [city_names[i] for i in child] }")
    return child

def mutate(path):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(1, NUM_CITIES), 2)
        path[i], path[j] = path[j], path[i]
        # print(f"  \n    Mutation: swapped {city_names[i]} and {city_names[j]}")
    return path

def next_gen(pop):
    print("\n--- Creating Next Generation ---")
    ranked = sorted(pop, key=path_length)
    # print(f" \n Top {ELITE_SIZE} kept as elite.")
    new_pop = ranked[:ELITE_SIZE]
    while len(new_pop) < POP_SIZE:
        p1, p2 = random.sample(ranked[:20], 2)
        # print(f" \n Selected:")
        # print(f"   P1: { [city_names[i] for i in p1] } → {path_length(p1):.2f}")
        # print(f"   P2: { [city_names[i] for i in p2] } → {path_length(p2):.2f}")
        child = crossover(p1, p2)
        child = mutate(child)
        # print(f"   Child distance: {path_length(child):.2f}")
        new_pop.append(child)
    return new_pop

# Visualization setup
fig, ax = plt.subplots()
ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_title("TSP Route Animation with City Labels")

# sc = ax.scatter(cities[:, 0], cities[:, 1], color='red')
# Color all cities blue except the start city
colors = ['blue'] * NUM_CITIES
colors[START_CITY] = 'red'  # start city is red
sc = ax.scatter(cities[:, 0], cities[:, 1], color=colors)
lines, = ax.plot([], [], 'b-o')
text_annotations = []
arrow_artists = []  # NEW

# Label cities
for i, (x, y) in enumerate(cities):
    ax.text(x + 1.5, y + 1.5, city_names[i], fontsize=8, color='black')

def label_edges(path):
    global text_annotations
    for txt in text_annotations:
        txt.remove()
    text_annotations = []
    for i in range(NUM_CITIES):
        a = path[i]
        b = path[(i + 1) % NUM_CITIES]
        mid = (cities[a] + cities[b]) / 2
        d = dist(a, b)
        txt = ax.text(mid[0], mid[1], f"{d:.1f}", fontsize=8, color='green')
        text_annotations.append(txt)

# NEW: draw arrows along the path
def draw_arrows(path):
    global arrow_artists
    for arrow in arrow_artists:
        arrow.remove()
    arrow_artists = []
    for i in range(NUM_CITIES):
        a = path[i]
        b = path[(i + 1) % NUM_CITIES]
        start = cities[a]
        end = cities[b]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        arrow = ax.arrow(start[0], start[1], dx, dy,
                         head_width=1.8, head_length=3,
                         length_includes_head=True,
                         fc='blue', ec='blue', alpha=0.5)
        arrow_artists.append(arrow)

# Init
population = init_population()
generation_counter = [0]
best_path = []

def update(frame):
    global population, best_path
    generation_counter[0] += 1
    print(f"\n============================")
    print(f"GENERATION {generation_counter[0]}")
    print(f"============================")

    population = next_gen(population)
    best_path = sorted(population, key=path_length)[0]
    best_distance = path_length(best_path)

    named_best = [city_names[i] for i in best_path]
    print(f"\n>>> Best Route: {named_best}")
    print(f">>> Distance: {best_distance:.2f}")

    coords = cities[best_path + [best_path[0]]]
    lines.set_data(coords[:, 0], coords[:, 1])
    label_edges(best_path)
    draw_arrows(best_path)
    ax.set_title(f"Generation {generation_counter[0]} | Distance: {best_distance:.2f}")
    return lines, *text_annotations, *arrow_artists

ani = FuncAnimation(fig, update, frames=GENERATIONS, interval=10, repeat=False)
plt.tight_layout()
plt.show()
