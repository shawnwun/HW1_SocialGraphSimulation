import sys;
import networkx as nx;
#import matplotlib.pyplot as plt;

def main (argv=None):
    #start with 2 connected nodes, Adam and Eve?
    graph = nx.generators.random_graphs.barabasi_albert_graph(2,1);
    
    for i in range(1, 10000):
        graph = nx.generators.random_graphs.barabasi_albert_graph(
            len(graph.nodes())+1, 2, graph);

        if (i%100) == 0:
            print (i);

        '''print (graph.nodes());
        print (graph.edges());
        print ("xxxxxxxxxx");'''
    
    '''nx.draw(graph);
    nx.draw_random(graph);
    nx.draw_circular(graph);
    nx.draw_spectral(graph);
    plt.show();'''
    print (len(graph.edges()));
    print (len(graph.nodes()));

    nx.write_adjlist(graph,"ba.adjlist")

    

if __name__ == "__main__":
    sys.exit(main());
