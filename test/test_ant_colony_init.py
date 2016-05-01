import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntColonyInit(unittest.TestCase):
	def test_correct(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): pass
		
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#do this as _init_nodes in __init__ is expected to return two values, an iterable, giving the weird error: NoneType is not iterable		
		def test_init_nodes(self, nodes):
			return 1, 2
		
		test_empty_object._init_nodes = test_init_nodes
		
		def test_init_ants(self, start=0):
			return True
		
		test_empty_object._init_ants = test_init_ants
		
		test_object = test_empty_object(testing_nodes, test_distance_callback)
		
		#testing
		self.assertEqual(test_object.start, 0)
		self.assertEqual(test_object.id_to_key, 1)
		self.assertEqual(test_object.nodes, 2)
		self.assertTrue(test_object.ants)
		
	def test_start_set_correct(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): pass
		
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#borrowing actual init nodes for this test
		def test_init_nodes(self, nodes):
			"""
			create a mapping of internal id numbers (0 .. n) to the keys in the nodes passed 
			create a mapping of the id's to the values of nodes
			we use id_to_key to return the route in the node names the caller expects in mainloop()
			"""
			id_to_key = dict()
			id_to_values = dict()
			
			id = 0
			for key in sorted(nodes.keys()):
				id_to_key[id] = key
				id_to_values[id] = nodes[key]
				id += 1
				
			return id_to_key, id_to_values
		
		test_empty_object._init_nodes = test_init_nodes
		
		def test_init_ants(self, start=0):
			return True
		
		test_empty_object._init_ants = test_init_ants
		
		test_object = test_empty_object(testing_nodes, test_distance_callback, start='a')
		
		#testing
		# import debug
		# debug.DEBUG(test_object.start)
		
		self.assertEqual(test_object.start, 1)
		
	def test_start_set_value_not_found(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): pass
		
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#borrowing actual init nodes for this test
		def test_init_nodes(self, nodes):
			"""
			create a mapping of internal id numbers (0 .. n) to the keys in the nodes passed 
			create a mapping of the id's to the values of nodes
			we use id_to_key to return the route in the node names the caller expects in mainloop()
			"""
			id_to_key = dict()
			id_to_values = dict()
			
			id = 0
			for key in sorted(nodes.keys()):
				id_to_key[id] = key
				id_to_values[id] = nodes[key]
				id += 1
				
			return id_to_key, id_to_values
		
		test_empty_object._init_nodes = test_init_nodes
		
		def test_init_ants(self, start=0):
			return True
		
		test_empty_object._init_ants = test_init_ants
		
		with self.assertRaisesRegexp(KeyError, 'not found in the nodes dict passed'):
			test_empty_object(testing_nodes, test_distance_callback, start='b')
	
	#invalid parameter testing
	
	def test_ant_colony_ant_count_too_small(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): pass
		
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#borrowing actual init nodes for this test
		def test_init_nodes(self, nodes):
			"""
			create a mapping of internal id numbers (0 .. n) to the keys in the nodes passed 
			create a mapping of the id's to the values of nodes
			we use id_to_key to return the route in the node names the caller expects in mainloop()
			"""
			id_to_key = dict()
			id_to_values = dict()
			
			id = 0
			for key in sorted(nodes.keys()):
				id_to_key[id] = key
				id_to_values[id] = nodes[key]
				id += 1
				
			return id_to_key, id_to_values
		
		test_empty_object._init_nodes = test_init_nodes
		
		def test_init_ants(self, start=0):
			return True
		
		test_empty_object._init_ants = test_init_ants
		
		with self.assertRaisesRegexp(ValueError, 'ant_count must be >= 1'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, ant_count=0)
		
	def test_ant_colony_ant_count_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): pass
		
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#borrowing actual init nodes for this test
		def test_init_nodes(self, nodes):
			"""
			create a mapping of internal id numbers (0 .. n) to the keys in the nodes passed 
			create a mapping of the id's to the values of nodes
			we use id_to_key to return the route in the node names the caller expects in mainloop()
			"""
			id_to_key = dict()
			id_to_values = dict()
			
			id = 0
			for key in sorted(nodes.keys()):
				id_to_key[id] = key
				id_to_values[id] = nodes[key]
				id += 1
				
			return id_to_key, id_to_values
		
		test_empty_object._init_nodes = test_init_nodes
		
		def test_init_ants(self, start=0):
			return True
		
		test_empty_object._init_ants = test_init_ants
		
		with self.assertRaisesRegexp(TypeError, 'ant_count must be int'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, ant_count=None)
	
	def test_ant_colony_alpha_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'alpha must be int or float'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, alpha='a')
	
	def test_ant_colony_alpha_too_small(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(ValueError, 'alpha must be >= 0'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, alpha=-1)
			
	def test_ant_colony_beta_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'beta must be int or float'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, beta='a')
			
	def test_ant_colony_beta_too_small(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(ValueError, 'beta must be >= 1'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, beta=0)
			
	def test_pheromone_evaporation_coefficient_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'pheromone_evaporation_coefficient must be int or float'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, pheromone_evaporation_coefficient='a')
			
	def test_pheromone_constant_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'pheromone_constant must be int or float'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, pheromone_constant='a')
			
	def test_pheromone_iterations_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'iterations must be int'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, iterations='a')
			
	def test_pheromone_iterations_too_small(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = {
						'a' : (1, 1),
						15 : (0, 0),
						'beaver' : (2, 2),
						'yes we can' : (3, 3),
						}
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(ValueError, 'iterations must be >= 0'):
			test_object = test_empty_object(testing_nodes, test_distance_callback, iterations=-1)
			
	def test_pheromone_nodes_too_small(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = dict()
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(ValueError, 'there must be at least one node in dict nodes'):
			test_object = test_empty_object(testing_nodes, test_distance_callback)
			
	def test_pheromone_nodes_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = []
						
		def test_distance_callback(self):
			pass
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'nodes must be dict'):
			test_object = test_empty_object(testing_nodes, test_distance_callback)
	
	def test_pheromone_nodes_invalid_type(self):
		module.debug = False
		
		#setup
		class test_empty_object(module.ant_colony):
			#def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			def mainloop(self): pass
			def _init_nodes(self, nodes): return 1, 2
			
		testing_nodes = testing_nodes = {
										'a' : (1, 1),
										15 : (0, 0),
										'beaver' : (2, 2),
										'yes we can' : (3, 3),
										}
						
		test_distance_callback = 0
		
		#testing
		with self.assertRaisesRegexp(TypeError, 'distance_callback is not callable, should be method'):
			test_object = test_empty_object(testing_nodes, test_distance_callback)
if __name__ == '__main__':
    unittest.main()