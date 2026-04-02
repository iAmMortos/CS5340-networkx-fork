import networkx as nx
import osmnx as ox

ox.settings.use_cache = True

G = ox.graph.graph_from_point((37.79, -122.41), dist=750, network_type="drive")

G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

gdf_nodes, gdf_edges = ox.convert.graph_to_gdfs(G)
G = ox.convert.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)

D = ox.convert.to_digraph(G, weight="travel_time")

bc = nx.betweenness_centrality(D, weight="travel_time", normalized=True)
nx.set_node_attributes(G, values=bc, name="bc")

nc = ox.plot.get_node_colors_by_attr(G, "bc", cmap="plasma")
fig, ax = ox.plot.plot_graph(G, bgcolor="k", node_color=nc, node_size=50, edge_linewidth=2, edge_color="#333333")

ox.io.save_graph_geopackage(G, filepath="./graph.gpkg")
ox.io.save_graphml(G, filepath="./graph.graphm1")