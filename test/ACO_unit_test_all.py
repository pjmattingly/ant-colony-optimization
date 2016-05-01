import unittest
import importlib

#import tests from files

#testing class Ant:
from test_ant_pick_path import *
from test_ant_update_distance_traveled import *
from test_ant_update_route import *
from test_ant_traverse import *
from test_ant_run import *
from test_ant_integration_testing import *

#testing for class Ant_Colony
from test_ant_colony_get_distance import *
from test_ant_colony_init_matrix import *
from test_ant_colony_init_ants import *
from test_ant_colony_populate_ant_updated_pheromone_map import *
from test_ant_colony_update_pheromones import *
from test_ant_colony_main_loop import *
from test_ant_colony_integration_testing import *
from test_ant_colony_more_general import *
from test_ant_colony_init_nodes import *
from test_ant_colony_init import *
	
if __name__ == '__main__':
    unittest.main()