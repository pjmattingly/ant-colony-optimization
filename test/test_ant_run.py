import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

class TestAntRun(unittest.TestCase):
	def test_correct(self):
		#Note: can't do this in setup because of python2's wonky OOP, doing it in the test instead
		
		class test_empty_object(module.ant_colony.ant):
			def __init__(self):
				from threading import Thread
				Thread.__init__(self)
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

if __name__ == '__main__':
    unittest.main()