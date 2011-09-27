from networkx import *
from math import log, ceil

# Part 1, 2: Calculating KL Divergence
# Assume x and y are of the same length (and already a prob distribution

def KL_divergence(x, y):
        total=0.0
        for i in range(len(x)):
                total=total+x[i]*log(x[i]/y[i])
        return total

# Part 1, 2: transform distribution to histogram-like structure
# Input: A graph (a set of dead people or the entire network)
# Assume each node has an "age" attribute
# Output: A dict where index are ages and values are cumulated count

def normalize_age(t):
        age=0
        normalizing_const=1
        age=ceil(t/normalizing_const)
        if age>100:
                age=100
        return age

def transform_dist(G):
        dict={}
        count=0
        for i in range(101):
                dict.update({i: 0})
        for v in G:
                dict[v.age()]=dict[v.age()]+1
                count=count+1
        for i in range(101):
                dict[i]=dict[i]/count
        return dict

# Part 3: Power-law degree distribution
# Usage: list=degree_histogram(G)
# (returns a list of degree frequency ex. [0, 1, 5, 3, 1] means 0 nodes for deg 0
# 1 nodes for deg 1, and so on

# Part 4: clustering coefficient
# Could use average_clustering(G) (but it could be slower due to its space saving

def avg_cluster(G):
        dic=clustering(G)
        avg=0.0
        for v in dic.keys():
                avg=avg+dic[v]
        avg=avg/number_of_nodes(G)
        return avg

# Part 5: average shortest path length
# Here use dijkstra for all pairs shortest paths (don't know if Floyd-Marshall is better
# Alternatively, one can use average_shortest_path_length(G, [weight])

def avg_spl(G):
        length=all_pairs_dijkstra_path_length(G)
        total=0.0
        n=number_of_nodes(G)
        for sub in length.keys():
                for v in length[sub].values():
                        total=total+v
        total=total/(n*(n-1))
        return total

# Part 6: Assortativity
# Usage: double=degree_assortativity(G)

# Part 7: Giant Connected Component

def giant_CC(G):
        CC_list=connected_components(G)
        size=1
        for CC in CC_list:
                if size < len(CC):
                        size=len(CC)
        return size/number_of_nodes(G)


# Part 8: Densification power-law
# Usage: nodes= number_of_nodes(G)
#        print("number of nodes: %d" % number_of_nodes(G))
#        edges= number_of_edges(G)
#        print("number of edges: %d" % number_of_edges(G))
# OR USE  (need to ask about the diagram)
# double=density(G) (density=m/C(n,2)  m=number of edges, n=number of nodes)

# Part 9: Shrinking Diameter- use diameter(G)
# Usage: dia=diameter(G)
#       print("diameter: %d" % diameter(G))


