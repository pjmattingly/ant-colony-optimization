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
	
	#codeEval sample data
	
	def test_code_eval_6_node(self):
		module.debug = False
					
		mapping = {
			0: (37.7768016, -122.4169151),
			1: (37.7860105, -122.4025377),
			2: (37.7821494, -122.4058960),
			3: (37.7689269, -122.4029053),
			4: (37.7768800, -122.3911496),
			5: (37.7706628, -122.4040139),
			}
		
		#testing
		test_object = module.ant_colony(mapping, distance_on_earth)
		#_DEBUG(test_object.mainloop())
		
		#code eval is 1 indexed, rather than 0, so add 1 to each value of the nodes passed back as the solution route
		solution = [(x+1) for x in test_object.mainloop()]
		#_DEBUG(solution)
		test_solution = [1, 3, 2, 5, 6, 4]
		self.assertEqual(test_solution, solution)
	
	def test_code_eval_10_node(self):
		mapping = {
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
		test_solution = [1, 6, 4, 8, 5, 3, 2, 7, 9, 10]
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = [(x+1) for x in test_object.mainloop()]
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
	
	#randomly generated data tests	
	def test_random_walk_1(self):
		mapping = {
				0 : (54.22763857131542, -100.62179306195173),
				1 : (73.53241835133572, -134.60844140643013),
				2 : (67.1841362158277, 49.97583689322559),
				3 : (-80.54009171727866, 57.282928570742165),
				4 : (84.99694847951791, -35.73977682352875),
				5 : (-68.4328382265224, -166.8079139888821),
				6 : (23.18660289102572, -111.77664481303432),
				7 : (-10.924596797226432, 6.246815481610602),
				8 : (75.34549712202669, -173.65929656966114),
				9 : (38.106379566058195, 87.6467277772618),
				}
		
		test_solution = [0, 6, 1, 8, 4, 2, 9, 7, 3, 5]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_2(self):
		mapping = {
			0 : (48.486781575030754, 65.24572487477447),
			1 : (-10.924864636156366, 87.97440869665179),
			2 : (63.403920043554955, -109.99874671435192),
			3 : (62.68822623141686, 21.24978336451562),
			4 : (86.52941104285614, 86.04503895514738),
			5 : (-82.53870602186487, 118.41414834264168),
			6 : (76.55733265395274, 132.68498122479392),
			7 : (-31.935901921881868, 160.71077334968686),
			8 : (59.42799999464727, -152.67420700671315),
			9 : (-81.14404553349029, 1.4803534037391102),
			}
		
		test_solution = [0, 3, 4, 2, 8, 6, 1, 7, 5, 9]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_3(self):
		mapping = {
			0 : (-32.7326634925997, -47.72614424184368),
			1 : (-43.01930989376043, 153.89594889398518),
			2 : (7.000707341214649, 99.93659002811677),
			3 : (-88.1960246073015, 9.097561629178955),
			4 : (-56.73285468611557, -147.35757169149065),
			5 : (-73.74948794283755, -78.25379817863156),
			6 : (0.9590546145812878, -161.1312571626125),
			7 : (26.54842474994664, -170.0058461727865),
			8 : (-24.984667641668132, 24.88773935416983),
			9 : (-47.639053465357634, 135.1975349603193),
			}
		
		test_solution = [0, 8, 2, 9, 1, 3, 5, 4, 6, 7]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
	
	def test_random_walk_4(self):
		mapping = {
			0: (-25.185341057764525, 6.843032336902314),
			1: (-59.747015334437215, -118.8074359235144),
			2: (-43.09554705792462, -68.0620020064857),
			3: (18.925216280013682, -16.557277363048527),
			4: (-20.59638938161909, 3.9391747092741247),
			5: (25.97286759954766, -68.79810165816949),
			6: (-30.28039950153856, 66.36145832654688),
			7: (-89.54087124232564, 155.79948034087846),
			8: (52.82734644419715, 45.45429752771343),
			9: (60.55234228654541, -124.81006280074178),
			}
		
		test_solution = [0, 4, 3, 8, 9, 5, 2, 1, 7, 6]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_5(self):
		mapping = {
			0 : (58.79509191656448, -178.55910838419044),
			1 : (16.486614610506862, -7.824694553357868),
			2 : (77.29514529480903, -105.32691203118401),
			3 : (53.34503186035435, 163.7007623147488),
			4 : (74.64366415510749, 177.08460921905697),
			5 : (-49.86627467811143, -82.35258299815835),
			6 : (-80.74653906601546, -19.554583037954366),
			7 : (-46.75691652975595, 66.91469490996121),
			8 : (-13.013162241064592, 169.56596818473466),
			9 : (68.24823093934518, 124.29622179399145),
			}
		
		test_solution = [0, 3, 9, 4, 2, 1, 5, 6, 7, 8]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_6(self):
		mapping = {
			0 : (-34.59053182135558, 66.28297501656762),
			1 : (69.36407785201745, -128.94982804266715),
			2 : (79.25324509240515, -139.58385632846998),
			3 : (54.12475065041613, 119.22033652453591),
			4 : (30.50257372566862, 112.56838685588858),
			5 : (-22.31337164715937, 53.781182473602186),
			6 : (-39.95851974968314, -56.35487198079979),
			7 : (-5.587454640480278, -105.05921307203073),
			8 : (25.759068952030823, -172.12900795946007),
			9 : (-68.66495585502365, -23.922134872650343),
			}
			
		test_solution = [0, 5, 9, 6, 7, 8, 1, 2, 3, 4]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_7(self):
		mapping = {
			0 : (-64.4036193622249, -29.714150050876313),
			1 : (-32.29057872675603, -98.76436965027347),
			2 : (6.465281166285687, -172.63028715334517),
			3 : (24.219652221932492, -132.07652687636286),
			4 : (-12.152639126645916, -48.16420512951025),
			5 : (54.63717498039018, -139.64644642904918),
			6 : (-82.59741117912702, 8.142344621286389),
			7 : (21.00555612983331, -141.4427192954134),
			8 : (-53.43381230866389, 175.08223889533545),
			9 : (-50.36504066561444, 161.8517059176784),
			}
		
		test_solution = [0, 6, 8, 9, 2, 5, 3, 7, 1, 4]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_8(self):
		mapping = {
			0 : (-25.1273564907845, 122.18872152786386),
			1 : (-74.35875169435528, 23.760381417489448),
			2 : (20.344316823911857, 101.78689326182749),
			3 : (-43.31100390730476, 159.84101792604747),
			4 : (-49.9158463951583, 60.68699096060512),
			5 : (35.427523300147605, 46.728501276412686),
			6 : (-1.6091835553446918, 61.93883608165216),
			7 : (14.94622535605768, 32.885314465697306),
			8 : (50.45531280472794, 135.59204635184474),
			9 : (48.60323678260074, 87.77991745110764),
			}
		test_solution = [0, 3, 1, 4, 6, 7, 5, 9, 2, 8]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)
		
	def test_random_walk_9(self):
		mapping = {
			0 : (50.813500398787454, -26.91658793347944),
			1 : (-13.833214991421519, -42.92176074044568),
			2 : (-2.738424133981322, 7.648819123155802),
			3 : (-8.226760542049261, -29.243456059138563),
			4 : (-4.294406186286353, -51.71515372708465),
			5 : (-62.28362920525646, 151.14751940141375),
			6 : (81.63674381459145, -139.7868870096079),
			7 : (69.88421258463741, 61.704377694656486),
			8 : (31.692641875994116, 174.02332532827222),
			9 : (24.759893320781764, -3.2911354279767724),
			}
		
		test_solution = [0, 4, 1, 3, 2, 9, 7, 6, 8, 5]
		
		test_object = module.ant_colony(mapping, distance_on_earth)
		solution = test_object.mainloop()
		#_DEBUG(solution)
		self.assertEqual(test_solution, solution)

if __name__ == '__main__':
    unittest.main()