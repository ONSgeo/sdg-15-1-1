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
    root_in_dir : str
        Main directory in which data is stored. 
    output_dir : str
        Description of `attr2`.
    """
    
    def __init__(self, root_in_dir: str, root_out_dir: Optional[str] = None) -> None:
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
        self.set_root_in_dir(root_in_dir)
        
        if root_out_dir is not None:
            self.set_output_dir(root_out_dir)
        else:
            self.set_output_dir(root_in_dir)          

        
    def set_root_in_dir(self, root_in_dir: str) -> None:
        """Sets directory and creates folders from which data is input 

        Parameters
        ----------
        root_in_dir: str
            The main directory in which data is stored 

        Returns
        -------
        None
        """
        self._root_in_dir = root_in_dir
        self.create_folders(self._root_in_dir)

        
    def get_root_in_dir(self) -> str:
        """returns main directory in which data is stored.

        Returns
        -------
        str
        """
        return self._root_in_dir

    
    def set_output_dir(self, root_out_dir: str) -> None:
        """sets directory and creates folders for data outputs

        Parameters
        ----------
        root_out_dir: str
            The directory in which outputs are stored

        Returns
        -------
        None
        """
        self._output_dir = f'{root_out_dir}/'
        self.create_folders(self._output_dir)

        
    def get_output_dir(self) -> str:
        """Returns directory in which outputs are stored

        Returns
        -------
        str
        """
        return self._output_dir

    
    def create_folders(self, new_dir: str) -> bool:
        """Creates folders to store output data

        Parameters
        ----------
        new_dir: str
            Directory in which to store output data
  
        Returns
        -------
        bool
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
            Files containing input data of interest?
        search_string: Optional[str]
             Searches for keyword(s) within folder of interest
            
        Returns
        -------
        list[str]
        """
        all_files = glob.glob(f'{self.get_root_in_dir()}/{inp_folder}/*.{ext}')
        if search_string:
            all_files = [f for f in all_files if search_string in f]
        return all_files
    
    
    def _get_read_function(self, ext: str) -> Callable:
        """Reads input files based on file type. 

        Parameters
        ----------
        ext: str
            Files containing data of interest
            
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
        """Saves data as .csv or .shp, dependent on data frame

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
            file.to_csv(f'{self.get_output_dir()}{file_name}.csv')
        if isinstance(file, gpd.GeoDataFrame):
            file.to_file(f'{self.get_output_dir()}{file_name}.shp')
        return True
    
    
    @abstractmethod
    def calculate_sdg(self):
        pass
    