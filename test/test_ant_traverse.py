import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

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

if __name__ == '__main__':
    unittest.main()