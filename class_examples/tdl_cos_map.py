import networkx as nx
import osmnx as ox

place = {"city": "Colorado Springs", "state": "Colorado", "country": "USA"}
G = ox.graph.graph_from_place(place, network_type="drive", truncate_by_edge=True)
# fig, ax = ox.plot.plot_graph(G, figsize=(10, 10), node_size=0, edge_color="y", edge_linewidth=0.2)

G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

# UCCS
orig = ox.distance.nearest_nodes(G, X=-104.80079959955438, Y=38.89284009494745)
# Airport
dest = ox.distance.nearest_nodes(G, X=-104.7114257661276, Y=38.80484732844506)

route = ox.routing.shortest_path(G, orig, dest, weight="travel_time")
fix, ax = ox.plot.plot_graph_route(G, route, node_size=0)