import networkx as nx
import hw1_tools as tl

pl_graph = nx.generators.random_graphs.powerlaw_cluster_graph(100, 2, 0.2, create_using=None, seed=None)

for i in range(110):
	print 'iteration: ', i
	pl_graph = nx.generators.random_graphs.powerlaw_cluster_graph((i+1)*100, 2, 0.2, pl_graph)
	"""
	histogram = nx.classes.function.degree_histogram(pl_graph)
	print histogram
	print tl.avg_cluster(pl_graph)
	print nx.algorithms.shortest_paths.generic.average_shortest_path_length(pl_graph)
	print nx.algorithms.mixing.degree_assortativity(pl_graph)
	print tl.giant_CC(pl_graph)
	print nx.algorithms.distance_measures.diameter(pl_graph)
	"""
	nx.write_adjlist(pl_graph,"graph/pl.adjlist.it"+str(i))
