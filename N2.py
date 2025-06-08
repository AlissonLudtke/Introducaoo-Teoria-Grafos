from typing import List, Tuple, Dict, Optional
import math

class Graph:
    def __init__(self, is_directed: bool = False, is_weighted: bool = True):
        self.vertices = []
        self.adjacency_matrix = []
        self.is_directed = is_directed
        self.is_weighted = is_weighted
    
    # ========================================
    # MÉTODOS BÁSICOS DO GRAFO
    # ========================================
    
    def add_vertex(self, vertex_data: dict) -> int:
        """Adiciona um vértice ao grafo"""
        # Verificar se já existe um vértice com o mesmo nome
        nome_novo = vertex_data.get('nome', '').strip()
        for vertex in self.vertices:
            if vertex.get('nome', '').strip().lower() == nome_novo.lower():
                print(f"Erro: Já existe um objeto celeste com o nome '{nome_novo}'.")
                return -1  # Retorna -1 para indicar erro
        
        self.vertices.append(vertex_data)
        
        # Expandir a matriz de adjacência
        n = len(self.vertices)
        
        # Adicionar nova linha
        self.adjacency_matrix.append([0.0] * n)
        
        # Adicionar nova coluna a todas as linhas existentes
        for i in range(n - 1):
            self.adjacency_matrix[i].append(0.0)
        
        return n - 1  # Retorna o índice do vértice adicionado
    
    def add_edge(self, v1: int, v2: int, weight: float = 1.0) -> None:
        """Adiciona uma aresta entre v1 e v2"""
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            return  # Silencioso para não quebrar o carregamento
        
        val = weight if self.is_weighted else 1.0
        self.adjacency_matrix[v1][v2] = val
        
        if not self.is_directed:
            self.adjacency_matrix[v2][v1] = val
    
    def remove_vertex(self, vertex_index: int) -> bool:
        """Remove um vértice do grafo"""
        if not (0 <= vertex_index < len(self.vertices)):
            print("Índice inválido.")
            return False
        
        # Remove o vértice da lista
        removed_vertex = self.vertices.pop(vertex_index)
        
        # Remove a linha correspondente da matriz
        self.adjacency_matrix.pop(vertex_index)
        
        # Remove a coluna correspondente de todas as linhas
        for row in self.adjacency_matrix:
            row.pop(vertex_index)
        
        print(f"Vértice '{removed_vertex['nome']}' removido com sucesso.")
        return True
    
    def remove_edge(self, v1: int, v2: int) -> bool:
        """Remove uma aresta entre v1 e v2"""
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            print("Índices inválidos.")
            return False
        
        self.adjacency_matrix[v1][v2] = 0.0
        if not self.is_directed:
            self.adjacency_matrix[v2][v1] = 0.0
        
        v1_nome = self.vertices[v1]['nome']
        v2_nome = self.vertices[v2]['nome']
        print(f"Aresta entre '{v1_nome}' e '{v2_nome}' removida.")
        return True
    
    def update_vertex(self, vertex_index: int, new_data: dict) -> bool:
        """Atualiza as informações de um vértice"""
        if not (0 <= vertex_index < len(self.vertices)):
            print("Índice inválido.")
            return False
        
        old_name = self.vertices[vertex_index]['nome']
        self.vertices[vertex_index].update(new_data)
        new_name = self.vertices[vertex_index]['nome']
        
        print(f"Vértice atualizado: '{old_name}' -> '{new_name}'")
        return True
    
    def update_edge(self, v1: int, v2: int, new_weight: float) -> bool:
        """Atualiza o peso de uma aresta"""
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            print("Índices inválidos.")
            return False
        
        if self.adjacency_matrix[v1][v2] == 0:
            print("Aresta não existe.")
            return False
        
        self.adjacency_matrix[v1][v2] = new_weight
        if not self.is_directed:
            self.adjacency_matrix[v2][v1] = new_weight
        
        v1_nome = self.vertices[v1]['nome']
        v2_nome = self.vertices[v2]['nome']
        print(f"Peso da aresta '{v1_nome}' -> '{v2_nome}' atualizado para {new_weight}")
        return True
    
    # ========================================
    # MÉTODOS DE CONSULTA E INFORMAÇÃO
    # ========================================
    
    def get_vertex_info(self, vertex_index: int) -> Optional[dict]:
        """Consulta informações de um vértice"""
        if not (0 <= vertex_index < len(self.vertices)):
            print("Índice inválido.")
            return None
        
        vertex = self.vertices[vertex_index]
        print(f"\nInformações do vértice {vertex_index + 1}:")
        for key, value in vertex.items():
            print(f"  {key}: {value}")
        
        # Mostrar conexões
        print(f"  Conexões:")
        for i, weight in enumerate(self.adjacency_matrix[vertex_index]):
            if weight > 0:
                target_name = self.vertices[i]['nome']
                print(f"    -> {target_name} (peso: {weight})")
        
        return vertex
    
    def get_edge_info(self, v1: int, v2: int) -> Optional[float]:
        """Consulta informações de uma aresta"""
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            print("Índices inválidos.")
            return None
        
        weight = self.adjacency_matrix[v1][v2]
        if weight == 0:
            print("Aresta não existe.")
            return None
        
        v1_nome = self.vertices[v1]['nome']
        v2_nome = self.vertices[v2]['nome']
        print(f"Aresta '{v1_nome}' -> '{v2_nome}': peso {weight}")
        return weight
    
    def list_graph_info(self):
        """Lista informações gerais do grafo"""
        print(f"\n{'='*50}")
        print(f"INFORMAÇÕES DO GRAFO")
        print(f"{'='*50}")
        print(f"Número de vértices: {len(self.vertices)}")
        
        # Contar arestas
        edge_count = 0
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if self.adjacency_matrix[i][j] > 0:
                    edge_count += 1
        
        if not self.is_directed:
            edge_count //= 2  # Cada aresta é contada duas vezes em grafos não-direcionados
        
        print(f"Número de arestas: {edge_count}")
        print(f"Tipo: {'Direcionado' if self.is_directed else 'Não-direcionado'}")
        print(f"Ponderado: {'Sim' if self.is_weighted else 'Não'}")
        
        if self.vertices:
            print(f"\nVértices:")
            for i, vertex in enumerate(self.vertices):
                print(f"  [{i+1:2d}] {vertex['nome']}")
    
    def find_brightest_star(self):
        """Encontra a estrela mais brilhante (menor magnitude)"""
        if not self.vertices:
            print("Grafo vazio.")
            return
        
        brightest = None
        min_magnitude = float('inf')
        
        for i, vertex in enumerate(self.vertices):
            magnitude = vertex.get('magnitude')
            if magnitude is not None and magnitude < min_magnitude:
                min_magnitude = magnitude
                brightest = (i, vertex)
        
        if brightest:
            print(f"\nEstrela mais brilhante:")
            print(f"  [{brightest[0]+1}] {brightest[1]['nome']}")
            print(f"  Magnitude: {min_magnitude}")
        else:
            print("Nenhuma estrela com magnitude definida encontrada.")
    
    def count_by_constellation(self):
        """Conta objetos por constelação"""
        if not self.vertices:
            print("Grafo vazio.")
            return
        
        constellation_count = {}
        for vertex in self.vertices:
            constellation = vertex.get('constelacao', 'Não definido')
            constellation_count[constellation] = constellation_count.get(constellation, 0) + 1
        
        print(f"\nContagem por constelação:")
        for constellation, count in sorted(constellation_count.items()):
            print(f"  {constellation}: {count} objeto(s)")
    
    def listar_todas_estrelas(self):
        """
        Lista todas as estrelas/planetas do grafo com informações detalhadas
        """
        if not self.vertices:
            print("Nenhum vértice encontrado no grafo.")
            return
        
        print(f"\n============================================================")
        print(f"                    REDE ESTELAR DISPONIVEL")
        print(f"============================================================")
        
        # Listar de forma simples e compatível
        for i, vertice in enumerate(self.vertices):
            nome = vertice.get('nome', 'Sem nome')
            magnitude = vertice.get('magnitude', 'N/A')
            constelacao = vertice.get('constelacao', 'N/A')
            print(f"[{i+1:2d}] {nome}")
            print(f"     Magnitude: {magnitude} | Constelacao: {constelacao}")
        
        print(f"============================================================")
        print(f"Total: {len(self.vertices)} objetos celestes disponíveis")
        print(f"============================================================\n")
    
    def list_most_connected_stars(self):
        """Lista as estrelas mais conectadas"""
        if not self.vertices:
            print("Grafo vazio.")
            return
        
        connections = []
        for i in range(len(self.vertices)):
            count = sum(1 for weight in self.adjacency_matrix[i] if weight > 0)
            connections.append((count, i, self.vertices[i]['nome']))
        
        connections.sort(reverse=True)
        
        print(f"\nEstrelas mais conectadas:")
        for count, index, name in connections[:5]:
            print(f"  [{index+1:2d}] {name}: {count} conexões")

    def exibir_matriz_adjacencia(self):
        """
        Exibe a matriz de adjacência verdadeira (apenas 0s e 1s)
        """
        if not self.vertices:
            print("Grafo vazio.")
            return
        
        n = len(self.vertices)
        
        print(f"\nMATRIZ DE ADJACENCIA (apenas conectividade)")
        print("=" * 80)
        
        # Cabeçalho
        header = "      "
        for vertice in self.vertices:
            nome = vertice['nome']
            if "Constelacao" in nome or "Constelação" in nome:
                abbrev = nome.split()[-1][:3]
            elif "estrela" in nome:
                abbrev = nome.split()[0][:3]
            else:
                abbrev = nome[:3]
            header += f"{abbrev:>4}"
        
        print(header)
        
        # Matriz só com 0 e 1
        for i in range(n):
            nome = self.vertices[i]['nome']
            if "Constelacao" in nome or "Constelação" in nome:
                linha_label = nome.split()[-1][:3]
            elif "estrela" in nome:
                linha_label = nome.split()[0][:3]
            else:
                linha_label = nome[:3]
            
            linha = f"{linha_label:>6}"
            
            for j in range(n):
                # APENAS 0 ou 1 - SEM DECIMAIS
                if self.adjacency_matrix[i][j] > 0:
                    linha += "   1"
                else:
                    linha += "   0"
            
            print(linha)
        
        print("=" * 80)
        print("1 = CONECTADO | 0 = NAO CONECTADO")

    def carregar_rede_estelar_predefinida(self):
        """
        Carrega uma rede estelar predefinida com dados astronômicos reais
        """
        # Limpar grafo existente
        self.vertices = []
        self.adjacency_matrix = []
        
        # Definir vértices com informações astronômicas detalhadas
        vertices_data = [
            {"nome": "Constelação de Órion", "magnitude": None, "constelacao": "Área do céu"},
            {"nome": "Betelgeuse (estrela em Órion)", "magnitude": 0.42, "constelacao": "Órion"},
            {"nome": "Rigel (estrela em Órion)", "magnitude": 0.18, "constelacao": "Órion"},
            {"nome": "Constelação do Escorpião", "magnitude": None, "constelacao": "Área do céu"},
            {"nome": "Antares (estrela em Escorpião)", "magnitude": 1.06, "constelacao": "Escorpião"},
            {"nome": "Shaula (estrela em Escorpião)", "magnitude": 1.62, "constelacao": "Escorpião"},
            {"nome": "Constelação da Ursa Maior", "magnitude": None, "constelacao": "Área do céu"},
            {"nome": "Dubhe (estrela na Ursa Maior)", "magnitude": 1.81, "constelacao": "Ursa Maior"},
            {"nome": "Merak (estrela na Ursa Maior)", "magnitude": 2.34, "constelacao": "Ursa Maior"},
            {"nome": "Constelação de Pégaso", "magnitude": None, "constelacao": "Área do céu"},
            {"nome": "Markab (estrela em Pégaso)", "magnitude": 2.49, "constelacao": "Pégaso"},
            {"nome": "Scheat (estrela em Pégaso)", "magnitude": 2.44, "constelacao": "Pégaso"},
            {"nome": "Sol", "magnitude": -26.74, "constelacao": "Sistema Solar"},
            {"nome": "Mercúrio", "magnitude": -1.9, "constelacao": "Sistema Solar"},
            {"nome": "Vênus", "magnitude": -4.6, "constelacao": "Sistema Solar"},
            {"nome": "Terra", "magnitude": None, "constelacao": "Sistema Solar"},
            {"nome": "Marte", "magnitude": -2.94, "constelacao": "Sistema Solar"},
            {"nome": "Júpiter", "magnitude": -2.7, "constelacao": "Sistema Solar"},
            {"nome": "Saturno", "magnitude": 0.46, "constelacao": "Sistema Solar"},
            {"nome": "Urano", "magnitude": 5.68, "constelacao": "Sistema Solar"},
            {"nome": "Netuno", "magnitude": 7.8, "constelacao": "Sistema Solar"},
            {"nome": "Plutão", "magnitude": 14.0, "constelacao": "Sistema Solar"}
        ]
        
        # Adicionar todos os vértices
        for vertex_data in vertices_data:
            self.add_vertex(vertex_data)
        
        # Define as arestas (usando pesos variados para demonstrar algoritmos)
        edges = [
            # Constelações -> Estrelas (peso 1.0)
            (0, 1, 1.0), (0, 2, 1.0),  # Órion -> Betelgeuse, Rigel
            (3, 4, 1.0), (3, 5, 1.0),  # Escorpião -> Antares, Shaula
            (6, 7, 1.0), (6, 8, 1.0),  # Ursa Maior -> Dubhe, Merak
            (9, 10, 1.0), (9, 11, 1.0), # Pégaso -> Markab, Scheat
            
            # Sol <-> Planetas (pesos representando distâncias aproximadas em UA)
            (12, 13, 0.39), (13, 12, 0.39),  # Sol <-> Mercúrio
            (12, 14, 0.72), (14, 12, 0.72),  # Sol <-> Vênus
            (12, 15, 1.0), (15, 12, 1.0),    # Sol <-> Terra
            (12, 16, 1.52), (16, 12, 1.52),  # Sol <-> Marte
            (12, 17, 5.2), (17, 12, 5.2),    # Sol <-> Júpiter
            (12, 18, 9.5), (18, 12, 9.5),    # Sol <-> Saturno
            (12, 19, 19.2), (19, 12, 19.2),  # Sol <-> Urano
            (12, 20, 30.0), (20, 12, 30.0),  # Sol <-> Netuno
            (12, 21, 39.5), (21, 12, 39.5),  # Sol <-> Plutão
            
            # Vizinhança orbital (pesos representando diferença de distância)
            (13, 14, 0.33), # Mercúrio -> Vênus
            (14, 15, 0.28), # Vênus -> Terra
            (15, 16, 0.52), # Terra -> Marte
            (16, 17, 3.68), # Marte -> Júpiter
            (17, 18, 4.3),  # Júpiter -> Saturno
            (18, 19, 9.7),  # Saturno -> Urano
            (19, 20, 10.8), # Urano -> Netuno
            (20, 21, 9.5),  # Netuno -> Plutão
        ]
        
        # Adicionar todas as arestas (serão automaticamente bidirecionais)
        for origem, destino, peso in edges:
            if origem < len(self.vertices) and destino < len(self.vertices):
                self.add_edge(origem, destino, peso)
    
    # ========================================
    # IMPLEMENTAÇÃO PRÓPRIA DE FILA DE PRIORIDADE (SEM BIBLIOTECAS)
    # ========================================
    class MinHeap:
        """Implementação própria de min-heap para substituir heapq"""
        def __init__(self):
            self.heap = []
        
        def push(self, item):
            """Insere item (custo, vertice) no heap"""
            self.heap.append(item)
            self._heapify_up(len(self.heap) - 1)
        
        def pop(self):
            """Remove e retorna o item com menor custo"""
            if not self.heap:
                return None
            
            if len(self.heap) == 1:
                return self.heap.pop()
            
            root = self.heap[0]
            self.heap[0] = self.heap.pop()
            self._heapify_down(0)
            return root
        
        def is_empty(self):
            return len(self.heap) == 0
        
        def _heapify_up(self, index):
            if index == 0:
                return
            
            parent_index = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent_index][0]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                self._heapify_up(parent_index)
        
        def _heapify_down(self, index):
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index
            
            if (left_child < len(self.heap) and 
                self.heap[left_child][0] < self.heap[smallest][0]):
                smallest = left_child
            
            if (right_child < len(self.heap) and 
                self.heap[right_child][0] < self.heap[smallest][0]):
                smallest = right_child
            
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                self._heapify_down(smallest)
    
    # ========================================
    # ALGORITMOS DE BUSCA CORRIGIDOS (SEGUINDO TODAS AS REGRAS)
    # ========================================
    
    def dfs_all_paths(self, start: int, target: int) -> Tuple[List[List[int]], List[float]]:
        """
        DFS que encontra TODOS os caminhos possíveis
        Retorna: (lista_de_caminhos, lista_de_custos)
        """
        if not self._validate_input(start, target):
            return [], []
        
        if start == target:
            return [[start]], [0.0]
        
        all_paths = []
        all_costs = []
        
        def dfs_recursive(current: int, path: List[int], cost: float, visited: set):
            if current == target:
                all_paths.append(path.copy())
                all_costs.append(cost)
                return
            
            for neighbor in range(len(self.vertices)):
                weight = self.adjacency_matrix[current][neighbor]
                if weight > 0 and neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs_recursive(neighbor, path, cost + weight, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        visited = {start}
        dfs_recursive(start, [start], 0.0, visited)
        
        if not all_paths:
            print(f"DFS: Não existe caminho entre {self.vertices[start]['nome']} e {self.vertices[target]['nome']}")
            return [], []
        
        # Encontrar caminho ótimo (menor custo)
        min_cost = min(all_costs)
        optimal_indices = [i for i, cost in enumerate(all_costs) if cost == min_cost]
        
        self._print_all_paths_results("DFS", all_paths, all_costs, optimal_indices, start, target)
        return all_paths, all_costs
    
    def bfs_all_paths(self, start: int, target: int) -> Tuple[List[List[int]], List[float]]:
        """
        BFS que encontra TODOS os caminhos com menor número de arestas
        """
        if not self._validate_input(start, target):
            return [], []
        
        if start == target:
            return [[start]], [0.0]
        
        # BFS nivel por nivel para encontrar distância mínima
        queue = [(start, [start], 0.0)]
        visited_levels = {}
        visited_levels[start] = 0
        min_path_length = float('inf')
        
        all_paths = []
        all_costs = []
        
        while queue:
            current, path, cost = queue.pop(0)
            
            # Se já encontramos caminhos e este é mais longo, parar
            if len(path) > min_path_length:
                continue
            
            if current == target:
                if len(path) < min_path_length:
                    min_path_length = len(path)
                    all_paths = [path.copy()]
                    all_costs = [cost]
                elif len(path) == min_path_length:
                    all_paths.append(path.copy())
                    all_costs.append(cost)
                continue
            
            for neighbor in range(len(self.vertices)):
                weight = self.adjacency_matrix[current][neighbor]
                if weight > 0:
                    new_path = path + [neighbor]
                    new_cost = cost + weight
                    
                    # Evitar ciclos e caminhos muito longos
                    if (neighbor not in path and 
                        (neighbor not in visited_levels or visited_levels[neighbor] >= len(new_path))):
                        visited_levels[neighbor] = len(new_path)
                        queue.append((neighbor, new_path, new_cost))
        
        if not all_paths:
            print(f"BFS: Não existe caminho entre {self.vertices[start]['nome']} e {self.vertices[target]['nome']}")
            return [], []
        
        # Para BFS, o ótimo é o de menor custo entre os de menor distância
        min_cost = min(all_costs)
        optimal_indices = [i for i, cost in enumerate(all_costs) if cost == min_cost]
        
        self._print_all_paths_results("BFS", all_paths, all_costs, optimal_indices, start, target)
        return all_paths, all_costs
    
    def dijkstra_all_paths(self, start: int, target: int) -> Tuple[List[List[int]], List[float]]:
        """
        Dijkstra que encontra TODOS os caminhos ótimos (mesmo custo mínimo)
        SEM usar bibliotecas externas
        """
        if not self._validate_input(start, target):
            return [], []
        
        if start == target:
            return [[start]], [0.0]
        
        n = len(self.vertices)
        distances = [float('inf')] * n
        distances[start] = 0.0
        
        # Armazenar TODOS os caminhos para cada vértice
        paths_to = {start: [[start]]}
        costs_to = {start: [0.0]}
        
        # Usar nossa implementação própria de heap
        pq = self.MinHeap()
        pq.push((0.0, start))
        visited = set()
        
        while not pq.is_empty():
            current_dist, current = pq.pop()
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor in range(n):
                weight = self.adjacency_matrix[current][neighbor]
                if weight > 0:
                    distance = current_dist + weight
                    
                    if distance < distances[neighbor]:
                        # Encontrou caminho melhor
                        distances[neighbor] = distance
                        paths_to[neighbor] = []
                        costs_to[neighbor] = []
                        
                        # Adicionar todos os caminhos que chegam ao current
                        for path in paths_to[current]:
                            new_path = path + [neighbor]
                            paths_to[neighbor].append(new_path)
                            costs_to[neighbor].append(distance)
                        
                        pq.push((distance, neighbor))
                    
                    elif distance == distances[neighbor]:
                        # Encontrou caminho alternativo com mesmo custo
                        for path in paths_to[current]:
                            new_path = path + [neighbor]
                            if new_path not in paths_to[neighbor]:
                                paths_to[neighbor].append(new_path)
                                costs_to[neighbor].append(distance)
        
        if target not in paths_to:
            print(f"Dijkstra: Não existe caminho entre {self.vertices[start]['nome']} e {self.vertices[target]['nome']}")
            return [], []
        
        all_paths = paths_to[target]
        all_costs = costs_to[target]
        
        # Todos os caminhos já são ótimos (mesmo custo)
        optimal_indices = list(range(len(all_paths)))
        
        self._print_all_paths_results("Dijkstra", all_paths, all_costs, optimal_indices, start, target)
        return all_paths, all_costs
    
    def floyd_warshall_all_paths(self, start: int, target: int) -> Tuple[List[List[int]], List[float]]:
        """
        Floyd-Warshall que encontra TODOS os caminhos ótimos
        """
        if not self._validate_input(start, target):
            return [], []
        
        if start == target:
            return [[start]], [0.0]
        
        n = len(self.vertices)
        
        # Inicializar matrizes de distância
        dist = [[float('inf')] * n for _ in range(n)]
        
        # Armazenar múltiplos próximos vértices para cada par
        next_vertices = [[[] for _ in range(n)] for _ in range(n)]
        
        # Inicializar distâncias diretas
        for i in range(n):
            dist[i][i] = 0.0
            for j in range(n):
                if self.adjacency_matrix[i][j] > 0:
                    dist[i][j] = self.adjacency_matrix[i][j]
                    next_vertices[i][j] = [j]
        
        # Floyd-Warshall principal
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        # Caminho melhor encontrado
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertices[i][j] = next_vertices[i][k].copy()
                    elif dist[i][k] + dist[k][j] == dist[i][j] and next_vertices[i][k]:
                        # Caminho alternativo com mesmo custo
                        for next_v in next_vertices[i][k]:
                            if next_v not in next_vertices[i][j]:
                                next_vertices[i][j].append(next_v)
        
        if dist[start][target] == float('inf'):
            print(f"Floyd-Warshall: Não existe caminho entre {self.vertices[start]['nome']} e {self.vertices[target]['nome']}")
            return [], []
        
        # Reconstruir todos os caminhos ótimos
        all_paths = []
        self._reconstruct_floyd_paths(start, target, next_vertices, [start], all_paths)
        
        optimal_cost = dist[start][target]
        all_costs = [optimal_cost] * len(all_paths)
        optimal_indices = list(range(len(all_paths)))
        
        self._print_all_paths_results("Floyd-Warshall", all_paths, all_costs, optimal_indices, start, target)
        return all_paths, all_costs
    
    def bellman_ford_all_paths(self, start: int, target: int) -> Tuple[List[List[int]], List[float]]:
        """
        Bellman-Ford que encontra TODOS os caminhos ótimos
        """
        if not self._validate_input(start, target):
            return [], []
        
        if start == target:
            return [[start]], [0.0]
        
        n = len(self.vertices)
        distances = [float('inf')] * n
        distances[start] = 0.0
        
        # Armazenar múltiplos predecessores para cada vértice
        predecessors = [[] for _ in range(n)]
        
        # Relaxamento das arestas (n-1) vezes
        for _ in range(n - 1):
            updated = False
            for i in range(n):
                for j in range(n):
                    weight = self.adjacency_matrix[i][j]
                    if weight > 0 and distances[i] != float('inf'):
                        if distances[i] + weight < distances[j]:
                            distances[j] = distances[i] + weight
                            predecessors[j] = [i]
                            updated = True
                        elif distances[i] + weight == distances[j] and i not in predecessors[j]:
                            predecessors[j].append(i)
                            updated = True
            
            if not updated:
                break
        
        # Verificar ciclos negativos
        for i in range(n):
            for j in range(n):
                weight = self.adjacency_matrix[i][j]
                if weight > 0 and distances[i] != float('inf'):
                    if distances[i] + weight < distances[j]:
                        print("Bellman-Ford: Ciclo negativo detectado!")
                        return [], []
        
        if distances[target] == float('inf'):
            print(f"Bellman-Ford: Não existe caminho entre {self.vertices[start]['nome']} e {self.vertices[target]['nome']}")
            return [], []
        
        # Reconstruir todos os caminhos ótimos
        all_paths = []
        self._reconstruct_bellman_paths(target, start, predecessors, [target], all_paths)
        
        # Reverter caminhos (foram construídos de trás para frente)
        all_paths = [path[::-1] for path in all_paths]
        
        optimal_cost = distances[target]
        all_costs = [optimal_cost] * len(all_paths)
        optimal_indices = list(range(len(all_paths)))
        
        self._print_all_paths_results("Bellman-Ford", all_paths, all_costs, optimal_indices, start, target)
        return all_paths, all_costs
    
    # ========================================
    # MÉTODOS AUXILIARES
    # ========================================
    
    def _validate_input(self, start: int, target: int) -> bool:
        """Validação de entrada para todos os algoritmos"""
        if not self.vertices:
            print("Erro: Grafo vazio!")
            return False
        
        if not (0 <= start < len(self.vertices)):
            print(f"Erro: Vértice de origem {start} inválido!")
            return False
        
        if not (0 <= target < len(self.vertices)):
            print(f"Erro: Vértice de destino {target} inválido!")
            return False
        
        return True
    
    def _print_all_paths_results(self, algorithm_name: str, all_paths: List[List[int]], 
                                all_costs: List[float], optimal_indices: List[int], 
                                start: int, target: int):
        """Imprime todos os caminhos encontrados e indica o(s) ótimo(s)"""
        
        print(f"\n{'='*60}")
        print(f"{algorithm_name}: {self.vertices[start]['nome']} → {self.vertices[target]['nome']}")
        print(f"{'='*60}")
        
        print(f"Total de caminhos encontrados: {len(all_paths)}")
        
        if len(all_paths) == 1:
            print(f"Caminho único:")
        else:
            print(f"Todos os caminhos:")
        
        for i, (path, cost) in enumerate(zip(all_paths, all_costs)):
            path_names = [self.vertices[v]['nome'] for v in path]
            is_optimal = i in optimal_indices
            status = " ★ ÓTIMO" if is_optimal else ""
            
            # Cálculos astronômicos
            km_total = cost * 150_000_000  # 1 UA = 150 milhões de km
            
            # Formatação da distância
            if km_total >= 1_000_000_000:  # Bilhões
                km_formatado = f"{km_total/1_000_000_000:.1f} bilhões de km"
            elif km_total >= 1_000_000:  # Milhões
                km_formatado = f"{km_total/1_000_000:.0f} milhões de km"
            else:
                km_formatado = f"{km_total:,.0f} km"
            
            print(f"  [{i+1:2d}] {' → '.join(path_names)}")
            print(f"       Custo total (Unidade Astronomica): {cost:.2f}")
            print(f"       Distancia real: {cost:.2f} × 150 milhões km = {km_formatado}{status}")
        
        if len(optimal_indices) > 1:
            print(f"\nCaminhos ótimos: {len(optimal_indices)} (mesmo custo mínimo)")
        elif len(optimal_indices) == 1:
            print(f"\nCaminho ótimo: #{optimal_indices[0]+1}")
    
    def _reconstruct_floyd_paths(self, start: int, target: int, next_vertices: List[List[List[int]]], 
                                current_path: List[int], all_paths: List[List[int]]):
        """Reconstrói recursivamente todos os caminhos do Floyd-Warshall"""
        if start == target:
            all_paths.append(current_path.copy())
            return
        
        for next_vertex in next_vertices[start][target]:
            new_path = current_path + [next_vertex]
            if next_vertex == target:
                all_paths.append(new_path.copy())
            else:
                self._reconstruct_floyd_paths(next_vertex, target, next_vertices, new_path, all_paths)
    
    def _reconstruct_bellman_paths(self, current: int, start: int, predecessors: List[List[int]], 
                                  current_path: List[int], all_paths: List[List[int]]):
        """Reconstrói recursivamente todos os caminhos do Bellman-Ford"""
        if current == start:
            all_paths.append(current_path.copy())
            return
        
        for pred in predecessors[current]:
            new_path = [pred] + current_path
            self._reconstruct_bellman_paths(pred, start, predecessors, new_path, all_paths)


def main():
    # Criar grafo não-direcionado e ponderado
    grafo = Graph(is_directed=False, is_weighted=True)
    
    while True:
        print(f"\n{'='*60}")
        print("                    REDE ESTELAR - ALGORITMOS DE BUSCA")
        print(f"{'='*60}")
        
        print("\nOPERACOES BASICAS:")
        print("1 - Adicionar vértice")
        print("2 - Remover vértice")
        print("3 - Atualizar vértice")
        print("4 - Consultar vértice")
        print("5 - Adicionar aresta")
        print("6 - Remover aresta")
        print("7 - Atualizar aresta")
        print("8 - Consultar aresta")
        print("9 - Listar informações do grafo")
        print("10 - Encontrar estrela mais brilhante")
        print("11 - Contar astros por constelação")
        print("12 - Listar todos os astros")
        print("13 - Qual menor estrela ou planeta?")
        print("14 - Listar estrelas mais conectadas")
        print("15 - Exibir matriz de adjacência")
        print("16 - Carregar Rede Estelar Predefinida")
        
        print("\nALGORITMOS DE BUSCA (TODOS OS CAMINHOS):")
        print("17 - Busca em Profundidade (DFS)")
        print("18 - Busca em Largura (BFS)")
        print("19 - Algoritmo de Dijkstra")
        print("20 - Algoritmo de Floyd-Warshall")
        print("21 - Algoritmo de Bellman-Ford")
        
        print("\n22 - Análise Comparativa de Algoritmos")
        print("0 - Sair")
        print(f"{'='*60}")
        
        opc = input("\nEscolha uma opção: ").strip()
        
        if opc == '0':
            print("Saindo...")
            break
        
        try:
            if opc == '1':  # Adicionar vértice
                nome = input("Nome do objeto celeste: ").strip()
                if not nome:
                    print("Nome não pode estar vazio.")
                    continue
                    
                magnitude = input("Magnitude (ou Enter para nulo): ")
                magnitude = float(magnitude) if magnitude else None
                constelacao = input("Constelação: ")
                
                vertex_data = {
                    'nome': nome,
                    'magnitude': magnitude,
                    'constelacao': constelacao
                }
                
                index = grafo.add_vertex(vertex_data)
                if index != -1:
                    print(f"Vértice '{nome}' adicionado com índice {index + 1}.")
            
            elif opc == '2':  # Remover vértice
                if not grafo.vertices:
                    print("Grafo vazio.")
                    continue
                
                grafo.listar_todas_estrelas()
                index = int(input("Índice do vértice a remover: ")) - 1
                grafo.remove_vertex(index)
            
            elif opc == '3':  # Atualizar vértice
                if not grafo.vertices:
                    print("Grafo vazio.")
                    continue
                
                grafo.listar_todas_estrelas()
                index = int(input("Índice do vértice a atualizar: ")) - 1
                
                nome = input("Novo nome (ou Enter para manter): ")
                magnitude = input("Nova magnitude (ou Enter para manter): ")
                constelacao = input("Nova constelação (ou Enter para manter): ")
                
                new_data = {}
                if nome:
                    new_data['nome'] = nome
                if magnitude:
                    new_data['magnitude'] = float(magnitude)
                if constelacao:
                    new_data['constelacao'] = constelacao
                
                grafo.update_vertex(index, new_data)
            
            elif opc == '4':  # Consultar vértice
                if not grafo.vertices:
                    print("Grafo vazio.")
                    continue
                
                grafo.listar_todas_estrelas()
                index = int(input("Índice do vértice a consultar: ")) - 1
                grafo.get_vertex_info(index)
            
            elif opc == '5':  # Adicionar aresta
                if len(grafo.vertices) < 2:
                    print("É necessário pelo menos 2 vértices.")
                    continue
                
                grafo.listar_todas_estrelas()
                v1 = int(input("Índice do primeiro vértice: ")) - 1
                v2 = int(input("Índice do segundo vértice: ")) - 1
                weight = float(input("Peso da aresta: "))
                
                grafo.add_edge(v1, v2, weight)
                v1_nome = grafo.vertices[v1]['nome']
                v2_nome = grafo.vertices[v2]['nome']
                print(f"Aresta adicionada entre '{v1_nome}' e '{v2_nome}' com peso {weight}.")
            
            elif opc == '6':  # Remover aresta
                if not grafo.vertices:
                    print("Grafo vazio.")
                    continue
                
                grafo.listar_todas_estrelas()
                v1 = int(input("Índice do primeiro vértice: ")) - 1
                v2 = int(input("Índice do segundo vértice: ")) - 1
                grafo.remove_edge(v1, v2)
            
            elif opc == '7':  # Atualizar aresta
                if not grafo.vertices:
                    print("Grafo vazio.")
                    continue
                
                grafo.listar_todas_estrelas()
                v1 = int(input("Índice do primeiro vértice: ")) - 1
                v2 = int(input("Índice do segundo vértice: ")) - 1
                new_weight = float(input("Novo peso: "))
                grafo.update_edge(v1, v2, new_weight)
            
            elif opc == '8':  # Consultar aresta
                if not grafo.vertices:
                    print("Grafo vazio.")
                    continue
                
                grafo.listar_todas_estrelas()
                v1 = int(input("Índice do primeiro vértice: ")) - 1
                v2 = int(input("Índice do segundo vértice: ")) - 1
                grafo.get_edge_info(v1, v2)
            
            elif opc == '9':  # Informações do grafo
                grafo.list_graph_info()
            
            elif opc == '10':  # Estrela mais brilhante
                grafo.find_brightest_star()
            
            elif opc == '11':  # Contar por constelação
                grafo.count_by_constellation()
            
            elif opc == '12':  # Listar todas
                grafo.listar_todas_estrelas()
            
            elif opc == '13':  # Menor estrela/planeta
                grafo.find_brightest_star()  # Reutiliza a função
            
            elif opc == '14':  # Mais conectadas
                grafo.list_most_connected_stars()
            
            elif opc == '15':  # Matriz de adjacência
                grafo.exibir_matriz_adjacencia()
            
            elif opc == '16':  # Carregar predefinida
                grafo.carregar_rede_estelar_predefinida()
                
                # Informações adicionais após carregamento
                print("\n========== REDE ESTELAR CARREGADA COM SUCESSO! ==========")
                print(f">>> {len(grafo.vertices)} objetos celestes inseridos")
                print(">>> 28 rotas espaciais estabelecidas")
                print(">>> Grafo configurado como NAO-DIRECIONADO (viagens bidirecionais)")
                
                print(f"\nDETALHAMENTO DOS OBJETOS ADICIONADOS:")
                print(f"   PLANETAS DO SISTEMA SOLAR: 9")
                print(f"      Mercurio, Venus, Terra, Marte, Jupiter, Saturno, Urano, Netuno, Plutao")
                print(f"   ESTRELAS EM CONSTELACOES: 8")  
                print(f"      Betelgeuse, Rigel, Antares, Shaula, Dubhe, Merak, Markab, Scheat")
                print(f"   CONSTELACOES: 4")
                print(f"      Orion, Escorpiao, Ursa Maior, Pegaso")
                print(f"   SOL: 1 (centro do sistema)")
                print(f"============================================================")
            
            elif opc in ['17', '18', '19', '20', '21']:  # Algoritmos individuais
                if not grafo.vertices:
                    print("Carregue primeiro uma rede (opção 16).")
                    continue
                
                grafo.listar_todas_estrelas()
                start = int(input("Vértice de origem: ")) - 1
                target = int(input("Vértice de destino: ")) - 1
                
                if opc == '17':
                    paths, costs = grafo.dfs_all_paths(start, target)
                elif opc == '18':
                    paths, costs = grafo.bfs_all_paths(start, target)
                elif opc == '19':
                    paths, costs = grafo.dijkstra_all_paths(start, target)
                elif opc == '20':
                    paths, costs = grafo.floyd_warshall_all_paths(start, target)
                elif opc == '21':
                    paths, costs = grafo.bellman_ford_all_paths(start, target)
            
            elif opc == '22':  # Análise comparativa
                if not grafo.vertices:
                    print("Carregue primeiro uma rede (opção 16).")
                    continue
                
                grafo.listar_todas_estrelas()
                start = int(input("Vértice de origem: ")) - 1
                target = int(input("Vértice de destino: ")) - 1
                
                algorithms = [
                    ("DFS", grafo.dfs_all_paths),
                    ("BFS", grafo.bfs_all_paths),
                    ("Dijkstra", grafo.dijkstra_all_paths),
                    ("Floyd-Warshall", grafo.floyd_warshall_all_paths),
                    ("Bellman-Ford", grafo.bellman_ford_all_paths)
                ]
                
                print(f"\n{'='*80}")
                print("                    ANÁLISE COMPARATIVA COMPLETA")
                print(f"{'='*80}")
                
                for name, algorithm in algorithms:
                    try:
                        paths, costs = algorithm(start, target)
                        print(f"\n{name} executado com sucesso!")
                    except Exception as e:
                        print(f"\nErro em {name}: {e}")
            
            else:
                print("Opção inválida.")
        
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except IndexError:
            print("Índice fora do intervalo válido.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()