import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntColonyInitAnts(unittest.TestCase):
	def test_correct_first_pass_is_False(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			#def _init_ants(self, start): pass
			def _add_pheromone_value(self, route, pheromone_values): pass
			def _dissipate_pheromones(self): pass
			def mainloop(self): pass
		test_object = test_empty_object()
		
		#setup test environment
		class mock_ant:
			def __init__(self, *args):
				self.ant_init_called = True
			
		ant_backup = test_object.ant
		test_object.ants = [mock_ant()]
		test_object.first_pass = False
		test_object.nodes = dict()
		test_object.pheromone_map = []
		test_object.alpha = 0
		test_object.beta = 0
		
		#testing
		test_object._init_ants(start=0)
		
		self.assertTrue(test_object.ants[0].ant_init_called)
		
	def test_correct_first_pass_is_True(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			#def _init_ants(self, count, start=0): pass
			def _add_pheromone_value(self, route, pheromone_values): pass
			def _dissipate_pheromones(self): pass
			def mainloop(self): pass
		test_object = test_empty_object()
		
		#setup test environment
		class mock_ant:
			def __init__(self, init_location, possible_locations, pheromone_map, distance_callback, alpha, beta, first_pass=False):
				self.first_pass = first_pass
				
			def is_mock_ant(self):
				return True
			
		ant_backup = test_object.ant
		test_object.ant = mock_ant
		test_object.ant_count = 1
		test_object.first_pass = True
		test_object.nodes = dict()
		test_object.pheromone_map = []
		test_object.alpha = 0
		test_object.beta = 0
		
		#testing
		#this messes up on assertEqual() as they're not the same object, but the same type of object
		#so just verify that it created a mock_ant object in both cases (we get back a list, thus the indexing)
		self.assertTrue(test_object._init_ants(1)[0].is_mock_ant())
		self.assertTrue(test_object._init_ants(1)[0].first_pass)
		
		#cleanup
		test_object.ant = ant_backup

if __name__ == '__main__':
    unittest.main()