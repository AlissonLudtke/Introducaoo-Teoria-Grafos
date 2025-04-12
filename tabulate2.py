import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Supondo que você já tenha seu grafo G criado anteriormente:
# Aqui está um exemplo simplificado:
G = nx.DiGraph()
vertices = [
    "Constelação de Órion", "Betelgeuse", "Rigel",
    "Constelação de Escorpião", "Antares", "Shaula",
    "Constelação da Ursa Maior", "Dubhe", "Merak",
    "Constelação de Pégaso", "Markab", "Algenib",
    "Sol", "Mercúrio", "Vênus", "Terra", "Marte",
    "Júpiter", "Saturno", "Urano", "Netuno", "Plutão"
]
G.add_nodes_from(vertices)

# Exemplo de algumas arestas
edges = [
    ("Constelação de Órion", "Betelgeuse"),
    ("Constelação de Órion", "Rigel"),
    ("Constelação de Escorpião", "Antares"),
    ("Constelação de Escorpião", "Shaula"),
    ("Sol", "Mercúrio"),
    ("Mercúrio", "Sol"),
    ("Sol", "Vênus"),
    ("Vênus", "Sol"),
    ("Sol", "Terra"),
    ("Terra", "Sol"),
    ("Sol", "Marte"),
    ("Marte", "Sol"),
    ("Mercúrio", "Vênus"),
    ("Vênus", "Terra"),
    ("Terra", "Marte")
]
G.add_edges_from(edges)

# Gerando a matriz de adjacência e convertendo para um DataFrame
A = nx.adjacency_matrix(G).todense()
labels = list(G.nodes())
df = pd.DataFrame(A, index=labels, columns=labels)

# Configurando e exibindo um heatmap para visualizar a matriz de adjacência
plt.figure(figsize=(12, 10))
sns.heatmap(df, annot=True, fmt="d", cmap="Blues", cbar=True)
plt.title("Matriz de Adjacência do Grafo")
plt.xlabel("Vértices")
plt.ylabel("Vértices")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=1)
plt.show()
