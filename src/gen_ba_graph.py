import sys;
import networkx as nx;
import random;
from networkx import *;

def main (argv=None):
    #start with 2 connected nodes, Adam and Eve?
    ba_graph = barabasi_albert_graph(2,1);

    #initialize Adam and Eve's start time
    nodes_dict = {0:{'start':0}, 1:{'start':0}};

    i=0;
    killed=0;
    borned=0;
    
    #for i in range(1, 5):
    while (i < 1000 and ba_graph.number_of_nodes() > 0 and ba_graph.number_of_nodes() < 10000):    
        i+=1;
        
        '''THE BORN STEP'''        
        #randomly choose number of nodes to add
        num_nodes = ba_graph.number_of_nodes();
        born_count = random.randint(1, getBornRate(num_nodes));

        #print born_count;

        ba_graph = barabasi_albert_graph(
            ba_graph.number_of_nodes() + born_count, 2, ba_graph);

        #go through the graph and see if every node has a "start" iter stored
        for n in ba_graph.nodes_iter():            
            if not (n in nodes_dict):
                nodes_dict[n] = {'start': i};
                borned+=1;


        '''THE DEATH STEP'''
        #The death god randomly select a number. That's the amount of people
        #   he will check whether he should kill or not, including infants
        randNum = (ba_graph.number_of_nodes()-2)/10;
        if (randNum < 1):
            randNum = 1;
        
        num_to_check = random.randint(1, randNum);

        for j in range(1, num_to_check):
            #randomly choose a node index
            node = random.randint(0, ba_graph.number_of_nodes());

            if node in ba_graph:
                node_attr = nodes_dict[node];
                deathRate = getDeathRate(node_attr['start'], i);
                rand = random.random();
                
                if (random.random() < deathRate):
                    #print "DeathRate: %f, rand: %f, kill %d" % (deathRate, rand, node);
                    node_attr = nodes_dict[node];
                    node_attr['end'] = i;
                    del nodes_dict[node];
                    nodes_dict[-node-1] = node_attr;

                    ba_graph.remove_node(node);
                    killed+=1;
        
        if (i%100) == 0:            
            print "iter: %d, borned: %d, killed: %d, total:%d" % (i, borned, killed, ba_graph.number_of_nodes());
            borned = 0;
            killed = 0;


                
    print (ba_graph.number_of_edges());
    print (ba_graph.number_of_nodes());

    LifeTimeHistogram = {};

    for node, attr in nodes_dict.iteritems():        
        if node < 0:
            age = attr['end'] - attr['start'];
        #else:
        #    age = i - attr['start'];

            if age in LifeTimeHistogram:
                LifeTimeHistogram[age] = LifeTimeHistogram[age] + 1;
            else:
                LifeTimeHistogram[age] = 1;

    #print "life time";
    #plotHistogram(LifeTimeHistogram);
    


    ageDistHistogram = {};

    for node, attr in nodes_dict.iteritems():
        if node >= 0:
            age = i - attr['start'];

            if age in ageDistHistogram:
                ageDistHistogram[age] = ageDistHistogram[age] + 1;
            else:
                ageDistHistogram[age] = 1;

    #print "age dist";
    #plotHistogram(ageDistHistogram);

    
def plotHistogram(histogram):
    maxAge = 0;
    for age, count in histogram.iteritems():        
        if age > maxAge:
            maxAge = age;

    for i in range (0, maxAge+1):    
        if i in histogram:
            sys.stdout.write("%d," % histogram[i]);            
        else:
            sys.stdout.write("0,");
        sys.stdout.flush();
    print "";
    
def getDeathRate(startTime, currentTime):
    return 1 - 1/((currentTime-startTime+1.0/100.0));

def getBornRate(nodeCount):
    rate = nodeCount/10;
    if (rate < 1):
        rate = 1;

    return rate;

if __name__ == "__main__":
    sys.exit(main());
