import os
from typing import Optional

class FolderMap:
    def __init__(self, root_in_dir: str, root_out_dir: Optional[str] = None) -> None:
        self.set_root_in_dir(root_in_dir)
        
        if root_out_dir is not None:
            self.set_root_out_dir(root_out_dir)
        else:
            self.set_root_out_dir(root_in_dir)
            
        self.set_data_dir(self.get_root_in_dir())
        self.set_output_dir(self.get_root_out_dir())

        
    def set_root_in_dir(self, root_in_dir: str) -> None:
        self._root_in_dir = root_in_dir
        self.create_folders(self._root_in_dir)

        
    def get_root_in_dir(self) -> str:
        return self._root_in_dir

    
    def set_root_out_dir(self, root_out_dir: str) -> None: # setter functions return None as they don't give anything back
        self._root_out_dir = root_out_dir
        self.create_folders(self._root_out_dir)

        
    def get_root_out_dir(self) -> str:
        return self._root_out_dir

    
    def set_data_dir(self, root_in_dir: str) -> None:
        self._data_dir = f'{root_in_dir}/data/'
        self.create_folders(self._data_dir)

        
    def get_data_dir(self) -> str:
        return self._data_dir

    
    def set_output_dir(self, root_out_dir: str) -> None:
        self._output_dir = f'{root_out_dir}/output/'
        self.create_folders(self._output_dir)

        
    def get_output_dir(self) -> str:
        return self._output_dir

    
    def create_folders(self, new_dir) -> bool:
        try:
            os.makedirs(new_dir, exist_ok=True)
            print(f'Directory {new_dir} was created or already existed')
        except Exception as e:
            print(f'Unable to make directory {new_dir} because of error {e}')