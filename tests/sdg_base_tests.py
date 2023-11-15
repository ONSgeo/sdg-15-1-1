import unittest
import pandas as pd
import geopandas as gpd

from src.SDG15_1_1 import SDG15_1_1
from user_params import UserParams


params: UserParams = UserParams()


class TestSDGBase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up class')
    
    def setUp(self) -> None:
        self._instance1: SDG15_1_1 = SDG15_1_1('', params.root_dir)
        
    def test_get_input_data_dir(self) -> None:
        print('running test_get_input_data_dir')
        self.assertIsNotNone(self._instance1.get_input_data_dir())
        self.assertIsInstance(self._instance1.get_input_data_dir(), str)
    
    def test_set_input_data_dir(self) -> None:
        print('running test_set_input_data_dir')
        self._instance1.set_input_data_dir(params.root_dir)
        self.assertEqual(self._instance1.get_input_data_dir(), params.root_dir)
                
    def test_get_output_data_dir(self) -> None:
        print('running test_get_output_data_dir')
        self.assertIsNotNone(self._instance1.get_output_data_dir())
        self.assertIsInstance(self._instance1.get_output_data_dir(), str)

    def test_set_output_data_dir(self) -> None:
        print('running test_set_output_data_dir')
        self._instance1.set_output_data_dir(params.root_dir)
        self.assertEqual(self._instance1.get_output_data_dir(), params.root_dir)
        
    def test_get_read_function(self) -> None:
        print('running test_get_read_function')
        self.assertIs(self._instance1._get_read_function('csv'), pd.read_csv)
        self.assertIs(self._instance1._get_read_function('xlsx'), pd.read_excel)
        self.assertIs(self._instance1._get_read_function('shp'), gpd.read_file)
        
        

        