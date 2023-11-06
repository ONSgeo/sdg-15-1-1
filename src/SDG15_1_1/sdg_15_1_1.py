from sdg_15_1_1.src.SDG15_1_1.sdg_base import SDGBase
from typing import List, Optional
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 


class SDG15_1_1(SDGBase):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes
    ----------
    attr1 : str
        Description of `attr1`.
    attr2 : :obj:`int`, optional
        Description of `attr2`.

    """
    
    def __init__(self, root_in_dir: str, root_out_dir: Optional[str] = None) -> None:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        self._sdg_name = 'sdg_15_1_1'
        self._output_dir = f'{root_out_dir}{self._sdg_name}_output'
        super().__init__(root_in_dir, self._output_dir)

        
    def _get_file_by_year(self, inp_list: List[str], year: int, n: int) -> List[str]:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        out_list = [l for l in inp_list if str(year) in l]
        if len(out_list) != n:
            return None
        return out_list
        

    def get_lists_by_year(self):
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        return self._lists_by_year
        
        
    def calculate_multiple_years(self, year_start: int, year_end: int, n: int = 1) -> bool:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        nfi_shps = self.get_ext_files('gb_nfi', 'shp')
        sam_xlsx = self.get_ext_files('*', 'xlsx', 'SAM_LAD')
        lad_shps = self.get_ext_files('LADs', 'shp')
        
        file_lists = [lad_shps, sam_xlsx, nfi_shps]

        self._lists_by_year = {}

        for year in range(year_start, year_end+1):

            year_list = []
            for file_list in file_lists:
                year_list.append(self._get_file_by_year(file_list, year, n))

            self._lists_by_year[year] = year_list
         
        for year in tqdm(self._lists_by_year.keys(), 'Calculating SDG'):
            # We're missing one of the data files
            # TODO add a logger that tells the user which one
            if None in self._lists_by_year[year]:
                continue

            lad_file_path = self._lists_by_year[year][0][0]
            sam_file_path = self._lists_by_year[year][1][0]
            nfi_file_path = self._lists_by_year[year][2][0]
            
            self.calculate_sdg(lad_file_path, sam_file_path, nfi_file_path, year)
    
        return True

    
    def calculate_sdg(self, lad_file_path: str, sam_file_path: str, nfi_file_path: str, year: int, save_shp_file: bool = False) -> bool:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        important_col = f'lad{year-2000}cd'

        lad_gdf = self.load_data(lad_file_path, index=important_col)
        sam_df = self.load_data(sam_file_path)
        nfi_gdf = self.load_data(nfi_file_path)

        woodland = nfi_gdf[nfi_gdf['category'] == 'Woodland']
        shared_cols = [col for col in lad_gdf.columns if col in sam_df.columns]
        lad_sam_gdf = lad_gdf.merge(sam_df, on=shared_cols)

        lad_sam_woodland_gdf = gpd.sjoin(lad_sam_gdf, woodland, how='left')

        lad_sam_woodland_gdf[f'pct_woodland_{year}'] = lad_sam_woodland_gdf['area_ha'] / lad_sam_woodland_gdf['arealhect'] * 100

        pct_groupby = lad_sam_woodland_gdf.groupby(important_col)[[f'pct_woodland_{year}']].sum()
        self.save_data(pct_groupby, f'{year}_LAD_pct_woodland')

        lad_gdf[f'pct_woodland_{year}'] = pct_groupby

        lad_gdf.plot(column=f'pct_woodland_{year}', figsize=(20, 20),cmap='Greens', legend=True)
        plt.title(f'Percentage of woodland by LAD for {year}')
        plt.xlabel('')
        plt.ylable('')
        plt.savefig(f"{self._output_dir}/{year}_LAD_pct_woodland.jpeg")               
        self.save_data(pct_groupby, f'{year}_LAD_pct_woodland')
        
        if save_shp_file:
            self.save_data(lad_sam_woodland_gdf, f'{year}_LAD_pct_woodland')
        
        return True