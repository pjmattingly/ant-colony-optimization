import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntColonyGetDistance(unittest.TestCase):
	def test_correct(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			#def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _add_pheromone_value(self, route, pheromone_values): pass
			def _dissipate_pheromones(self): pass
			def mainloop(self): pass
		test_object = test_empty_object()
		
		#setup test environment
		def _init_matrix(size, value=None):
			"""
			setup a matrix NxN (where n = size)
			used in both self.distance_matrix and self.pheromone_map
			as they require identical matrixes besides which value to initialize to
			"""
			ret = []
			for row in range(size):
				ret.append([value for x in range(size)])
			return ret
		
		test_object.distance_matrix = _init_matrix(10)
		
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		test_object.nodes = {x:x for x in range(10)}
		
		#testing
		self.assertEqual(test_object._get_distance(0, 1), 1)
		self.assertEqual(test_object.distance_matrix[0][1], 1)
		
	def test_distance_callback_returns_other_than_int_or_float(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			#def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _add_pheromone_value(self, route, pheromone_values): pass
			def _dissipate_pheromones(self): pass
			def mainloop(self): pass
		test_object = test_empty_object()
		
		#setup test environment
		def _init_matrix(size, value=None):
			"""
			setup a matrix NxN (where n = size)
			used in both self.distance_matrix and self.pheromone_map
			as they require identical matrixes besides which value to initialize to
			"""
			ret = []
			for row in range(size):
				ret.append([value for x in range(size)])
			return ret
		
		test_object.distance_matrix = _init_matrix(10)
		
		def mock_distance_callback(start, end):
			return 'a'
		
		test_object.distance_callback = mock_distance_callback
		
		test_object.nodes = {x:x for x in range(10)}
		
		#testing
		#testing
		with self.assertRaisesRegexp(TypeError, 'distance_callback should return either int or float, saw: <type \'str\'>'):
			test_object._get_distance(0, 1)

if __name__ == '__main__':
    unittest.main()