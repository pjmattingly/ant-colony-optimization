import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

#	W:\Programming Workspace\ACO\ACO more general
#	testing of a more general implementation of ACO
class TestAntColonyMoreGeneral(unittest.TestCase):
	def test_generalized_node_names(self):
		module.debug = False
		
		#setup
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
		
		#we want to force the ant to follow the path 0 (a) -> 1 (15) -> 2 (beaver) -> 3 (yes we can)
		#	as it should have the shortest distance of 3 (all other paths return a 3 distance)
		def testing_distance_callback(start, end):
			if (start == (0, 0) and end == (1, 1)) or (start == (1, 1) and end == (0, 0)):
				return 1.0
			if (start == (1, 1) and end == (2, 2))or (start == (2, 2) and end == (1, 1)):
				return 1.0
			if (start == (2, 2) and end == (3, 3))or (start == (3, 3) and end == (2, 2)):
				return 1.0
			return 3.0
		
		#testing
		test_object = module.ant_colony(testing_nodes, testing_distance_callback)
		self.assertEqual([15, 'a', 'beaver', 'yes we can'], test_object.mainloop())
		
if __name__ == '__main__':
    unittest.main()