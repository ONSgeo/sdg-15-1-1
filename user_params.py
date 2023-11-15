import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class UserParams:
    def __init__(self) -> None:
        # the root directory to work from
        self.root_dir: Optional[str] = os.getenv('ROOT_DIR')
        
        # the directory where the data is located
        # if none the class will assume it is in: f'{self._root_dir}/{self._sdg_name}_data'
        # e.g.  'C:/Users/name/Scripts/SDGs/sdg_15_1_1_data'
        self.data_dir: Optional[str] = None
        
        # the directory where the output is saved
        # if none the class will assume it is in: f'{self._root_dir}/{self._sdg_name}_output'
        # e.g.  'C:/Users/name/Scripts/SDGs/sdg_15_1_1_output'
        self.output_dir: Optional[str] = None
        
        # the starting year for multiple year exports
        # the ONLY year for single year exports
        self.year_start: int = 2017
        
        # the ending year for multiple year exports
        self.year_end: int = 2022
        
        # if only testing a single year
        # Note this requires all the file paths below to be populated
        self.single_year_test: bool = False
        
        # The specific path to the LAD file for the single year
        self.lad_file_path: Optional[str] = None
        
        # The specific path to the SAM file for the single year
        self.sam_file_path: Optional[str] = None
        
        # The specific path to the NFI file for the single year
        self.nfi_file_path: Optional[str] = None
        
        
    def print_params(self) -> None:
        for k, v in vars(self).items():
            print(f'{k} = {v}')