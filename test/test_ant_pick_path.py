import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntPickPath(unittest.TestCase):
	def test_is_first_pass(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#setting up object environment
		test_object.first_pass = True
		test_object.possible_locations = [x for x in range(10)]
		
		#mock random for the test
		import random
		def mock_choice(*args):
			return 1
		choice_backup = random.choice
		random.choice = mock_choice
		
		#on a first pass we just pick randomly from possible_locations
		self.assertEqual(test_object._pick_path(), 1)
		
		#restore choice
		random.choice = choice_backup
		
	def test_single_path_with_pheromone(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#since we're traversing between 0 and 1 for the test, setup a pheromone trail in pheromone_map
		test_object.pheromone_map[0][1] = 1
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#_DEBUG(test_object._pick_path())
		
		module.debug = False
		
		#all other paths are zero and all distances are equal, so we have to pick the one with pheromone
		self.assertEqual(test_object._pick_path(), 1)
	
	def test_multiple_paths_with_pheromones_low_probability_toss(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .2
			
		random_random_backup = random.random
		random.random = mock_random
		
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		module.debug = False
		self.assertEqual(test_object._pick_path(), 1)
		
		#restore random.random()
		random.random = random_random_backup
		
	def test_multiple_paths_with_pheromones_medium_probability_toss(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .4
			
		random_random_backup = random.random
		random.random = mock_random
		
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		module.debug = False
		self.assertEqual(test_object._pick_path(), 2)
		
		#restore random.random()
		random.random = random_random_backup

	def test_multiple_paths_with_pheromones_high_probability_toss(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .8
			
		random_random_backup = random.random
		random.random = mock_random
		
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		module.debug = False
		self.assertEqual(test_object._pick_path(), 2)
		
		#restore random.random()
		random.random = random_random_backup
	
	def test_ALL_paths_with_pheromones_low_probability_toss(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		test_object.pheromone_map[0][3] = 3
		test_object.pheromone_map[0][4] = 4
		test_object.pheromone_map[0][5] = 5
		test_object.pheromone_map[0][6] = 6
		test_object.pheromone_map[0][7] = 7
		test_object.pheromone_map[0][8] = 8
		test_object.pheromone_map[0][9] = 9
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .2
			
		random_random_backup = random.random
		random.random = mock_random
		
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		module.debug = False
		self.assertEqual(test_object._pick_path(), 4)
		
		#restore random.random()
		random.random = random_random_backup
		
	def test_ALL_paths_with_pheromones_medium_probability_toss(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		test_object.pheromone_map[0][3] = 3
		test_object.pheromone_map[0][4] = 4
		test_object.pheromone_map[0][5] = 5
		test_object.pheromone_map[0][6] = 6
		test_object.pheromone_map[0][7] = 7
		test_object.pheromone_map[0][8] = 8
		test_object.pheromone_map[0][9] = 9
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .5
			
		random_random_backup = random.random
		random.random = mock_random
		
		module.debug = False
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		
		self.assertEqual(test_object._pick_path(), 7)
		
		#restore random.random()
		random.random = random_random_backup
	
	def test_ALL_paths_with_pheromones_high_probability_toss(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		test_object.pheromone_map[0][3] = 3
		test_object.pheromone_map[0][4] = 4
		test_object.pheromone_map[0][5] = 5
		test_object.pheromone_map[0][6] = 6
		test_object.pheromone_map[0][7] = 7
		test_object.pheromone_map[0][8] = 8
		test_object.pheromone_map[0][9] = 9
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .9
			
		random_random_backup = random.random
		random.random = mock_random
		
		module.debug = False
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		
		self.assertEqual(test_object._pick_path(), 9)
		
		#restore random.random()
		random.random = random_random_backup
	
	def test_ALL_paths_with_pheromones_LOW_probability_toss_distance_varies(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _deposit_pheromone(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		test_object.pheromone_map[0][3] = 3
		test_object.pheromone_map[0][4] = 4
		test_object.pheromone_map[0][5] = 5
		test_object.pheromone_map[0][6] = 6
		test_object.pheromone_map[0][7] = 7
		test_object.pheromone_map[0][8] = 8
		test_object.pheromone_map[0][9] = 9
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return (2*end - start) ** 2
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .1
			
		random_random_backup = random.random
		random.random = mock_random
		
		module.debug = False
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		
		self.assertEqual(test_object._pick_path(), 1)
		
		#restore random.random()
		random.random = random_random_backup
	
	def test_ALL_paths_with_pheromones_MEDIUM_probability_toss_distance_varies(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		test_object.pheromone_map[0][3] = 3
		test_object.pheromone_map[0][4] = 4
		test_object.pheromone_map[0][5] = 5
		test_object.pheromone_map[0][6] = 6
		test_object.pheromone_map[0][7] = 7
		test_object.pheromone_map[0][8] = 8
		test_object.pheromone_map[0][9] = 9
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return (2*end - start) ** 2
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .5
			
		random_random_backup = random.random
		random.random = mock_random
		
		module.debug = False
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		
		self.assertEqual(test_object._pick_path(), 2)
		
		#restore random.random()
		random.random = random_random_backup
	
	def test_ALL_paths_with_pheromones_HIGH_probability_toss_distance_varies(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0)
		
		#setup pheromone trail between paths we want to choose from
		test_object.pheromone_map[0][1] = 1
		test_object.pheromone_map[0][2] = 2
		test_object.pheromone_map[0][3] = 3
		test_object.pheromone_map[0][4] = 4
		test_object.pheromone_map[0][5] = 5
		test_object.pheromone_map[0][6] = 6
		test_object.pheromone_map[0][7] = 7
		test_object.pheromone_map[0][8] = 8
		test_object.pheromone_map[0][9] = 9
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return (2*end - start) ** 2
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#_DEBUG_ARRAY(test_object.pheromone_map)
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .99
			
		random_random_backup = random.random
		random.random = mock_random
		
		module.debug = False
		#_DEBUG("picked path: " + str(test_object._pick_path()))
		
		self.assertEqual(test_object._pick_path(), 9)
		
		#restore random.random()
		random.random = random_random_backup
	
	def test_corner_case_of_attractiveness_of_all_paths_equal_zero(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		module.debug = True
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#borrowing _init_matrix() from the code for help with setup
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
		
		#setting up object environment
		test_object.first_pass = False
		test_object.location = 0	#starting at the 0th position
		test_object.possible_locations = [x for x in range(1, 10)]	#so we remove 0 from the list of possible locations for the next traversal
		
		#setup a pheromone map to use when picking the next path to choose
		#	doing the len(test_object.possible_locations)+1 in this case as in all instances the list of possible locations will be smaller than the pheromone map, as the ant is always initialized to a starting location and possible_locations is decrimented to reflect that (we can't traverse to our starting location)
		test_object.pheromone_map = _init_matrix(len(test_object.possible_locations)+1, value=0.0)
		#BUT keep all pheromone values at zero, to simulate the corner case of the attractiveness of each path being zero, as per the corner case
		
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return (2*end - start) ** 2
		
		test_object.distance_callback = mock_distance_callback
		
		#setup alpha and beta for "attractiveness" calculation, where alpha and beta are parameters
		test_object.alpha = 1
		test_object.beta = 1
		
		#mock random.random() for testing
		import random
		
		def mock_random():
			return .99
			
		random_random_backup = random.random
		random.random = mock_random
		
		#test_object._pick_path()
		self.assertEqual(test_object._pick_path(), 1)
		
		#restore random.random()
		random.random = random_random_backup
		
if __name__ == '__main__':
    unittest.main()