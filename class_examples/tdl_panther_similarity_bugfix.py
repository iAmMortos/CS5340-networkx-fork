import networkx as nx

# algorithms/similarity:panther_similarity

### Bugged example
if False:
  G = nx.Graph()
  G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3)])
  nx.panther_similarity(G, source=0)

### Working example
if True:
  G = nx.star_graph(10)
  sim = nx.panther_similarity(G, 0)
  print(sim)


