from src.SDG15_1_1 import SDG15_1_1
from user_params import UserParams

def run(params: UserParams) -> None:
    
    gfr: SDG15_1_1 = SDG15_1_1('', params.root_dir, params.data_dir, params.output_dir)

    if params.single_year_test and all([params.lad_file_path, params.sam_file_path, params.nfi_file_path, params.year_start]):
        print(f'Running single year export for year: {params.year_start}')
        gfr.calculate_sdg(params.lad_file_path, params.sam_file_path, params.nfi_file_path, params.year_start)

    if not params.single_year_test and all([params.year_start, params.year_end]):
        print(f'Running multi year export for years: {params.year_start}-{params.year_end}')
        gfr.calculate_multiple_years(params.year_start, params.year_end)

    else:
        print('Execution failed, please check necessary params:\n')
        params.print_params()