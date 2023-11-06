class UserParams:
    def __init__(self):
        # the root directory to work from
        self.root_dir = r'C:\Users\Cusse\Scripts\geo_work\sdg-15-1-1' 
        
        # the directory where the data is located
        # if none the class will assume it is in: f'{self._root_dir}/{self._sdg_name}_data'
        # e.g.  'C:/Users/name/Scripts/SDGs/sdg_15_1_1_data'
        self.data_dir = None
        
        # the directory where the output is saved
        # if none the class will assume it is in: f'{self._root_dir}/{self._sdg_name}_output'
        # e.g.  'C:/Users/name/Scripts/SDGs/sdg_15_1_1_output'
        self.output_dir = None
        
        # the starting year for multiple year exports
        self.year_start = 2017
        
        # the ending year for multiple year exports
        self.year_end = 2022