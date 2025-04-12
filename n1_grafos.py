from typing import Any, Dict, List, Optional

class Graph:
    def __init__(self, is_directed: bool = True, is_weighted: bool = False):
        """
        Grafo com armazenamento dinâmico em matriz de adjacências.
        :param is_directed: Se True, o grafo é direcionado.
        :param is_weighted: Se True, as arestas podem ter 'peso' (float).
        """
        self.is_directed = is_directed
        self.is_weighted = is_weighted
        
        # Lista de vértices (cada vértice = dict com dados, ex. nome, magnitude etc.)
        self.vertices: List[Dict[str, Any]] = []
        
        # Matriz de adjacências (lista de listas). Cresce dinamicamente conforme add_vertex é chamado.
        self.adjacency_matrix: List[List[float]] = []

    # -------------------------------------------------------------------
    # Métodos de Manipulação de Vértice
    # -------------------------------------------------------------------
    
    def add_vertex(self, vertex_data: Dict[str, Any]) -> int:
        """
        Adiciona um novo vértice e retorna o índice (0-based interno).
        A matriz de adjacências é expandida em uma linha e uma coluna.
        """
        self.vertices.append(vertex_data)
        new_size = len(self.vertices)
        
        # Expande a matriz: uma nova linha e uma nova coluna
        self.adjacency_matrix.append([0.0]*(new_size - 1))
        for row in self.adjacency_matrix:
            row.append(0.0)
        
        return new_size - 1

    def remove_vertex(self, vertex_index: int) -> None:
        """
        Remove o vértice (e todas as arestas) do grafo.
        Aqui, vertex_index é 0-based interno.
        """
        if 0 <= vertex_index < len(self.vertices):
            self.vertices.pop(vertex_index)
            self.adjacency_matrix.pop(vertex_index)
            for row in self.adjacency_matrix:
                row.pop(vertex_index)
        else:
            print(f"Índice {vertex_index+1} inválido para remoção de vértice.")

    def update_vertex(self, vertex_index: int, new_data: Dict[str, Any]) -> None:
        """
        Atualiza os dados de um vértice específico (0-based interno).
        """
        if 0 <= vertex_index < len(self.vertices):
            self.vertices[vertex_index].update(new_data)
        else:
            print(f"Vértice {vertex_index+1} não encontrado para atualização.")

    def get_vertex(self, vertex_index: int) -> Optional[Dict[str, Any]]:
        """
        Retorna os dados do vértice (0-based interno) ou None se não existir.
        """
        if 0 <= vertex_index < len(self.vertices):
            return self.vertices[vertex_index]
        return None

    # -------------------------------------------------------------------
    # Métodos de Manipulação de Arestas
    # -------------------------------------------------------------------
    
    def add_edge(self, v1: int, v2: int, weight: float = 1.0) -> None:
        """
        Adiciona uma aresta entre v1 e v2 (0-based interno).
        Se is_directed=True, só v1->v2. Se is_directed=False, também v2->v1.
        """
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            print(f"Índices de vértices inválidos: {v1+1}, {v2+1}.")
            return
        
        val = weight if self.is_weighted else 1.0
        self.adjacency_matrix[v1][v2] = val
        
        if not self.is_directed:
            self.adjacency_matrix[v2][v1] = val

    def remove_edge(self, v1: int, v2: int) -> None:
        """
        Remove a aresta entre v1 e v2 (0-based interno).
        Se não for direcionado, remove ambos os lados.
        """
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            print(f"Índices de vértices inválidos: {v1+1}, {v2+1}.")
            return
        
        self.adjacency_matrix[v1][v2] = 0.0
        if not self.is_directed:
            self.adjacency_matrix[v2][v1] = 0.0

    def update_edge(self, v1: int, v2: int, new_weight: float) -> None:
        """
        Atualiza o peso de uma aresta específica (0-based interno).
        Só faz sentido se is_weighted=True.
        """
        if not self.is_weighted:
            print("Grafo não é valorado. Não há peso para atualizar.")
            return
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            print(f"Índices de vértices inválidos: {v1+1}, {v2+1}.")
            return
        
        self.adjacency_matrix[v1][v2] = new_weight
        if not self.is_directed:
            self.adjacency_matrix[v2][v1] = new_weight

    def get_edge(self, v1: int, v2: int) -> float:
        """
        Retorna o valor da aresta (ou 0 se não existir).
        (0-based interno)
        """
        if not (0 <= v1 < len(self.vertices)) or not (0 <= v2 < len(self.vertices)):
            return 0.0
        return self.adjacency_matrix[v1][v2]

    # -------------------------------------------------------------------
    # Métodos de Consulta / Visualização
    # -------------------------------------------------------------------
    
    def list_graph_info(self) -> None:
        """
        Exibe informações do grafo:
          - se é direcionado ou não
          - se é valorado ou não
          - se tem laço
          - grau de entrada/saída de cada vértice
        """
        print("="*60)
        print(f"Grafo é {'direcionado' if self.is_directed else 'não-direcionado'}.")
        print(f"Grafo é {'valorado' if self.is_weighted else 'não-valorado'}.")
        
        # Verificar laços
        has_loop = any(self.adjacency_matrix[i][i] != 0 for i in range(len(self.vertices)))
        print(f"Possui laço: {'Sim' if has_loop else 'Não'}\n")

        for i in range(len(self.vertices)):
            vname = self.vertices[i].get("nome", f"VérticeDesconhecido{i+1}")
            out_degree = sum(1 for val in self.adjacency_matrix[i] if val != 0)
            in_degree = sum(1 for row in self.adjacency_matrix if row[i] != 0)
            print(f"[{i+1}] {vname}: grau entrada={in_degree}, grau saída={out_degree}")

        print("="*60)

    def find_brightest_star(self) -> Optional[int]:
        """
        Retorna o índice (0-based) do astro com a menor magnitude (mais brilhante).
        """
        if not self.vertices:
            return None
        
        brightest_idx = None
        smallest_magnitude = 99999.0
        
        for i, v in enumerate(self.vertices):
            mag = v.get("magnitude", 99999.0)
            try:
                mag_float = float(mag)
            except:
                mag_float = 99999.0
            
            if mag_float < smallest_magnitude:
                smallest_magnitude = mag_float
                brightest_idx = i
        
        return brightest_idx

    def count_stars_by_constellation(self) -> Dict[str, int]:
        """
        Conta quantos vértices há em cada constelação (chave 'constelacao').
        """
        const_count = {}
        for v in self.vertices:
            c = v.get("constelacao", "Desconhecida")
            const_count[c] = const_count.get(c, 0) + 1
        return const_count

    def listar_todas_estrelas(self) -> None:
        """
        Lista todos os vértices, mostrando índice (1-based), nome, magnitude, constelação, etc.
        """
        if not self.vertices:
            print("Não há nenhum vértice no grafo.")
            return
        
        print("\n=== Lista de Vértices (Índice inicia em 1) ===")
        for i, v in enumerate(self.vertices):
            nome = v.get("nome", f"Vértice{i+1}")
            mag = v.get("magnitude", "N/A")
            const = v.get("constelacao", "N/A")
            print(f"[{i+1}] Nome: {nome}, Magnitude: {mag}, Constelação: {const}")
        print("===================================\n")

    def imprimir_matriz_adjacencia(self):
        """
        Exibe a matriz de adjacência de forma abreviada (nome[:5]).
        Mostra 0 ou 1 (sem decimais) para facilitar leitura.
        """
        n = len(self.vertices)
        if n == 0:
            print("Grafo vazio. Sem vértices para exibir.")
            return
        
        print("\nMATRIZ DE ADJACÊNCIA (abreviada)\n")
        
        # Cabeçalho
        print("     ", end="")
        for col in range(n):
            nome_c = self.vertices[col].get("nome", f"V{col+1}")[:5]
            print(f"{nome_c:>6}", end="")
        print()

        # Linhas
        for lin in range(n):
            nome_l = self.vertices[lin].get("nome", f"V{lin+1}")[:5]
            print(f"{nome_l:>5}", end="")
            for col in range(n):
                val = self.adjacency_matrix[lin][col]
                if val != 0.0:
                    print(f"{1:>6}", end="")  # se houver aresta, imprime 1
                else:
                    print(f"{0:>6}", end="")  # senão 0
            print()
        print()

    def find_largest_star(self) -> Optional[int]:
        """
        Retorna o índice (0-based) do astro com a 'maior' magnitude (valor numérico mais alto).
        """
        if not self.vertices:
            return None
        
        largest_idx = None
        largest_mag = -99999.0
        
        for i, v in enumerate(self.vertices):
            mag = v.get("magnitude", None)
            if mag is None:
                continue
            try:
                mag_float = float(mag)
            except:
                continue
            
            if mag_float > largest_mag:
                largest_mag = mag_float
                largest_idx = i
        
        return largest_idx

    def listar_estrelas_mais_conectadas(self) -> None:
        """
        Lista os vértices em ordem decrescente de 'conexões' (grau total = entrada + saída).
        """
        n = len(self.vertices)
        if n == 0:
            print("Grafo vazio, sem vértices.")
            return
        
        ranking = []
        for i in range(n):
            out_degree = sum(1 for val in self.adjacency_matrix[i] if val != 0)
            in_degree = sum(1 for row in self.adjacency_matrix if row[i] != 0)
            total = out_degree + in_degree
            ranking.append((i, total))
        
        ranking.sort(key=lambda x: x[1], reverse=True)

        print("\nEstrelas (vértices) mais conectadas - ordem decrescente:")
        for idx, total in ranking:
            nome = self.vertices[idx].get("nome", f"Vértice{idx+1}")
            print(f"  [{idx+1}] {nome} - conexões: {total}")
        print()

    # -------------------------------------------------------------------
    # CARREGAR REDE ESTELAR PREDEFINIDA
    # -------------------------------------------------------------------
    def carregar_rede_estelar_predefinida(self) -> None:
        """
        Limpa o grafo atual e carrega 23 vértices e as arestas
        (incluindo Netuno e Plutão), com as conexões solicitadas.
        """
        self.vertices = []
        self.adjacency_matrix = []

        dados_vertices = [
          {"nome":"Constelação de Órion","magnitude":None,"constelacao":"Área do céu"},
          {"nome":"Betelgeuse (estrela em Órion)","magnitude":0.42,"constelacao":"Órion"},
          {"nome":"Rigel (estrela em Órion)","magnitude":0.12,"constelacao":"Órion"},
          {"nome":"Constelação de Escorpião","magnitude":None,"constelacao":"Área do céu"},
          {"nome":"Antares (estrela em Escorpião)","magnitude":1.09,"constelacao":"Escorpião"},
          {"nome":"Shaula (estrela em Escorpião)","magnitude":1.62,"constelacao":"Escorpião"},
          {"nome":"Constelação da Ursa Maior","magnitude":None,"constelacao":"Área do céu"},
          {"nome":"Dubhe (estrela na Ursa Maior)","magnitude":1.79,"constelacao":"Ursa Maior"},
          {"nome":"Merak (estrela na Ursa Maior)","magnitude":2.34,"constelacao":"Ursa Maior"},
          {"nome":"Constelação de Pégaso","magnitude":None,"constelacao":"Área do céu"},
          {"nome":"Markab (estrela em Pégaso)","magnitude":2.48,"constelacao":"Pégaso"},
          {"nome":"Algenib (estrela em Pégaso)","magnitude":2.84,"constelacao":"Pégaso"},
          {"nome":"Sol","magnitude":-26.74,"constelacao":"Sistema Solar"},
          {"nome":"Mercúrio","magnitude":-2.45,"constelacao":"Sistema Solar"},
          {"nome":"Vênus","magnitude":-4.89,"constelacao":"Sistema Solar"},
          {"nome":"Terra","magnitude":None,"constelacao":"Sistema Solar"},
          {"nome":"Marte","magnitude":-2.91,"constelacao":"Sistema Solar"},
          {"nome":"Júpiter","magnitude":-2.94,"constelacao":"Sistema Solar"},
          {"nome":"Saturno","magnitude":-0.55,"constelacao":"Sistema Solar"},
          {"nome":"Urano","magnitude":5.7,"constelacao":"Sistema Solar"},
          {"nome":"Netuno","magnitude":7.8,"constelacao":"Sistema Solar"},
          {"nome":"Plutão","magnitude":14.0,"constelacao":"Sistema Solar"}
        ]
        
        for v in dados_vertices:
            self.add_vertex(v)

        edges = [
          # Constelações -> Estrelas
          ("Constelação de Órion","Betelgeuse (estrela em Órion)"),
          ("Constelação de Órion","Rigel (estrela em Órion)"),
          ("Constelação de Escorpião","Antares (estrela em Escorpião)"),
          ("Constelação de Escorpião","Shaula (estrela em Escorpião)"),
          ("Constelação da Ursa Maior","Dubhe (estrela na Ursa Maior)"),
          ("Constelação da Ursa Maior","Merak (estrela na Ursa Maior)"),
          ("Constelação de Pégaso","Markab (estrela em Pégaso)"),
          ("Constelação de Pégaso","Algenib (estrela em Pégaso)"),

          # Sol <-> Planetas (ida e volta)
          ("Sol","Mercúrio"), ("Mercúrio","Sol"),
          ("Sol","Vênus"),    ("Vênus","Sol"),
          ("Sol","Terra"),    ("Terra","Sol"),
          ("Sol","Marte"),    ("Marte","Sol"),
          ("Sol","Júpiter"),  ("Júpiter","Sol"),
          ("Sol","Saturno"),  ("Saturno","Sol"),
          ("Sol","Urano"),    ("Urano","Sol"),
          ("Sol","Netuno"),   ("Netuno","Sol"),
          ("Sol","Plutão"),   ("Plutão","Sol"),

          # Vizinhança orbital
          ("Mercúrio","Vênus"),
          ("Vênus","Terra"),
          ("Terra","Marte"),
          ("Marte","Júpiter"),
          ("Júpiter","Saturno"),
          ("Saturno","Urano"),
          ("Urano","Netuno"),
          ("Netuno","Plutão")
        ]

        def indice_por_nome(nome_busca: str) -> int:
            for i, vt in enumerate(self.vertices):
                if vt.get("nome","") == nome_busca:
                    return i
            return -1
        
        for (origem, destino) in edges:
            i1 = indice_por_nome(origem)
            i2 = indice_por_nome(destino)
            if i1 != -1 and i2 != -1:
                self.add_edge(i1, i2)

        print("\nRede Estelar Predefinida carregada com sucesso!")
        print(f"Foram inseridos {len(self.vertices)} vértices e {len(edges)} arestas.\n")

# ---------------------------------------------------------------------------
# Menu Interativo
# ---------------------------------------------------------------------------

def menu_interativo():
    grafo = Graph(is_directed=True, is_weighted=False)

    while True:
        print("\n=== MENU ===")
        print("1 - Adicionar vértice")
        print("2 - Remover vértice")
        print("3 - Atualizar vértice")
        print("4 - Consultar vértice")
        print("5 - Adicionar aresta")
        print("6 - Remover aresta")
        print("7 - Atualizar aresta (só se valorado)")
        print("8 - Consultar aresta")
        print("9 - Listar dados do grafo (grau entrada/saída)")
        print("10 - Encontrar estrela mais brilhante")
        print("11 - Contar astros por constelação")
        print("12 - Listar todos os astros")
        print("13 - Qual menor estrela ou planeta?")
        print("14 - Listar estrelas mais conectadas")
        print("15 - Exibir matriz de adjacência")
        print("16 - Carregar Rede Estelar Predefinida")
        print("0 - Sair")

        opc = input("Escolha uma opção: ")

        if opc == '0':
            print("Encerrando programa...")
            break

        elif opc == '1':
            nome = input("Digite o nome do vértice: ")
            mag = input("Digite a magnitude (ou deixe em branco): ")
            const = input("Digite a constelação (ou outro dado): ")
            try:
                mag_float = float(mag)
            except:
                mag_float = None
            data = {"nome": nome, "magnitude": mag_float, "constelacao": const}
            idx_interno = grafo.add_vertex(data)
            print(f"Vértice '{nome}' adicionado com índice interno {idx_interno+1}.")

        elif opc == '2':
            idx_str = input("Digite o índice do vértice para remover (Índice inicia em 1): ")
            try:
                idx_interno = int(idx_str) - 1
            except:
                print("Índice inválido.")
                continue
            grafo.remove_vertex(idx_interno)

        elif opc == '3':
            idx_str = input("Digite o índice do vértice a atualizar (Índice inicia em 1): ")
            try:
                idx_interno = int(idx_str) - 1
            except:
                print("Índice inválido.")
                continue

            novo_nome = input("Novo nome (ou Enter para não alterar): ")
            nova_mag = input("Nova magnitude (ou Enter para não alterar): ")
            nova_const = input("Nova constelação (ou Enter para não alterar): ")

            atualizacoes = {}
            if novo_nome.strip():
                atualizacoes['nome'] = novo_nome
            if nova_mag.strip():
                try:
                    atualizacoes['magnitude'] = float(nova_mag)
                except:
                    pass
            if nova_const.strip():
                atualizacoes['constelacao'] = nova_const

            grafo.update_vertex(idx_interno, atualizacoes)

        elif opc == '4':
            idx_str = input("Digite o índice do vértice (Índice inicia em 1): ")
            try:
                idx_interno = int(idx_str) - 1
            except:
                print("Índice inválido.")
                continue
            v = grafo.get_vertex(idx_interno)
            if v is None:
                print("Vértice não encontrado.")
            else:
                print(f"Dados do vértice [{idx_interno+1}]: {v}")

        elif opc == '5':
            v1_str = input("Índice do vértice origem (Índice inicia em 1): ")
            v2_str = input("Índice do vértice destino (Índice inicia em 1): ")
            try:
                v1 = int(v1_str) - 1
                v2 = int(v2_str) - 1
            except:
                print("Índices inválidos.")
                continue

            if grafo.is_weighted:
                w_str = input("Peso da aresta: ")
                try:
                    w = float(w_str)
                except:
                    w = 1.0
                grafo.add_edge(v1, v2, w)
            else:
                grafo.add_edge(v1, v2)
            print("Aresta adicionada (se índices válidos).")

        elif opc == '6':
            v1_str = input("Índice do vértice origem (Índice inicia em 1): ")
            v2_str = input("Índice do vértice destino (Índice inicia em 1): ")
            try:
                v1 = int(v1_str) - 1
                v2 = int(v2_str) - 1
            except:
                print("Índices inválidos.")
                continue
            grafo.remove_edge(v1, v2)

        elif opc == '7':
            if not grafo.is_weighted:
                print("Grafo não é valorado. Opção inválida.")
            else:
                v1_str = input("Índice do vértice origem (Índice inicia em 1): ")
                v2_str = input("Índice do vértice destino (Índice inicia em 1): ")
                try:
                    v1 = int(v1_str) - 1
                    v2 = int(v2_str) - 1
                except:
                    print("Índices inválidos.")
                    continue
                new_w_str = input("Novo peso: ")
                try:
                    new_w = float(new_w_str)
                except:
                    new_w = 1.0
                grafo.update_edge(v1, v2, new_w)

        elif opc == '8':
            v1_str = input("Índice do vértice origem (Índice inicia em 1): ")
            v2_str = input("Índice do vértice destino (Índice inicia em 1): ")
            try:
                v1 = int(v1_str) - 1
                v2 = int(v2_str) - 1
            except:
                print("Índices inválidos.")
                continue
            val = grafo.get_edge(v1, v2)
            if val == 0.0:
                print("Aresta não existe (ou valor=0).")
            else:
                print(f"Aresta existe. Valor (peso): {val}")

        elif opc == '9':
            grafo.list_graph_info()

        elif opc == '10':
            idx_brilh = grafo.find_brightest_star()
            if idx_brilh is None:
                print("Não foi encontrada nenhuma magnitude válida.")
            else:
                v = grafo.get_vertex(idx_brilh)
                print(f"Mais brilhante é [{idx_brilh+1}]: {v}")

        elif opc == '11':
            ccount = grafo.count_stars_by_constellation()
            print("Quantidade de astros em cada constelação:")
            for const, qtde in ccount.items():
                print(f"  {const}: {qtde}")

        elif opc == '12':
            grafo.listar_todas_estrelas()

        elif opc == '15':
            grafo.imprimir_matriz_adjacencia()

        elif opc == '16':
            grafo.carregar_rede_estelar_predefinida()

        elif opc == '12':
            idx_maior = grafo.find_largest_star()
            if idx_maior is None:
                print("Não há magnitudes válidas para calcular a 'maior'.")
            else:
                v = grafo.get_vertex(idx_maior)
                print(f"Maior magnitude é [{idx_maior+1}]: {v}")

        elif opc == '13':
            grafo.listar_estrelas_mais_conectadas()

        else:
            print("Opção inválida. Tente novamente.")

def main():
    menu_interativo()

if __name__ == "__main__":
    main()
