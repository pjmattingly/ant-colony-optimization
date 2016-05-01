import unittest
import importlib

module = importlib.import_module('ant_colony')

debug = True

def _DEBUG(msg):
	if debug: print("[DEBUG]" + str(msg))
	
def _DEBUG_ARRAY(array):
	#transpose
	if debug:
		for row in list(zip(*array)):
			print(row)

#Class ANT testing below:

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
	
class TestAntUpdateDistanceTraveled(unittest.TestCase):
	def test_correct(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _update_distance_traveled correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _update_distance_traveled, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _pick_path(self): pass
			#def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#setting up object environment
		test_object.distance_traveled = 0
				
		#setup the distance callback to get a value for the distance between nodes
		def mock_distance_callback(start, end):
			return 1
		
		test_object.distance_callback = mock_distance_callback
		
		test_object._update_distance_traveled(0, 1)
		
		self.assertEqual(test_object.distance_traveled, 1)

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

class TestAntTraverse(unittest.TestCase):
	def test_correct(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			def run(self): pass
			#def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#setting up object environment
		test_object.location = 0	#starting at the 0th position
		
		self.called_update_route = False
		def mock_update_route(end):
			self.called_update_route = True
		
		test_object._update_route = mock_update_route
		
		self.called_update_distance_traveled = False
		def mock_update_distance_traveled(start, end):
			self.called_update_distance_traveled = True
			
		test_object._update_distance_traveled = mock_update_distance_traveled
		
		test_object._traverse(0, 1)
		
		#the ant moved from 0 to 1
		self.assertEqual(test_object.location, 1)
		self.assertTrue(self.called_update_route)
		self.assertTrue(self.called_update_distance_traveled)
		
		#cleanup
		del self.called_update_route
		del self.called_update_distance_traveled

class TestAntRun(unittest.TestCase):
	def test_correct(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		#inherit from ant so we can call _pick_path correctly
		class test_empty_object(module.ant_colony.ant):
			#override each method EXCEPT _pick_path, to get a clean testing environment
			def __init__(self): pass
			#def run(self): pass
			def _traverse(self): pass
			def _update_route(self): pass
			def _update_distance_traveled(self): pass
		test_object = test_empty_object()
		
		#setting up object environment
		test_object.location = 0
		test_object.route = []
		test_object.distance_traveled = 0
		test_object.possible_locations = [x for x in range(1)]
		
		def mock_pick_path():
			return test_object.possible_locations.pop()
		test_object._pick_path = mock_pick_path
		
		self.called_traverse = False
		def mock_traverse(*args):
			self.called_traverse = True
		test_object._traverse = mock_traverse
		
		test_object.run()
		
		self.assertEqual(test_object.possible_locations, [])
		self.assertTrue(self.called_traverse)
		
		#cleanup
		del self.called_traverse
	
class TestAntIntegrationTesting(unittest.TestCase):
	def test_first_run(self):
		module.debug = False
		
		#setup init environment
		
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
		
		def mock_distance_callback(start, end):
			return (2*end - start) ** 2	
			
		test_object = module.ant_colony.ant(init_location=0,
											possible_locations=[x for x in range(0, 10)],
											pheromone_map=_init_matrix(10, 0),
											distance_callback=mock_distance_callback,
											alpha=1,
											beta=1,
											first_pass=True)
		
		#before run() we need to override random.choice for predictable results
		
		self.test_next_choice = 1
		def mock_choice(*args):
			self.test_next_choice += 1
			return self.test_next_choice - 1
		
		import random
		random_choice_backup = random.choice
		random.choice = mock_choice
		
		test_object.run()
		route = test_object.get_route()
		distance = test_object.get_distance_traveled()
		#_DEBUG(route)
		#_DEBUG(distance)
		
		self.assertEqual(route, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(distance, 384)
		
		#cleanup
		random.choice = random_choice_backup
		del self.test_next_choice
		
	def test_nth_run_pheromones_are_one(self):
		module.debug = False
		#setup init environment
		
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
		
		def mock_distance_callback(start, end):
			return (2*end - start) ** 2
			
		test_object = module.ant_colony.ant(init_location=0,
											possible_locations=[x for x in range(0, 10)],
											pheromone_map=_init_matrix(10, 1),
											distance_callback=mock_distance_callback,
											alpha=1,
											beta=1,
											first_pass=False)
		
		#before run() we need to override random.random for predictable results
		def mock_random(*args):
			return .2
		
		import random
		random_random_backup = random.random
		random.random = mock_random
		
		test_object.run()
		route = test_object.get_route()
		distance = test_object.get_distance_traveled()
		# _DEBUG(route)
		# _DEBUG(distance)
		
		self.assertEqual(route, [0, 1, 2, 3, 4, 5, 9, 6, 8, 7])
		self.assertEqual(distance, 404)
		
		#cleanup
		random.random = random_random_backup
	
#Class ANT_COLONY testing:

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
		self.assertEqual(test_object.distance_matrix[1][0], 1)
		self.assertEqual(test_object.distance_matrix[0][1], 1)

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
		
class TestAntColonyInitAnts(unittest.TestCase):
	def test_correct_first_pass_is_False(self):
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
		test_object._init_ants()
		
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
		
class TestAntColonyMainLoop(unittest.TestCase):
	def test_correct(self):
		module.debug = False
		
		class test_empty_object(module.ant_colony):
			def __init__(self): pass
			def _get_distance(self, start, end): pass
			def _init_matrix(self, size, value=None): pass
			def _init_ants(self, start=0): pass
			def _update_pheromone_map(self): pass
			def _populate_ant_updated_pheromone_map(self, ant): pass
			#def mainloop(self): pass
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
			def run(self): pass
			def get_distance_traveled(self): pass
			def get_route(self): pass
		
		test_object.ants = [mock_ant()]
		self.called_populate_ant_updated_pheromone_map = False
		def mock_populate_ant_updated_pheromone_map(ant):
			self.called_populate_ant_updated_pheromone_map = True
			
		test_object._populate_ant_updated_pheromone_map = mock_populate_ant_updated_pheromone_map
		
		self.called_update_pheromone_map = False
		def mock_update_pheromone_map():
			self.called_update_pheromone_map = True
			
		test_object._update_pheromone_map = mock_update_pheromone_map
		
		test_object.iterations = 1
		
		test_object.first_pass = None
		test_object.nodes = dict()
		test_object.shortest_distance = None
		test_object.shortest_path_seen = None
		
		#testing
		test_object.mainloop()
		self.assertTrue(self.called_update_pheromone_map)
		self.assertTrue(self.called_populate_ant_updated_pheromone_map)
		
		#cleanup
		del self.called_update_pheromone_map
		del self.called_populate_ant_updated_pheromone_map

class TestAntColonyIntegrationTesting(unittest.TestCase):
	def test_short_run_two_ants_simple_distance(self):
		module.debug = False
		
		#setup
		testing_nodes = {
						0 : (1, 2),
						1 : (3, 8),
						2 : (6, 3),
						}
		
		def testing_distance_callback(start, end):
			return 1
		
		import random
		random_choice_backup = random.choice
		
		#force the ants to choose the path 0 -> 1 -> 2
		self.next = 0
		self.choice = [0, 1, 2, 1, 2]
		def mock_random_choice(*args):
			self.next += 1
			return self.choice[self.next]
			
		random.choice = mock_random_choice
		
		#testing
		test_object = module.ant_colony(testing_nodes, testing_distance_callback, ant_count=2)
		self.assertEqual([0, 1, 2], test_object.mainloop())
		
		#cleanup
		del self.next
		del self.choice
		random.choice = random_choice_backup
		
	def test_short_run_with_optimal_path(self):
		module.debug = False
		
		#setup
		testing_nodes = {
						0 : (0, 0),
						1 : (1, 1),
						2 : (2, 2),
						3 : (3, 3),
						}
		
		#we want to force the ant to follow the path 0 -> 1 -> 2 -> 3, as it should have the shortest distance of 3 (all other paths return a 3 distance)
		def testing_distance_callback(start, end):
			#_DEBUG("[testing_distance_callback()] START")
			# _DEBUG(start)
			# _DEBUG(end)
			if (start == (0, 0) and end == (1, 1)) or (start == (1, 1) and end == (0, 0)):
				# _DEBUG("[testing_distance_callback()] saw 0 -> 1")
				# _DEBUG("[testing_distance_callback()] END")
				return 1.0
			if (start == (1, 1) and end == (2, 2))or (start == (2, 2) and end == (1, 1)):
				# _DEBUG("[testing_distance_callback()] saw 1 -> 2")
				# _DEBUG("[testing_distance_callback()] END")
				return 1.0
			if (start == (2, 2) and end == (3, 3))or (start == (3, 3) and end == (2, 2)):
				# _DEBUG("[testing_distance_callback()] saw 2 -> 3")
				# _DEBUG("[testing_distance_callback()] END")
				return 1.0
			#_DEBUG("[testing_distance_callback()] END")
			return 3.0
		
		#testing
		test_object = module.ant_colony(testing_nodes, testing_distance_callback)
		self.assertEqual([0, 1, 2, 3], test_object.mainloop())
		
	def test_medium_run_with_optimal_path(self):
		module.debug = False
		
		#setup
		testing_nodes = {
						0 : (0, 0),
						1 : (1, 1),
						2 : (2, 2),
						3 : (3, 3),
						4 : (4, 4),
						5 : (5, 5),
						6 : (6, 6),
						}
		
		#path: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
		def testing_distance_callback(start, end):
			if (start == (0, 0) and end == (1, 1)) or (start == (1, 1) and end == (0, 0)):
				return 1.0
			if (start == (1, 1) and end == (2, 2))or (start == (2, 2) and end == (1, 1)):
				return 1.0
			if (start == (2, 2) and end == (3, 3))or (start == (3, 3) and end == (2, 2)):
				return 1.0
			if (start == (3, 3) and end == (4, 4))or (start == (4, 4) and end == (3, 3)):
				return 1.0
			if (start == (4, 4) and end == (5, 5))or (start == (5, 5) and end == (4, 4)):
				return 1.0
			if (start == (5, 5) and end == (6, 6))or (start == (6, 6) and end == (5, 5)):
				return 1.0
			return 3.0
		
		#testing
		test_object = module.ant_colony(testing_nodes, testing_distance_callback)
		#_DEBUG(test_object.mainloop())
		self.assertEqual([0, 1, 2, 3, 4, 5, 6], test_object.mainloop())
		
	def test_long_run_with_optimal_path(self):
		module.debug = False
		
		#setup
		testing_nodes = {
						0 : (0, 0),
						1 : (1, 1),
						2 : (2, 2),
						3 : (3, 3),
						4 : (4, 4),
						5 : (5, 5),
						6 : (6, 6),
						7 : (7, 7),
						8 : (8, 8),
						9 : (9, 9),
						}
		
		#path: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9
		def testing_distance_callback(start, end):
			if (start == (0, 0) and end == (1, 1)) or (start == (1, 1) and end == (0, 0)):
				return 2.0
			if (start == (1, 1) and end == (2, 2))or (start == (2, 2) and end == (1, 1)):
				return 1.0
			if (start == (2, 2) and end == (3, 3))or (start == (3, 3) and end == (2, 2)):
				return 2.0
			if (start == (3, 3) and end == (4, 4))or (start == (4, 4) and end == (3, 3)):
				return 1.0
			if (start == (4, 4) and end == (5, 5))or (start == (5, 5) and end == (4, 4)):
				return 2.0
			if (start == (5, 5) and end == (6, 6))or (start == (6, 6) and end == (5, 5)):
				return 1.0
			if (start == (6, 6) and end == (7, 7))or (start == (7, 7) and end == (6, 6)):
				return 2.0
			if (start == (7, 7) and end == (8, 8))or (start == (8, 8) and end == (7, 7)):
				return 1.0
			if (start == (8, 8) and end == (9, 9))or (start == (9, 9) and end == (8, 8)):
				return 1.0
			return 4.0
		
		#testing
		test_object = module.ant_colony(testing_nodes, testing_distance_callback)
		#_DEBUG(test_object.mainloop())
		self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], test_object.mainloop())
	
if __name__ == '__main__':
    unittest.main()