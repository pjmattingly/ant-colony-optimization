import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntColonyInitMatrix(unittest.TestCase):
	def test_correct(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			#def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _add_pheromone_value(self, route, pheromone_values): pass
			def _dissipate_pheromones(self): pass
			def mainloop(self): pass
		test_object = test_empty_object()
		
		self.assertEqual(test_object._init_matrix(1), [[0.0]])
		
if __name__ == '__main__':
    unittest.main()