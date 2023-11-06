import unittest
from sdg_15_1_1.src.SDG15_1_1.sdg_base import SDGBase
from sdg_15_1_1.user_params import UserParams


class TestSDGBase(unittest.TestCase):
    
    def set_up(self):
        self.sdg_base = SDGBase('', )
        