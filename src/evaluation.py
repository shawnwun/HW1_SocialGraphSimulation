import networkx as nx
import hw1_tools as tl
import sys
import os

def evaluation(graph):
    print '---------------------------------'
    histogram = nx.classes.function.degree_histogram(graph)
    print '########## Histogram ############'
    for his in histogram:
	print str(his) + "  ",
    print
    print "Cluster_Coeff:     ", tl.avg_cluster(graph)
    print "AVG_Shortest_Path: ", nx.algorithms.shortest_paths.generic.average_shortest_path_length(graph)
#    print "Assortativity:     ", nx.algorithms.mixing.degree_assortativity(graph)
    print "Giant_Component:   ", tl.giant_CC(graph)
    print "Diameter:          ", nx.algorithms.distance_measures.diameter(graph)
    print "Densification:	  ", str(nx.number_of_nodes(graph)) + "	" + str(nx.number_of_edges(graph))
    print '--------------------------------'
    print


filename = sys.argv[1]
graph = nx.read_adjlist(filename)
evaluation(graph)

"""
for root, Dir, Files in os.walk(sys.argv[1]):
    for f in Files:
	filename = os.path.join(root,f)                                         
	graph = nx.read_adjlist(filename)
	print filename
	evaluation(graph)
"""
