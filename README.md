# Genetic Algorithm for Solving the Traveling Salesman Problem (TSP)

This project demonstrates how to solve the Traveling Salesman Problem (TSP) using a **Genetic Algorithm (GA)** in Python. It includes an animated visualization of the evolution of the path and direction arrows to show the order of cities visited.

## 📌 Problem

Given a set of cities, the goal is to find the shortest possible route that visits each city exactly once and returns to the starting city.

##  Features

- Animated plotting of the GA process using `matplotlib.animation`
- Customizable number of cities
- Direction arrows to visualize the visiting order of cities
- GA features like:
  - Population-based evolution
  - Selection, crossover, mutation
  - Elitism to preserve the best routes
  - Early stopping when an optimal path is found

##  Parameters

You can customize the following parameters:

```python
NUM_CITIES = 8            # Number of cities in the problem
POP_SIZE = 50             # Population size
GENERATIONS = 500         # Number of generations to evolve
MUTATION_RATE = 0.05      # Mutation rate (0 to 1)
ELITE_SIZE = 5            # Number of elite individuals to carry over
