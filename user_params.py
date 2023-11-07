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
        # the ONLY year for single year exports
        self.year_start = 2017
        
        # the ending year for multiple year exports
        self.year_end = 2022
        
        # if only testing a single year
        # Note this requires all the file paths below to be populated
        self.single_year_test = False
        
        # The specific path to the LAD file for the single year
        self.lad_file_path = None
        
        # The specific path to the SAM file for the single year
        self.sam_file_path = None
        
        # The specific path to the NFI file for the single year
        self.nfi_file_path = None
        
        
    def print_params(self):
        for k, v in vars(self).items():
            print(f'{k} = {v}')