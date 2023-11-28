import os
from Utilities.unpyc3_compiler import Unpyc3PythonCompiler

release_dir = os.path.join('..', '..', 'Release')

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join(release_dir, 'ShonenFighting'),
    names_of_modules_include=('shonenfighting',),
    output_ts4script_name='shonenfighting'
)
