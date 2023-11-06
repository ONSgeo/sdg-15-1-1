from typing import List, Optional, Union 
from collections.abc import Callable
from abc import ABC, abstractmethod
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
from tqdm import tqdm


class SDGBase(ABC):   
    """
    
    Attributes
    ----------
    _root_dir : str
        Main directory in which data is stored. 
    _sdg_name : str
        The specific SDG eg 'sdg_15_1_1'
    """
    
   
    def __init__(self, sdg_name: str, root_dir: str, data_dir: Optional[str] = None, output_dir: Optional[str] = None) -> None:
        """Defines input and output directories for data

        Parameters
        ----------
        root_in_dir: str
            The main directory in which data is stored
        root_out_dir: Optional[str]
            This is for if the user wants to save the output elsewhere
            If not the root out directory will be the same as the input directory

        Returns
        -------
        None
        """
        
        self._root_dir = root_dir
        self._sdg_name = sdg_name
        
        self.set_file_tree(data_dir, output_dir)
        
        
    def set_input_data_dir(self, root_in_dir: str) -> None:
        """Sets directory and creates folders from which data is input 

        Parameters
        ----------
        root_in_dir: str
            The main directory in which data is stored 

        Returns
        -------
        None
        """
        
        self._input_data_dir = root_in_dir
        self.create_folders(self._input_data_dir)

        
    def get_input_data_dir(self) -> str:
        """returns main directory in which data is stored.

        Returns
        -------
        str
        """
        return self._input_data_dir

    
    def set_output_data_dir(self, root_out_dir: str) -> None:
        """sets directory and creates folders for data outputs

        Parameters
        ----------
        root_out_dir: str
            The directory in which outputs are stored

        Returns
        -------
        None
        """
        
        self._output_data_dir = f'{root_out_dir}/'
        self.create_folders(self._output_dir)


    def get_output_data_dir(self) -> str:
        """Returns directory in which outputs are stored

        Returns
        -------
        str
        """
        
        return self._output_data_dir

    
    def set_file_tree(self, input_data_dir: Optional[str] = None, output_data_dir: Optional[str] = None) -> None:
        
        if input_data_dir is None:
            self._input_data_dir = f'{self._root_dir}/{self._sdg_name}_data'
        else:
            self._input_data_dir = input_data_dir
            
        if output_data_dir is None:
            self._output_data_dir = f'{self._root_dir}/{self._sdg_name}_output'
        else:
            self._output_data_dir = output_data_dir
            
        self._test_in_dir = f'{self._root_dir}/tests_data/{self._sdg_name}_data'
        self._test_out_dir = f'{self._root_dir}/tests_data/{self._sdg_name}_output'

        file_tree = [self._input_data_dir, self._output_data_dir, self._test_in_dir, self._test_out_dir]
        
        for branch in file_tree:
            self.create_folders(branch)

            
    def create_folders(self, new_dir: str) -> None:
        """Creates folders to store output data

        Parameters
        ----------
        new_dir: str
            Directory in which to store output data
  
        Returns
        -------
        None
        
        Raises
        -------
            Catches any error in making the file
        """
        
        try:
            os.makedirs(new_dir, exist_ok=True)
            print(f'Directory {new_dir} was created or already existed')
        except Exception as e:
            print(f'Unable to make directory {new_dir} because of error {e}')
        
        
    def get_ext_files(self, inp_folder: str, ext: str, search_string: Optional[str] = None) -> List[str]:
        """Retrieves input files

        Parameters
        ----------
        inp_folder: str
            Folder containing input data of interest
        ext: str
            The extension being searched for
        search_string: Optional[str]
            Searches for keyword(s) within folder of interest
            
        Returns
        -------
        list[str]
        """
        all_files = glob.glob(f'{self.get_input_data_dir()}/{inp_folder}/*.{ext}')
        if search_string:
            all_files = [f for f in all_files if search_string in f]
        return all_files
    
    
    def _get_read_function(self, ext: str) -> Callable:
        """Returns the relevent read method based on the
           input extension

        Parameters
        ----------
        ext: str
            The extension being searched for
            
        Returns
        -------
        Callable
        """
        data_read_dict = {
            'csv' : pd.read_csv,
            'shp' : gpd.read_file,
            'xlsx': pd.read_excel,
        }    
        return data_read_dict[ext]
    
    
    def load_data(self, file_path: str, cols: List[str] = None, index: str = None, epsg: int = 27700) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """Joins and loads data of interest as a data frame

        Parameters
        ----------
        file_path: str
            Location of files of interest
        cols: List[str]
            Columnn of interest
        index: str
            Row of interest?
        espg: int
            ESPG code of coordinate reference system used in files of interest

        Returns
        -------
        File: Union[pd.DataFrame, gpd.GeoDataFrame]
        """
        ext = file_path.split('.')[-1]
        read_func = self._get_read_function(ext)
        df = read_func(file_path)
        df.columns = df.columns.str.lower()
        if cols:
            df = df[cols]
        if index:
            df = df.set_index(index)
        if isinstance(df, gpd.GeoDataFrame) and not df.crs.to_epsg() == epsg:
            df = df.to_crs(epsg)
            df = df.set_geometry(df['geometry'])

        return df   

    
    def save_data(self, file: Union[pd.DataFrame, gpd.GeoDataFrame], file_name: str) -> bool:
        """Saves data as .csv or .shp, dependent on dataframe

        Parameters
        ----------
        file: Union[pd.DataFrame, gpd.DataFrame]
            Data of interest
        file_name: str
            Name of file containing output data of interest.

        Returns
        -------
        bool
        """
        if isinstance(file, pd.DataFrame):
            file.to_csv(f'{self.get_output_data_dir()}/{file_name}.csv')
        if isinstance(file, gpd.GeoDataFrame):
            file.to_file(f'{self.get_output_data_dir()}/{file_name}.shp')
        return True
    
    
    @abstractmethod
    def calculate_sdg(self):
        pass
    