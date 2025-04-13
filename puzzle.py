import pygame
import time
from collections import deque
import heapq

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# Configuração da tela do Pygame
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador do 8-Puzzle - DFS")

# Estado inicial e objetivo
estado_inicial = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
estado_objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Movimentos possíveis
movimentos = {
    "↑": (-1, 0),
    "↓": (1, 0),
    "←": (0, -1),
    "→": (0, 1)
}

# Função para encontrar a posição do zero (espaço vazio)
def encontrar_zero(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j

# Função para mover o zero
def mover(estado, direcao):
    i, j = encontrar_zero(estado)
    di, dj = movimentos[direcao]
    novo_i, novo_j = i + di, j + dj

    if 0 <= novo_i < 3 and 0 <= novo_j < 3:
        novo_estado = [linha[:] for linha in estado]  # Copia o tabuleiro
        novo_estado[i][j], novo_estado[novo_i][novo_j] = novo_estado[novo_i][novo_j], novo_estado[i][j]
        return novo_estado

    return None  # Movimento inválido

# Conversor de estado para tupla (para usar em conjuntos e dicionários)
def estado_para_tupla(estado):
    return tuple(tuple(linha) for linha in estado)

# Implementação da Busca em Largura (BFS)
def bfs(inicio, objetivo):
    fila = deque([(inicio, [])])
    visitados = set()

    while fila:
        estado_atual, caminho = fila.popleft()
        estado_tupla = estado_para_tupla(estado_atual)

        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)

        if estado_atual == objetivo:
            return caminho + [estado_atual]

        for direcao in movimentos:
            novo_estado = mover(estado_atual, direcao)
            if novo_estado:
                fila.append((novo_estado, caminho + [estado_atual]))

    return None

# Implementação da Busca em Profundidade (DFS)
def dfs(inicio, objetivo):
    pilha = [(inicio, [])]
    visitados = set()

    while pilha:
        estado_atual, caminho = pilha.pop()
        estado_tupla = estado_para_tupla(estado_atual)

        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)

        if estado_atual == objetivo:
            return caminho + [estado_atual]

        for direcao in movimentos:
            novo_estado = mover(estado_atual, direcao)
            if novo_estado:
                pilha.append((novo_estado, caminho + [estado_atual]))

    return None

# Heurística: número de peças fora do lugar
def heuristica_pecas(estado, objetivo):
    return sum(1 for i in range(3) for j in range(3) if estado[i][j] != 0 and estado[i][j] != objetivo[i][j])

# Heurística: distância de Manhattan (quantos movimentos faltam para cada peça)
def heuristica_movimentos(estado, objetivo):
    dist = 0
    for num in range(1, 9):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == num:
                    for x in range(3):
                        for y in range(3):
                            if objetivo[x][y] == num:
                                dist += abs(i - x) + abs(j - y)
    return dist

# Algoritmo A* (usando heurística)
def a_estrela(inicio, objetivo, heuristica):
    heap = [(heuristica(inicio, objetivo), 0, inicio, [])]
    visitados = set()

    while heap:
        _, custo, estado_atual, caminho = heapq.heappop(heap)
        estado_tupla = estado_para_tupla(estado_atual)

        if estado_tupla in visitados:
            continue
        visitados.add(estado_tupla)

        if estado_atual == objetivo:
            return caminho + [estado_atual]

        for direcao in movimentos:
            novo_estado = mover(estado_atual, direcao)
            if novo_estado:
                novo_caminho = caminho + [estado_atual]
                novo_custo = custo + 1
                heur = heuristica(novo_estado, objetivo)
                heapq.heappush(heap, (novo_custo + heur, novo_custo, novo_estado, novo_caminho))

    return None

# Função para desenhar o tabuleiro do 8-Puzzle no Pygame
def desenhar_tabuleiro(estado):
    screen.fill(WHITE)
    tam_celula = WIDTH // 3

    for i in range(3):
        for j in range(3):
            num = estado[i][j]
            rect = pygame.Rect(j * tam_celula, i * tam_celula, tam_celula, tam_celula)
            pygame.draw.rect(screen, BLUE if num == 0 else GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)

            if num != 0:
                font = pygame.font.Font(None, 60)
                text = font.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    pygame.display.flip()

# Loop de animação da solução
def executar_simulacao(caminho):
    pygame.init()
    clock = pygame.time.Clock()

    for estado in caminho:
        desenhar_tabuleiro(estado)
        time.sleep(1)
        clock.tick(1)

    time.sleep(2)
    pygame.quit()

# Escolha do algoritmo de busca
# caminho_solucao = dfs(estado_inicial, estado_objetivo)
caminho_solucao = bfs(estado_inicial, estado_objetivo)
# caminho_solucao = a_estrela(estado_inicial, estado_objetivo, heuristica_movimentos)

# Verifica e executa a simulação se houver solução
if caminho_solucao:
    executar_simulacao(caminho_solucao)
    print("Passos para a solução:", len(caminho_solucao) - 1)
else:
    print("Nenhuma solução encontrada.")
