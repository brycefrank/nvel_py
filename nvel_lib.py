import os
from ctypes import *

mydll = cdll.LoadLibrary('/home/bryce/Programming/nvel_py/libvollib.so')


# TODO: Think about looking for segfaults

# One issue here will be backwards compatibility with python 2 and 3
# so the first step is to test c_char_p and c_wchar_p

# Another issue is the version names in windows vs. linux...
# probably something to deal with now


def func_convert(func_string):
    """
	Because function calls within the library are different for Windows and Linux
	we need to convert those func_strings to compatibile versions.

	For example, a library function call would look like:
	nvel_lib.getvoleq_([args]) in Linux and
    nvel_lib.GETVOLEQ([args]) in Windows

    This function accepts either Windows-style or Linux-style function calls
	and converts one into the other.
    """
    # TODO: Consider different ways to handle conversion. I think the best way
    # is to keep pep-8 compliant function strings as the input, for example
	# 'getvoleq' would correspond to 'getvoleq_ and GETVOLEQ' respectively

    # TODO: As a separate issue, this is not terribly robust:

    # First, check if string is Linux-style
    if ('_' in func_string) and (func_string[:-1].islower()):
        pass
	# Next check if string is Windows-style
    elif (func_string.isupper()):
        pass
	# Otherwise something strange happened, raise an error
    else:
        raise Exception('Function string: {} passed does not match \
		                 Linux or Windows styles.'.format(func_string))

def call_lib(func_string):
    """
    Calls the library, but in a restrained way.
    """

    pass


class NVEL:
    def __init__(self, lib_path):
        self.lib_path = lib_path
        self.lib = cdll.LoadLibrary(lib_path)

		# Check if OS is Windows or Linux
        if os.name == 'nt':
            self.op_sys = 'Windows'
        elif os.name == 'posix':
            self.op_sys = 'Linux'
        else:
            raise Exception('You are not using Windows or Linux! nvel_py is therefore \
			                 incompatible with your system.')


    def vernum(self):
        """
		Gets the version number of the installed library.
		"""

		# Create container for version integer.
        version = c_int()

		# Call funtion to library.
        #method_to_call = getattr(mydll, 'vernum_')
        #method_to_call(byref(version))

        self.lib.vernum_(byref(version))
        return version.value

