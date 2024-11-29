import os

from rcpsp import read_from_psplib_file
from cp_formulation import build_cp_formulation
from cp_formulation import solve
from mip_formulation import build_mip_formulation
from write_output import initialize_csv, append_to_csv



# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    problems = 'j30'
    input_directory = 'resources/' + problems
    output_directory = 'output/'
    execution_time_limit_seconds = 2
    solve_mip = False

    output_file_name = problems + '_tl' + str(execution_time_limit_seconds) + '.csv'
    output_file_path = os.path.join(output_directory, output_file_name)
    initialize_csv(output_file_path)

    for input_file_name in os.listdir(input_directory):
        valid_input_file = '.sm' in input_file_name
        if not valid_input_file:
            continue

        input_file_path = os.path.join(input_directory, input_file_name)

        rcpsp = read_from_psplib_file(input_file_path)

        if solve_mip:
            mip = build_mip_formulation(rcpsp)
            mip.mdl.solve()
        else:
            cp_formulation = build_cp_formulation(rcpsp)
            [mk, mk_optimality_gap] = solve(cp_formulation, execution_time_limit_seconds)
            append_to_csv(output_file_path, [input_file_name, mk, mk_optimality_gap])
