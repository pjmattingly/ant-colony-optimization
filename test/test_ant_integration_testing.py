import unittest
import importlib

#source: http://stackoverflow.com/a/11158224/5343977
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import ant_colony as module

#give distance between two GPS locations
def distance_on_earth(start, end):
	"""
	Gives distance between two points.
	start and end are assumed to be in decimal representation of latitude and longitude
	each lat / long pair are assumed to be in standard lat / long order
	sources: http://www.movable-type.co.uk/scripts/latlong.html
		http://www.codecodex.com/wiki/Calculate_Distance_Between_Two_Points_on_a_Globe#Python
		(modified the above code, from non-standard input ordering [long / lat])
	Example: distance((37.7689269, -122.4029053), (37.7768800, -122.3911496))
	Return: 1.36002518696 km
	(example lat / long pairs are, respectively: airbnb and dropbox headquarters in SF CA)
	"""
	import math

	def recalculate_coordinate(val,  _as=None):  
		""" 
		Accepts a coordinate as a tuple (degree, minutes, seconds) 
		You can give only one of them (e.g. only minutes as a floating point number) and it will be duly 
		recalculated into degrees, minutes and seconds. 
		Return value can be specified as 'deg', 'min' or 'sec'; default return value is a proper coordinate tuple. 
		"""  
		deg,  min,  sec = val  
		# pass outstanding values from right to left  
		min = (min or 0) + int(sec) / 60  
		sec = sec % 60  
		deg = (deg or 0) + int(min) / 60  
		min = min % 60  
		# pass decimal part from left to right  
		dfrac,  dint = math.modf(deg)  
		min = min + dfrac * 60  
		deg = dint  
		mfrac,  mint = math.modf(min)  
		sec = sec + mfrac * 60  
		min = mint  
		if _as:  
			sec = sec + min * 60 + deg * 3600
			if _as == 'sec': return sec
			if _as == 'min': return sec / 60
			if _as == 'deg': return sec / 3600
		return deg,  min,  sec

	def points2distance(start,  end):  
		""" 
		Calculate distance (in kilometers) between two points given as (long, latt) pairs 
		based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula). 
		Implementation inspired by JavaScript implementation from http://www.movable-type.co.uk/scripts/latlong.html 
		Accepts coordinates as tuples (deg, min, sec), but coordinates can be given in any form - e.g. 
		can specify only minutes: 
		(0, 3133.9333, 0)  
		is interpreted as  
		(52.0, 13.0, 55.998000000008687) 
		which, not accidentally, is the lattitude of Warsaw, Poland. 
		"""  
		start_long = math.radians(recalculate_coordinate(start[1],  'deg'))  
		start_latt = math.radians(recalculate_coordinate(start[0],  'deg'))  
		end_long = math.radians(recalculate_coordinate(end[1],  'deg'))  
		end_latt = math.radians(recalculate_coordinate(end[0],  'deg'))
		d_latt = end_latt - start_latt  
		d_long = end_long - start_long  
		a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2  
		c = 2 * math.asin(math.sqrt(a))
		return 6371 * c
	
	def decdeg2dms(dd):
		"""
		Source: http://stackoverflow.com/a/12737895/5343977
		"""
		negative = dd < 0
		dd = abs(dd)
		minutes,seconds = divmod(dd*3600,60)
		degrees,minutes = divmod(minutes,60)
		if negative:
			if degrees > 0:
				degrees = -degrees
			elif minutes > 0:
				minutes = -minutes
			else:
				seconds = -seconds
		return (degrees,minutes,seconds)
	
	#converting to degrees / minutes / seconds representation, as points2distance() requires it
	start_dms = (decdeg2dms(start[0]), decdeg2dms(start[1]))
	end_dms = (decdeg2dms(end[0]), decdeg2dms(end[1]))
	return float(points2distance(start_dms, end_dms))

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
		
	def test_live_data(self):
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
			
		self.test_nodes = {
							0: (37.7768016, -122.4169151),
							1: (37.7860105, -122.4025377),
							2: (37.7821494, -122.4058960),
							3: (37.7689269, -122.4029053),
							4: (37.7768800, -122.3911496),
							5: (37.7706628, -122.4040139),
							6: (37.7870361, -122.4039444),
							7: (37.7507903, -122.3877184),
							8: (37.7914417, -122.3927229),
							9: (37.8672841, -122.5010216)
							}
							
		self.test_distance_matrix = _init_matrix(10)
		
		#borrowing for distance callback
		def _get_distance(start, end):
			"""
			uses the distance_callback to return the distance between nodes
			note that distances are assumed to be symmetric
			e.g. that distance_matrix[0][1] == distance_matrix[1][0]
			if a distance has not been calculated before, then it is populated in distance_matrix and returned
			if a distance has been called before, then its value is returned from distance_matrix
			"""
			if not self.test_distance_matrix[start][end]:
				distance = distance_on_earth(self.test_nodes[start], self.test_nodes[end])
				self.test_distance_matrix[start][end] = distance
				self.test_distance_matrix[end][start] = distance
				#_DEBUG_ARRAY(self.distance_matrix)
				return distance
			return self.test_distance_matrix[start][end]
			
		test_object = module.ant_colony.ant(init_location=0,
											possible_locations=self.test_nodes.keys(),
											pheromone_map=_init_matrix(10, 1),
											distance_callback=_get_distance,
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
		
		self.assertEqual(route, [0, 2, 1, 5, 3, 9, 8, 4, 6, 7])
		
		#cleanup
		random.random = random_random_backup
		del self.test_distance_matrix
		del self.test_nodes
	
if __name__ == '__main__':
    unittest.main()