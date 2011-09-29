import sys;
import networkx as nx;
import random;
from networkx import *;

def main (argv=None):
    #init with 50 random nodes
    pl_graph = powerlaw_cluster_graph(50, 5, 0.4)

    #Read birth rate and death rate data from file
    birth_rate = readBirthRateData()
    death_rate = readDeathRateData()
    nodes_dict = {}

    #initialize Adam and Eve's start time
    for i in range(50):
	nodes_dict[i] = {'start':0,'age':0}

    i=0;
    killed=0;
    borned=0;
    
    while (pl_graph.number_of_nodes() > 0 and pl_graph.number_of_nodes() < 10000):    
        i+=1;
        
        '''THE BORN STEP'''        
        #randomly choose number of nodes to add
        num_nodes = pl_graph.number_of_nodes();

	now_birth_rate = 0
	if num_nodes <=2500: # Baby Boom
	    now_birth_rate = birth_rate['boom']
	elif num_nodes <=5000: # Baby Boom
	    now_birth_rate = birth_rate['top']-(birth_rate['top']-birth_rate['boom'])*((5000-num_nodes)/2500)
	elif num_nodes <=7500: # Baby Boom
	    now_birth_rate = birth_rate['trans']+(birth_rate['top']-birth_rate['trans'])*((7500-num_nodes)/2500)
	else:		    # Aging
	    now_birth_rate = birth_rate['aging']+(birth_rate['trans']-birth_rate['aging'])*((10000-num_nodes)/2500)


        born_count = num_nodes * now_birth_rate

        #print born_count;

        pl_graph = powerlaw_cluster_graph(pl_graph.number_of_nodes() + born_count, 5, 0.4 , pl_graph);

        #go through the graph and see if every node has a "start" iter stored
        for n in pl_graph.nodes_iter():            
            if not (n in nodes_dict):
                nodes_dict[n] = {'start':i, 'age':0};
                borned+=1;
	    else:
		nodes_dict[n]['age']+=1


        '''THE DEATH STEP'''
	#
	for node in pl_graph.nodes_iter():
	    node_attr = nodes_dict[node];
	    my_death_rate = death_rate[node_attr['age']]
	    rand = random.uniform(0,1)
	    #print rand
	    if rand <= my_death_rate:
		node_attr['end'] = i
		del nodes_dict[node]
		nodes_dict[-node-1] = node_attr;
		pl_graph.remove_node(node)
		killed +=1


        if (i%100) == 0:            
            print "iter: %d, borned: %d, killed: %d, total:%d" % (i, borned, killed, pl_graph.number_of_nodes());
            borned = 0;
            killed = 0;


                
    print (pl_graph.number_of_edges());
    print (pl_graph.number_of_nodes());

    
    nx.write_adjlist(pl_graph,"../graph/pl.adjlist")

    LifeTimeHistogram = {};

    nol = 0.0
    for node, attr in nodes_dict.iteritems():        
        if node < 0:
            age = attr['age'];
	    if(attr['end']<100):
		continue
	    nol += 1.0
            if age in LifeTimeHistogram:
                LifeTimeHistogram[age] = LifeTimeHistogram[age] + 1.0;
            else:
                LifeTimeHistogram[age] = 1.0;
    
    for key in LifeTimeHistogram.keys():
	LifeTimeHistogram[key] = float(LifeTimeHistogram[key])/float(nol)   

    print LifeTimeHistogram 
    print "life time";
    for key, value in LifeTimeHistogram.iteritems():
	print value, '	',
    #plotHistogram(LifeTimeHistogram);
    print '\n'


    ageDistHistogram = {};

    nol = 0.0
    for node, attr in nodes_dict.iteritems():
        if node >= 0:
            age = attr['age'];
	    nol +=1.0
            if age in ageDistHistogram:
                ageDistHistogram[age] = ageDistHistogram[age] + 1.0;
            else:
                ageDistHistogram[age] = 1.0;

    for key in ageDistHistogram.keys(): 
	ageDistHistogram[key] = float(ageDistHistogram[key])/float(nol)   
 
    print "age dist";
    for key, value in ageDistHistogram.iteritems():
	print value, '	',
    ##plotHistogram(ageDistHistogram);

    
def plotHistogram(histogram):
    maxAge = 0;
    for age, count in histogram.iteritems():        
        if age > maxAge:
            maxAge = age;

    for i in range (0, maxAge+1):    
        if i in histogram.keys():
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


def readDeathRateData():
    f = file('../data/death.rate','r')
    age = 0
    death_rate = {}
    while True:
	line = f.readline()
	if(line==''):
	    break
	rate = float(line)
	death_rate[age] = rate
	age +=1
    return death_rate


def readBirthRateData():
    f = file('../data/birth.rate','r')
    rate1 = float(f.readline().split(' ')[1])
    rate2 = float(f.readline().split(' ')[1])
    rate3 = float(f.readline().split(' ')[1])
    rate4 = float(f.readline().split(' ')[1])
    birth_rate = {'boom':rate1,'top':rate2,'trans':rate3,'aging':rate4}
    return birth_rate
 
if __name__ == "__main__":
    sys.exit(main());
