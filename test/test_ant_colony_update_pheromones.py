import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntColonyUpdatePheromones(unittest.TestCase):
	def test_empty_first_run_no_ants(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			#def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
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
			
		test_object.pheromone_map = _init_matrix(1, value=0)
		test_object.ant_updated_pheromone_map = _init_matrix(1, value=0)
		test_object.pheromone_evaporation_coefficient = .99
		test_object.first_pass = True
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		test_object._update_pheromone_map()
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#verify no changes took place, since this was a first pass
		self.assertEqual(test_object.pheromone_map, [[0]])
		
	def test_decay_no_ants(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			#def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
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
			
		test_object.pheromone_map = _init_matrix(2, value=1)
		test_object.ant_updated_pheromone_map = _init_matrix(2, value=0)
		test_object.pheromone_evaporation_coefficient = .99
		test_object.ants = []
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		test_object._update_pheromone_map()
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		self.assertTrue(test_object.pheromone_map[0][1] < 1)
		self.assertTrue(test_object.pheromone_map[1][0] < 1)
		self.assertTrue(test_object.pheromone_map[1][1] < 1)
		self.assertTrue(test_object.pheromone_map[0][0] < 1)
		
	def test_first_run_single_ant(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			#def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
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
				
		test_object.pheromone_map = _init_matrix(3, value=0)
		test_object.ant_updated_pheromone_map = _init_matrix(3, value=.5)
		test_object.pheromone_evaporation_coefficient = .99
		test_object.pheromone_constant = 1
		test_object.ants = [mock_ant()]
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		test_object._update_pheromone_map()
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#testing
		self.assertEqual(test_object.pheromone_map[0][1], .5)
		self.assertEqual(test_object.pheromone_map[1][0], .5)
		self.assertEqual(test_object.pheromone_map[1][2], .5)
		self.assertEqual(test_object.pheromone_map[2][1], .5)
	
	def test_single_ant(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			#def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
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
				
		test_object.pheromone_map = _init_matrix(3, value=1)
		test_object.ant_updated_pheromone_map = _init_matrix(3, value=.5)
		test_object.pheromone_evaporation_coefficient = .99
		test_object.pheromone_constant = 1
		test_object.ants = [mock_ant()]
		test_object.first_pass = False
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		test_object._update_pheromone_map()
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#testing
		self.assertEqual(test_object.pheromone_map[0][1], .51)
		self.assertEqual(test_object.pheromone_map[1][2], .51)

	def test_first_run_two_ants(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			#def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
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
				
		test_object.pheromone_map = _init_matrix(4, value=0)
		test_object.ant_updated_pheromone_map = _init_matrix(4, value=0)
		
		#ant1, traverse: 0 -> 1 -> 2 -> 3, distance == 2
		test_object.ant_updated_pheromone_map[0][1] = .5
		test_object.ant_updated_pheromone_map[1][0] = .5
		test_object.ant_updated_pheromone_map[1][2] = .5
		test_object.ant_updated_pheromone_map[2][1] = .5
		test_object.ant_updated_pheromone_map[2][3] = .5
		test_object.ant_updated_pheromone_map[3][2] = .5
		
		#ant2, traverse: 3 -> 0 -> 2 -> 1, distance == 3
		test_object.ant_updated_pheromone_map[3][0] = 1.0/3.0
		test_object.ant_updated_pheromone_map[0][3] = 1.0/3.0
		test_object.ant_updated_pheromone_map[0][2] = 1.0/3.0
		test_object.ant_updated_pheromone_map[2][0] = 1.0/3.0
		test_object.ant_updated_pheromone_map[2][1] += 1.0/3.0	#as this is traversed twice, once by each ant
		test_object.ant_updated_pheromone_map[1][2] += 1.0/3.0
		
		test_object.pheromone_evaporation_coefficient = .99
		test_object.pheromone_constant = 1
		ant1 = mock_ant([0, 1, 2, 3], 2)
		ant2 = mock_ant([3, 0, 2, 1], 3)
		
		test_object.ants = [ant1, ant2]
		
		test_object.first_pass = True
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		test_object._update_pheromone_map()
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#testing
		
		# #ant 1
		self.assertEqual(test_object.pheromone_map[0][1], .5)
		
		#this is updated TWICE, once by each ant and is higher than the others as two sets of pheromone track are laid down (after the decay step)
		#	due to rounding errors we use this "squeeze" method to issolate its value
		#	(true value should be 5/6 [1/2 + 1/3, from ant1 and ant2 respectively])
		self.assertTrue(test_object.pheromone_map[1][2] < .9 and test_object.pheromone_map[1][2] >= (.83))
		self.assertEqual(test_object.pheromone_map[2][3], .5)
		
		#ant2
		self.assertEqual(test_object.pheromone_map[3][0], (1.0/3.0))
		self.assertEqual(test_object.pheromone_map[0][2], (1.0/3.0))
		self.assertTrue(test_object.pheromone_map[2][1] < .9 and test_object.pheromone_map[2][1] >= (.83))
	
	def test_two_ants(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, count, start=0): pass
			#def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
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
				
		test_object.pheromone_map = _init_matrix(4, value=1)
		test_object.ant_updated_pheromone_map = _init_matrix(4, value=0)
		
		#ant1, traverse: 0 -> 1 -> 2 -> 3, distance == 2
		test_object.ant_updated_pheromone_map[0][1] = .5
		test_object.ant_updated_pheromone_map[1][0] = .5
		test_object.ant_updated_pheromone_map[1][2] = .5
		test_object.ant_updated_pheromone_map[2][1] = .5
		test_object.ant_updated_pheromone_map[2][3] = .5
		test_object.ant_updated_pheromone_map[3][2] = .5
		
		#ant2, traverse: 3 -> 0 -> 2 -> 1, distance == 3
		test_object.ant_updated_pheromone_map[3][0] = 1.0/3.0
		test_object.ant_updated_pheromone_map[0][3] = 1.0/3.0
		test_object.ant_updated_pheromone_map[0][2] = 1.0/3.0
		test_object.ant_updated_pheromone_map[2][0] = 1.0/3.0
		test_object.ant_updated_pheromone_map[2][1] += 1.0/3.0	#as this is traversed twice, once by each ant
		test_object.ant_updated_pheromone_map[1][2] += 1.0/3.0
		
		test_object.pheromone_evaporation_coefficient = .99
		test_object.pheromone_constant = 1
		ant1 = mock_ant([0, 1, 2, 3], 2)
		ant2 = mock_ant([3, 0, 2, 1], 3)
		
		test_object.ants = [ant1, ant2]
		
		test_object.first_pass = True
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		test_object._update_pheromone_map()
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#testing
		#	where we see ~1% larger values than the previous test
		#	since each value was decayed from 1 (with .99 pheromone_evaporation_coefficient) and then each ant contribution added
		#ant 1
		self.assertEqual(test_object.pheromone_map[0][1], .51)
		
		self.assertTrue(test_object.pheromone_map[1][2] < .9 and test_object.pheromone_map[1][2] >= (.83 + .01))
		self.assertEqual(test_object.pheromone_map[2][3], .51)
		
		#ant2
		self.assertEqual(test_object.pheromone_map[3][0], (1.0/3.0) + .01)
		self.assertEqual(test_object.pheromone_map[0][2], (1.0/3.0) + .01)
		self.assertTrue(test_object.pheromone_map[2][1] < .9 and test_object.pheromone_map[2][1] >= (.83 + .01))

if __name__ == '__main__':
    unittest.main()