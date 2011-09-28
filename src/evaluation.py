import networkx as nx
import hw1_tools as tl
import sys

graph = nx.read_adjlist(sys.argv[1])

histogram = nx.classes.function.degree_histogram(graph)
print histogram
print "Cluster_Coeff:     ", tl.avg_cluster(graph)
print "AVG_Shortest_Path: ", nx.algorithms.shortest_paths.generic.average_shortest_path_length(graph)
print "Assortativity:     ", nx.algorithms.mixing.degree_assortativity(graph)
print "Giant_Component:   ", tl.giant_CC(graph)
print "Diameter:          ", nx.algorithms.distance_measures.diameter(graph)

