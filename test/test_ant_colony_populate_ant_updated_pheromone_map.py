import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntColonyPopulateAntUpdatedPheromoneMap(unittest.TestCase):
	def test_first_run_single_ant(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _update_pheromones(self, ant): pass
			#def _populate_ant_updated_pheromone_map(self, ant): pass
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
			
		class mock_ant:
			def get_route(self):
				return [0, 1, 2]
			def get_distance_traveled(self):
				return float(2)
				
		test_object.ant_updated_pheromone_map = _init_matrix(3, value=0)
		test_object.pheromone_constant = 1
		
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		test_object._populate_ant_updated_pheromone_map(mock_ant())
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		
		#testing
		self.assertEqual(test_object.ant_updated_pheromone_map[0][1], .5)
		self.assertEqual(test_object.ant_updated_pheromone_map[1][0], .5)
		self.assertEqual(test_object.ant_updated_pheromone_map[1][2], .5)
		self.assertEqual(test_object.ant_updated_pheromone_map[2][1], .5)
		
	def test_single_ant(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _update_pheromones(self, ant): pass
			#def _populate_ant_updated_pheromone_map(self, ant): pass
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
			
		class mock_ant:
			def get_route(self):
				return [0, 1, 2]
			def get_distance_traveled(self):
				return float(2)
				
		test_object.ant_updated_pheromone_map = _init_matrix(3, value=1)
		test_object.pheromone_constant = 1
		
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		test_object._populate_ant_updated_pheromone_map(mock_ant())
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		
		#testing
		self.assertEqual(test_object.ant_updated_pheromone_map[0][1], 1.5)
		self.assertEqual(test_object.ant_updated_pheromone_map[1][0], 1.5)
		self.assertEqual(test_object.ant_updated_pheromone_map[1][2], 1.5)
		self.assertEqual(test_object.ant_updated_pheromone_map[2][1], 1.5)
	
	def test_first_run_two_ants(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _update_pheromones(self, ant): pass
			#def _populate_ant_updated_pheromone_map(self, ant): pass
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
			
		class mock_ant:
			def __init__(self, route, distance):
				self.route = route
				self.distance = distance
				
			def get_route(self):
				return self.route
			
			def get_distance_traveled(self):
				return float(self.distance)
				
		test_object.ant_updated_pheromone_map = _init_matrix(4, value=0)
		test_object.pheromone_constant = 1
		ant1 = mock_ant([0, 1, 2, 3], 2)
		ant2 = mock_ant([3, 0, 2, 1], 3)
		
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		test_object._populate_ant_updated_pheromone_map(ant1)
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		test_object._populate_ant_updated_pheromone_map(ant2)
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		
		#testing
		#ant1
		self.assertEqual(test_object.ant_updated_pheromone_map[0][1], 1.0/2.0)
		#this is updated TWICE, once by each ant and is higher than the others as two sets of pheromone track are laid down (after the decay step)
		#	due to rounding errors we use this "squeeze" method to issolate its value
		#	(true value should be 5/6 [1/2 + 1/3, from ant1 and ant2 respectively])
		self.assertTrue(test_object.ant_updated_pheromone_map[1][2] < .9 and test_object.ant_updated_pheromone_map[1][2] >= (.83))
		self.assertEqual(test_object.ant_updated_pheromone_map[2][3], 1.0/2.0)
		
		#ant2
		self.assertEqual(test_object.ant_updated_pheromone_map[3][0], 1.0/3.0)
		self.assertEqual(test_object.ant_updated_pheromone_map[0][2], 1.0/3.0)
		self.assertTrue(test_object.ant_updated_pheromone_map[2][1] < .9 and test_object.ant_updated_pheromone_map[1][2] >= (.83))
		
	def test_two_ants(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			def _update_pheromones(self, ant): pass
			#def _populate_ant_updated_pheromone_map(self, ant): pass
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
			
		class mock_ant:
			def __init__(self, route, distance):
				self.route = route
				self.distance = distance
				
			def get_route(self):
				return self.route
			
			def get_distance_traveled(self):
				return float(self.distance)
				
		test_object.ant_updated_pheromone_map = _init_matrix(4, value=1)
		test_object.pheromone_constant = 1
		ant1 = mock_ant([0, 1, 2, 3], 2)
		ant2 = mock_ant([3, 0, 2, 1], 3)
		
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		test_object._populate_ant_updated_pheromone_map(ant1)
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		test_object._populate_ant_updated_pheromone_map(ant2)
		#_DEBUG_ARRAY(test_object.ant_updated_pheromone_map)
		
		#testing
		#ant1
		self.assertEqual(test_object.ant_updated_pheromone_map[0][1], 1.0/2.0 + 1)
		self.assertTrue(test_object.ant_updated_pheromone_map[1][2] < 1.9 and test_object.ant_updated_pheromone_map[1][2] >= (1.83))
		self.assertEqual(test_object.ant_updated_pheromone_map[2][3], 1.0/2.0 + 1)
		
		#ant2
		self.assertEqual(test_object.ant_updated_pheromone_map[3][0], 1.0/3.0 + 1)
		self.assertEqual(test_object.ant_updated_pheromone_map[0][2], 1.0/3.0 + 1)
		self.assertTrue(test_object.ant_updated_pheromone_map[2][1] < 1.9 and test_object.ant_updated_pheromone_map[1][2] >= (1.83))

if __name__ == '__main__':
    unittest.main()