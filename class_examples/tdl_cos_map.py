import networkx as nx
import osmnx as ox

ox.settings.bidirectional_network_types += "drive"
G = ox.graph.graph_from_place("Colorado Springs, Colorado, USA", network_type="drive")
# fig, ax = ox.plot.plot_graph(G, edge_linewidth=.2, node_size=0)

G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

# UCCS
orig = ox.distance.nearest_nodes(G, X=-104.80079959955438, Y=38.89284009494745)
# Airport
dest = ox.distance.nearest_nodes(G, X=-104.7114257661276, Y=38.80484732844506)

route = ox.routing.shortest_path(G, orig, dest, weight="travel_time")
fix, ax = ox.plot.plot_graph_route(G, route, node_size=0)