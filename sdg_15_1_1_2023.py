

class SDGIndicator15_1_1:
    def __init__(self, root_dir: str) -> None:
        self.set_root_dir(root_dir)
        
    
    def set_root_dir(self, root_dir: str) -> None:
        self._root_dir = root_dir
        
    
    def get_root_dir(self) -> str:
        return self._root_dir
    
    
    def _get_full_file_path(self, file_name: str) -> str:
        return f'{self.get_root_dir()}/data/{file_name}'
    
    
    def read_file(self, file_name: str, cols: List[str] = None, index: str = None, epsg: int = 27700) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        ext = file_name.split('.')[-1]

        data_read_dict = {
            'csv' : pd.read_csv,
            'shp' : gpd.read_file,
        }

        df = data_read_dict[ext](self._get_full_file_path(file_name))

        if cols:
            df = df[cols]
        if index:
            df = df.set_index(index)
        if isinstance(df, gpd.GeoDataFrame) and not df.crs.to_epsg() == epsg:
            # Set the projection to that defined in epsg in the arguments
            df = df.to_crs(epsg)

        return df   

    
    def save_file(self, df: Union[pd.DataFrame, gpd.GeoDataFrame], file_name: str) -> bool:
        if isinstance(df, pd.DataFrame):
            df.to_csv(f'{self.get_root_dir()}/output/{file_name}.csv')
        if isinstance(df, gpd.GeoDataFrame):
            df.to_file(f'{self.get_root_dir()}/output/{file_name}.shp')
        
        return True