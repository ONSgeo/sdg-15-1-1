from sdg_base.src.sdg_base_src.sdg_base import SDGBase
from user_params import UserParams

from typing import Dict, List, Optional
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 


class SDG15_1_1(SDGBase):
    """Defines input and output directories for data.
    
    Attributes (inherited)
    ----------
    root_dir
        The main directory in which data is stored.
    input_data_dir
        The main directory from which data is input.
    output_data_dir
        The main directory to which data is output.
    test_in_dir
        The main directory from which tests are drawn.
    test_out_dir
        The main directory to which tests are output.
    
    """ 
    
    def __init__(self, sdg_name: str, root_dir: Optional[str], data_dir: Optional[str] = None, output_dir: Optional[str] = None) -> None:
        """To retrieve input and save output data.
        
        Parameters
        ----------
        root_in_dir: str
            The main directory that the data is stored.
            For example: 'C:/Users/{user}/Scripts/geo_work/sdg_15_1_1/data'
        root_out_dir: Optional[str]
            This is for if the user wants to save the output elsewhere.
            If not the root out directory will be the same as the input directory.
            
        Returns
        -------
        None
        """

        self._sdg_name = 'sdg_15_1_1'
        super().__init__(self._sdg_name, root_dir, data_dir, output_dir)
        print(f"{self._sdg_name} Initialised")


    def _get_file_by_year(self, inp_list: List[str], year: int, n: int) -> Optional[List[str]]:
        """Retrieves files based on year of interest.
 
        Parameters
        ----------
        inp_list: List[str]
            The input files.
        year: int
            The year each file was published.
        n: int
            Expected number of files.
 
        Returns
        -------
        List: str
        """
        
        out_list: List[str] = [l for l in inp_list if str(year) in l]
        if len(out_list) != n:
            return None
        return out_list
        

    def get_lists_by_year(self) -> List[str]:
        """Creates list of files required for analysis matched by year. 
        
        Returns
        -------
            lists_by_year: List[str]
        """
        return self._lists_by_year
        
        
    def calculate_multiple_years(self, year_start: int, year_end: int, n: int = 1, save_shp_file: bool = False) -> bool:
        """Allows for the calulation of SDG for multiple years.
        
        Parameters
        ----------
        year_start: int
            Starting year.
        year_end: int
            Ending year.
            
        Returns
        -------
        bool
        """
        nfi_shps: List[str] = self.get_ext_files('gb_nfi', 'shp')
        sam_xlsx: List[str] = self.get_ext_files('*', 'xlsx', 'SAM_LAD')
        lad_shps: List[str] = self.get_ext_files('LADs', 'shp')
        
        file_lists: List[List[str]] = [lad_shps, sam_xlsx, nfi_shps]

        self._lists_by_year: Dict[str, List[str]] = {}

        for year in range(year_start, year_end+1):

            year_list: List[str] = []
            for file_list in file_lists:
                year_list.append(self._get_file_by_year(file_list, year, n))

            self._lists_by_year[year] = year_list
         
        for year in tqdm(self._lists_by_year.keys(), 'Calculating SDG'):
            # We're missing one of the data files
            # TODO add a logger that tells the user which one
            if None in self._lists_by_year[year]:
                continue

            lad_file_path: str = self._lists_by_year[year][0][0]
            sam_file_path: str = self._lists_by_year[year][1][0]
            nfi_file_path: str = self._lists_by_year[year][2][0]
            
            self.calculate_sdg(lad_file_path, sam_file_path, nfi_file_path, year, save_shp_file)
    
        return True

    
    def calculate_sdg(self, lad_file_path: Optional[str], sam_file_path: Optional[str], nfi_file_path: Optional[str], year: int, save_shp_file: bool = False) -> bool:
        """Calulates Sustainable Development Goal and plots result.
        
        Parameters
        ----------
        lad_file_path: str
            Location/directory of land boundary files.
        sam_file_path: str
            Location/directory of standard area measurements.
        nfi_file_path: str
            Location/directory of National Forest Inventory data.
        year: int
            The year for which data was published. 
        save_shape_file: bool
            Option to output save as .shp file. 
            
        Returns
        -------
        bool
        """
        important_col: str = f'lad{year-2000}cd'

        lad_gdf: gpd.GeoDataFrame = self.load_data(lad_file_path, index=important_col)
        sam_df: pd.DataFrame = self.load_data(sam_file_path)
        nfi_gdf: gpd.GeoDataFrame = self.load_data(nfi_file_path)

        woodland: gpd.GeoDataFrame = nfi_gdf[nfi_gdf['category'] == 'Woodland']
        shared_cols: List[str] = [col for col in lad_gdf.columns if col in sam_df.columns]
        lad_sam_gdf: gpd.GeoDataFrame = lad_gdf.merge(sam_df, on=shared_cols)

        lad_sam_woodland_gdf: gpd.GeoDataFrame = gpd.sjoin(lad_sam_gdf, woodland, how='left')

        lad_sam_woodland_gdf[f'pct_woodland_{year}'] = lad_sam_woodland_gdf['area_ha'] / lad_sam_woodland_gdf['arealhect'] * 100

        pct_groupby: gpd.GeoDataFrame = lad_sam_woodland_gdf.groupby(important_col)[[f'pct_woodland_{year}']].sum()
        self.save_data(pct_groupby, f'{year}_LAD_pct_woodland')

        lad_gdf[f'pct_woodland_{year}'] = pct_groupby

        lad_gdf.plot(column=f'pct_woodland_{year}', figsize=(20, 20),cmap='YlGn', legend=True)
        plt.title(f'Percentage of woodland by LAD for {year}')
        plt.savefig(f"{self._output_data_dir}/{year}_LAD_pct_woodland.jpeg")               
        self.save_data(pct_groupby, f'{year}_LAD_pct_woodland')
        
        if save_shp_file:
            self.save_data(lad_sam_woodland_gdf, f'{year}_LAD_pct_woodland')
        
        return True



def run_sdg15_1_1(params: UserParams) -> None:
    
    gfr: SDG15_1_1 = SDG15_1_1('', params.root_dir, params.data_dir, params.output_dir)
    
    if params.single_year_test and all([params.lad_file_path, params.sam_file_path, params.nfi_file_path, params.year_start]):
        print(f'Running single year export for year: {params.year_start}')
        gfr.calculate_sdg(params.lad_file_path, params.sam_file_path, params.nfi_file_path, params.year_start, save_shp_file=params.save_shp_file)

    if not params.single_year_test and all([params.year_start, params.year_end]):
        print(f'Running multi year export for years: {params.year_start}-{params.year_end}')
        gfr.calculate_multiple_years(params.year_start, params.year_end, save_shp_file=params.save_shp_file)

    else:
        print('Execution failed, please check necessary params:\n')
        params.print_params()