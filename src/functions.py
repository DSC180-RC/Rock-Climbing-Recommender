# Brian Cheng
# Eric Liu
# Brent Min

# functions.py contains a series of functions useful across all code

import os

from pathlib import Path

def make_absolute(path):
    """
    This function adjusts the input path to be absolute, if it is not already. Since this function
    uses os.path.isabs(), it should be cross platform

    :param:     path    The path to make absolute

    :return:    str     The original input path if it is already absolute, or the absolute version
                        of the input path relative to the project root
    """
    # store the absolute path in this variable
    absolute_path = path

    # if the input path is not absolute, then make it so with the project root
    if(not os.path.isabs(absolute_path)):
        # store the directory of the project root
        proj_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # make the path absolute
        absolute_path = proj_root / absolute_path

    # return the absolute path
    return absolute_path


def check_folder(path):
    """
    This function checks that the input folder exists. If it does not exist, the folder is created

    :param:     path    The folder to check for existence or to create
    """
    # ensure that the input path is absolute
    absolute_path = make_absolute(path)

    # check that the absolute path directory exists, create if it does not
    if(not os.path.exists(absolute_path)):
        os.makedirs(absolute_path)
