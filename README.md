# ant-colony-optimization
Implementation of the Ant Colony Optimization algorithm (python)

#Usage:
	import ant_colony
			
	//given some nodes, and some locations...
	test_nodes = {0: (0, 7), 1: (3, 9), 2: (12, 4), 3: (14, 11), 4: (8, 11)
		5: (15, 6), 6: (6, 15), 7: (15, 9), 8: (12, 10), 9: (10, 7)}
	
	//...and a function to get distance between nodes...
	def distance(start, end):
		x_distance = abs(start[0] - end[0])
		y_distance = abs(start[1] - end[1])
		
		//c = sqrt(a^2 + b^2)
		import math
		return math.sqrt(pow(x_distance, 2) + pow(y_distance, 2))
	
	//...we can make a colony of ants...
	colony = ant_colony(test_nodes, distance)
	
	//...that will find the optimal solution with ACO
	answer = colony.mainloop()

#Discussion:

Ant Colony Optimization is intended to solve combinatoric optimization problems 
(like the Traveling Salesman Problem, or the Knapsack Problem). Simply feed the constructor a dict mapping your node names to
coordinates of those nodes and give it a distance function call back that can take the coordinates and it will solve it using
the ACO algorithm as described.

An effort has been made to initialize the algorithm's variables (alpha, beta, Q, etc) to sensible defaults. But your TSP problem
may differ significantly from the testing set (see test directory) and may perform more poorly than optimal.

The latest release is multithreaded.

A full description of the behavior of the algorithm can be found here: https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms#Example_pseudo-code_and_formula

Note: Tests that implement finding actual optimal paths may fail occasionally, as this algorithm is semi-random. The default configuration should make this a rare occurance.
