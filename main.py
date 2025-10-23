import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caixeiro Viajante - Algoritmo Genético")
clock = pygame.time.Clock()

# Parâmetros
TOTAL_CITIES = 10
POP_SIZE = 500
MUTATION_RATE = 0.01
CROSSOVER_RATE = 1.0

# Variáveis globais
cities = []
population = []
fitness = [0] * POP_SIZE
record_distance = float('inf')
best_ever = []
current_best = []
generation_count = 0
execution_number = 1

# Estatísticas para a tabela
stats = {
    'execution': execution_number,
    'crossover_rate': CROSSOVER_RATE,
    'mutation_rate': MUTATION_RATE,
    'population_size': POP_SIZE,
    'generations': 0,
    'best_fitness': 0,
    'best_distance': float('inf')
}

# Funções auxiliares
def swap(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp

def calc_distance(points, order):
    sum_dist = 0
    for i in range(len(order) - 1):
        city_a_index = order[i]
        city_a = points[city_a_index]
        city_b_index = order[i + 1]
        city_b = points[city_b_index]
        d = math.dist(city_a, city_b)
        sum_dist += d
    return sum_dist

# Algoritmo Genético
def calculate_fitness():
    global record_distance, best_ever, current_best, stats
    current_record = float('inf')
    
    for i in range(len(population)):
        d = calc_distance(cities, population[i])
        
        if d < record_distance:
            record_distance = d
            best_ever = population[i].copy()
            stats['best_distance'] = d
        
        if d < current_record:
            current_record = d
            current_best = population[i].copy()
        
        # Função de fitness (quanto menor a distância, maior o fitness)
        # Inverso simples para valores mais legíveis
        fitness[i] = 1 / (d + 1)
        
        # Atualiza o melhor fitness
        if fitness[i] > stats['best_fitness']:
            stats['best_fitness'] = fitness[i]

def normalize_fitness():
    sum_fitness = sum(fitness)
    for i in range(len(fitness)):
        fitness[i] = fitness[i] / sum_fitness
# Seleção por Roleta
def pick_one(population_list, prob):
    index = 0
    r = random.random()
    
    while r > 0:
        r = r - prob[index]
        index += 1
    
    index -= 1
    return population_list[index].copy()

# Crossover de Ordem (Order Crossover - 0X)
def cross_over(order_a, order_b):
    start = random.randint(0, len(order_a) - 1)
    end = random.randint(start + 1, len(order_a))
    new_order = order_a[start:end]
    
    for city in order_b:
        if city not in new_order:
            new_order.append(city)
    
    return new_order

# Mutação por troca (swap mutation)
def mutate(order, mutation_rate):
    for i in range(TOTAL_CITIES):
        if random.random() < mutation_rate:
            index_a = random.randint(0, len(order) - 1)
            index_b = (index_a + 1) % TOTAL_CITIES
            swap(order, index_a, index_b)

def next_generation():
    global population, generation_count
    new_population = []
    
    for i in range(len(population)):
        order_a = pick_one(population, fitness)
        order_b = pick_one(population, fitness)
        order = cross_over(order_a, order_b)
        mutate(order, MUTATION_RATE)
        new_population.append(order)
    
    population = new_population
    generation_count += 1
    stats['generations'] = generation_count

# Setup inicial
def setup():
    global cities, population
    
    order = list(range(TOTAL_CITIES))
    
    for i in range(TOTAL_CITIES):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 2)
        cities.append((x, y))
    
    for i in range(POP_SIZE):
        shuffled = order.copy()
        random.shuffle(shuffled)
        population.append(shuffled)

def print_stats():
    print(f"\n{'='*70}")
    print(f"RESULTADOS DA EXECUÇÃO")
    print(f"{'='*70}")
    print(f"N° Execução:           {stats['execution']}")
    print(f"Taxa de Cruzamento:    {stats['crossover_rate']:.2f}")
    print(f"Taxa de Mutação:       {stats['mutation_rate']:.4f}")
    print(f"Tamanho da População:  {stats['population_size']}")
    print(f"N° de Gerações:        {stats['generations']}")
    print(f"Melhor Fitness:        {stats['best_fitness']:.6f}")
    print(f"Melhor Distância:      {stats['best_distance']:.2f}")
    print(f"{'='*70}\n")
    
# Função de desenho
def draw():
    screen.fill((0, 0, 0))
    
    # Executa o algoritmo genético
    calculate_fitness()
    normalize_fitness()
    next_generation()
    
    # Desenha o melhor caminho de todos os tempos (metade superior)
    if best_ever:
        # Desenha as linhas
        for i in range(len(best_ever) - 1):
            n = best_ever[i]
            n_next = best_ever[i + 1]
            pygame.draw.line(screen, (255, 255, 255), cities[n], cities[n_next], 2)
        
        # Desenha os círculos nas cidades
        for i in range(len(best_ever)):
            n = best_ever[i]
            pygame.draw.circle(screen, (255, 255, 255), cities[n], 8, 2)
    
    # Desenha o melhor caminho da geração atual (metade inferior)
    if current_best:
        # Desenha as linhas
        for i in range(len(current_best) - 1):
            n = current_best[i]
            n_next = current_best[i + 1]
            city_a = (cities[n][0], cities[n][1] + HEIGHT // 2)
            city_b = (cities[n_next][0], cities[n_next][1] + HEIGHT // 2)
            pygame.draw.line(screen, (255, 255, 255), city_a, city_b, 2)
        
        # Desenha os círculos nas cidades
        for i in range(len(current_best)):
            n = current_best[i]
            city = (cities[n][0], cities[n][1] + HEIGHT // 2)
            pygame.draw.circle(screen, (255, 255, 255), city, 8, 2)
    
    # Exibe informações
    font = pygame.font.Font(None, 28)
    
    text1 = font.render(f"Geracao: {generation_count}", True, (255, 255, 255))
    text2 = font.render(f"Melhor Distancia: {record_distance:.2f}", True, (255, 255, 255))
    
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    
    pygame.display.flip()

# Loop principal
def main():
    setup()
    running = True
    
    print("\n" + "="*60)
    print("ALGORITMO GENÉTICO - PROBLEMA DO CAIXEIRO VIAJANTE")
    print("="*60)
    print(f"Configurações:")
    print(f"  - Número de Cidades: {TOTAL_CITIES}")
    print(f"  - Tamanho da População: {POP_SIZE}")
    print(f"  - Taxa de Mutação: {MUTATION_RATE}")
    print(f"  - Taxa de Cruzamento: {CROSSOVER_RATE}")
    print(f"\nPressione ESC para finalizar e salvar resultados")
    print("="*60 + "\n")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print_stats()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print_stats()
                    running = False
        
        draw()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()
