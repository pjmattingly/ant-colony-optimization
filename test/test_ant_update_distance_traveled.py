import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

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

if __name__ == '__main__':
    unittest.main()