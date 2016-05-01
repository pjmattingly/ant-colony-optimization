import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntUpdateRoute(unittest.TestCase):
	def test_correct(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call method correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT target method, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			#def _update_route(self): pass
			def _pick_path(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#setting up object environment
		test_object.route = []
		test_object.possible_locations = [x for x in range(1, 10)]	#remove 0 from the list of possible locations for the next traversal
		
		module.debug = False
		
		test_object._update_route(1)	#traverse from current location to 1
		
		self.assertEqual(test_object.route, [1])
		self.assertEqual(test_object.possible_locations, [x for x in range(2, 10)])

if __name__ == '__main__':
    unittest.main()