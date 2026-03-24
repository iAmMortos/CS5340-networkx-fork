import networkx as nx

G = nx.cycle_graph(3)
spanning_trees = nx.SpanningTreeIterator(G)
next(spanning_trees)


