__author__ = "Addison Raak, Michael Antkiewicz, Ka'ulu Ng, Nicholas Baldwin"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Addison Raak", "Michael Antkiewicz", "Ka'ulu Ng", "Nicholas Baldwin"]

#
# This file must be in the ROOT directory of the project. It is used to find the paths
# to the dll files that are required to use the RSA.
#

import os
from pathlib import Path

# Gets the absolute path of the pwd
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Variables holding the paths of the DLL files
RSA_DLL_PATH_x64 = Path("RSA_API/lib/x64")
RSA_DLL_PATH_x84 = Path("RSA_API/lib/x86")
DLL_FULL_PATH_x64 = ROOT_DIR / RSA_DLL_PATH_x64
DLL_FULL_PATH_x84 = ROOT_DIR / RSA_DLL_PATH_x84


# returns the ROOT_DIR of the project
def get_root():
    return ROOT_DIR


# Helper method to change the working directory to properly path the setup
# for the RSA dll file.
def change_cwd(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        return False
    return True
