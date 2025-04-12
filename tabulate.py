import networkx as nx
import numpy as np
from tabulate import tabulate

# Se ainda não instalou tabulate:
# pip install tabulate

# Crie ou carregue o seu grafo (direcionado ou não)
G = nx.DiGraph()

# Lista de vértices de exemplo
vertices = [
    "Const", "Betel", "Rigel", "Antar",
    "Shaul", "Dubhe", "Merak", "Const2",
    "Marka", "Algem", "Sol", "Mercú",
    "Vênus", "Terra", "Marte", "Júpit",
    "Satur", "Urano"
]

# Adicione nós ao grafo
G.add_nodes_from(vertices)

# Exemplo de algumas arestas
edges = [
    ("Const", "Betel"),
    ("Const", "Rigel"),
    ("Betel", "Rigel"),
    ("Antar", "Shaul"),
    ("Sol", "Mercú"),
    ("Mercú", "Vênus"),
    ("Vênus", "Terra"),
    ("Terra", "Marte"),
    ("Marte", "Júpit"),
    ("Júpit", "Satur"),
    ("Satur", "Urano"),
]
G.add_edges_from(edges)

# Gera a matriz de adjacência como array NumPy
# (Se você precisar preservar paralelos entre nós, use list(G.nodes()) consistentemente)
A = nx.to_numpy_array(G, nodelist=vertices)

# Monta a tabela para exibir, com a primeira coluna sendo o nome da linha
table = []
for i, v_label in enumerate(vertices):
    # Cada linha começa com o nome do vértice + os valores 0 ou 1
    row = [v_label] + list(A[i].astype(int))
    table.append(row)

# Cabeçalhos: primeiro " " (ou algo parecido) e depois os nomes dos vértices (colunas)
headers = [""] + vertices

# Impressão em formato tabular no terminal
print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
