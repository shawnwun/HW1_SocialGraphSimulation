import sys
import networkx as nx
import random
from networkx import *
import hw1_tools as tl
import evaluation as eva
import math

"""Edge linking probabilities"""
neighbor_prob = 0.8

def main (argv=None):
    #init with 50 random nodes
    """
    pl_graph = nx.Graph()
    for i in range(50):
	pl_graph.add_node(i)
    """
    #pl_graph = powerlaw_cluster_graph(100, 1, 0);
    pl_graph = empty_graph(50)

    """
    print tl.giant_CC(pl_graph)
    print tl.giant_CC(pl_graph)
    print number_of_edges(pl_graph)
    """

    #Read birth rate and death rate data from file
    birth_rate = readBirthRateData()
    death_rate = readDeathRateData()
    nodes_dict = {}

    #initialize Adam and Eve's start time
    for i in range(50):
	nodes_dict[i] = {'start':0,'age':0}

    iteration=0;
    killed=0
    borned=0
    
    while (pl_graph.number_of_nodes() > 0 and pl_graph.number_of_nodes() < 10000):    
        iteration += 1
        
        '''THE BORN STEP'''        
        #randomly choose number of nodes to add
        num_nodes = pl_graph.number_of_nodes()

	now_birth_rate = 0
	if num_nodes <=2500: # Baby Boom
	    now_birth_rate = birth_rate['boom']
	elif num_nodes <=5000: # Baby Boom
	    now_birth_rate = birth_rate['top']-float(birth_rate['top']-birth_rate['boom'])*(float(5000-num_nodes)/float(2500))
	elif num_nodes <=7500: # Baby Boom
	    now_birth_rate = birth_rate['trans']+float(birth_rate['top']-birth_rate['trans'])*(float(7500-num_nodes)/float(2500))
	else:		    # Aging
	    now_birth_rate = birth_rate['aging']+float(birth_rate['trans']-birth_rate['aging'])*(float(10000-num_nodes)/float(2500))

	#print birth_rate['boom'],birth_rate['top'],birth_rate['trans'],birth_rate['aging']
	#print now_birth_rate

        born_count = num_nodes * now_birth_rate

        #print born_count;
        pl_graph = powerlaw_cluster_graph(pl_graph.number_of_nodes() + born_count, 3, 0.8 , pl_graph);

        #go through the graph and see if every node has a "start" iter stored
        for n in pl_graph.nodes_iter():            
            if not (n in nodes_dict):
                nodes_dict[n] = {'start':iteration, 'age':0};
                borned+=1;
	    else:
		nodes_dict[n]['age']+=1
	
	#TODO:Add edge
	if(iteration%10==0 or pl_graph.number_of_nodes() >=10000 ):
	    num_edges = pl_graph.number_of_edges()
	    num_edges_to_reach = int( float(5) * float(num_nodes)/float(10000) * num_nodes )
	    print num_edges, num_edges_to_reach, num_nodes

	    all_degree = sum(list(pl_graph.degree().values()))
	    prob_cache = {}

	    cache_id = 1
	    for node in pl_graph.nodes_iter():
		for i in range(pl_graph.degree(node)):
		    prob_cache[cache_id] = node
		cache_id += 1
	    #print all_degree, len(prob_cache)

	    for i in range(num_edges,num_edges_to_reach): 
		randidx1 = int(random.uniform(0,1)*all_degree)
		randidx2 = 0
		if randidx1 <=0:
		    randidx1 = 1
		elif randidx1 > len(prob_cache):
		    randidx1 = len(prob_cache)
		node1 = prob_cache[randidx1]
		node2 = None
		prob = random.uniform(0,1)

		# Form the Triangle
		if prob <= neighbor_prob:
		    local_id = 1
		    local_cache = {}
		    for neighbor in pl_graph.neighbors(node1):
			for nei_neighbor in pl_graph.neighbors(neighbor):
			    if pl_graph.has_edge(node1,nei_neighbor):
				continue
			    else:
				for j in range(pl_graph.degree(nei_neighbor)):
				    local_cache[local_id] = nei_neighbor
				    local_id += 1
		    randidx2 = random.randrange(0,len(local_cache)) + 1
		    node2 = local_cache[randidx2]
		# Add edge according to degree
		else:
		    randidx2 = int(random.uniform(0,1)*all_degree)
		    if randidx2 <=0:
			randidx2 = 1 
		    elif randidx2 > len(prob_cache):
			randidx2 = len(prob_cache)
		    node2 = prob_cache[randidx2]
	    
		pl_graph.add_edge(node1,node2)
		prob_cache[cache_id] = node1
		prob_cache[cache_id+1] = node2
		all_degree += 2
		cache_id += 2
	    
        '''THE DEATH STEP'''
	# death rate follows the distribution
	for node in pl_graph.nodes_iter():
	    node_attr = nodes_dict[node];
	    my_death_rate = death_rate[node_attr['age']]
	    rand = random.uniform(0,1)
	    #print rand
	    if rand <= my_death_rate:
		node_attr['end'] = iteration
		del nodes_dict[node]
		nodes_dict[-node-1] = node_attr
		pl_graph.remove_node(node)
		killed +=1


        if (iteration%100) == 0:            
            print "iter: %d, borned: %d, killed: %d, total:%d" % (i, borned, killed, pl_graph.number_of_nodes());
            borned = 0;
            killed = 0;

	if(iteration%10==0):
	    eva.evaluation(pl_graph)
	    nx.write_adjlist(pl_graph,"../graph/pl_modified.adjlist.it"+str(iteration))
                
    print (pl_graph.number_of_edges());
    print (pl_graph.number_of_nodes());

    
    nx.write_adjlist(pl_graph,"../graph/pl_modified.adjlist")

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
