import networkx as nx

ws_graph = nx.generators.random_graphs.watts_strogatz_graph(10000,100,0.0001,create_using=None,seed=None)
nx.write_adjlist(ws_graph,"graph/ws.adjlist")

#print networkx.algorithms.shortest_paths.generic.shortest_path(nws_graph,source=None,target=None,weight=None)

