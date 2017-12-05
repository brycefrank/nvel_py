import os
import signal
from ctypes import *


# TODO: Think about looking for segfaults


# One issue here will be backwards compatibility with python 2 and 3
# so the first step is to test c_char_p and c_wchar_p

# Another issue is the version names in windows vs. linux...
# probably something to deal with now

def args_check(args):
    """
    Checks the arguments passed to a library function for the correct ctypes, this is
    to prevent mysterious segmentation faults.
    """
    pass

def arg_convert(args):
    """
    Converts arguments passed to a Python function into arguments that can be passed
    into the volume library functions.
    """

    print(args)




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
    # is to keep pep-8 compliant function strings as the input, fgetvolor example
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

        DLL equivalent: VERNUM
		"""

		# Create container for version integer.
        version = c_int()

		# Call funtion to library.
        #method_to_call = getattr(mydll, 'vernum_')
        #method_to_call(byref(version))

        self.lib.vernum_(byref(version))
        return version.value

    def getvoleq(self, regn, forst, dist, spec, prod, errflag=1):
        """
        Gets the volume equation string from the volume library.

        DLL equivalent: GETVOLEQ
        """

        # Create volume equation container, a c string of length 11
        voleq = c_char_p(b'           ')

        self.lib.getvoleq_(byref(c_int(regn)), c_char_p(forst), c_char_p(dist),
                           byref(c_int(spec)), c_char_p(prod), voleq, byref(c_int(errflag)))
        return voleq.value

    def ezvollib(self, voleqi, dbhob, httot):
        """
        Gets the volume for users with only DBH and Height

        DLL Equivalent: EZVOLLIB
        """

        # TODO: Broken, getting segfaults :(
        # Could be something to do with the voleq I am using

        # Initialize volume container

        # Convert args
        voleqi = c_char_p(voleqi)
        dbhob = c_float(dbhob)
        httot = c_float(httot)

        vol = (c_float * 15)()
        
        self.lib.ezvollib_(byref(voleqi), byref(dbhob), byref(httot), vol)

    def jenkins(self, spec, dbhob):
        """
        Gets the Jenkins equation biomass using DBH in inches
        """

        spec = c_int(spec)
        dbhob = c_float(dbhob)
        bioms = (c_float * 8)()

        # Call the Jenkins equation
        self.lib.jenkins_(byref(spec), byref(dbhob), bioms)

        # Return a Python list of elements
        return [bioms[i] for i in range(len(bioms))]






# Arguments notes
# regn - region - byref(c_int())
# forst - forest - c_wchar_p("00")
# dist - district - c_wchar_p("00")
# spec - FIA Species code - byref(c_int())
# prod - product type - byref(c_int())
# errflag - error flag - byref(c_int())


a = NVEL('/home/bryce/Programming/nvel_py/libvollib.so')

flewelling_pp = a.getvoleq(1, b'06', b'01', 122, b'01')

vole = b'I00FW2W122 '


a.ezvollib(vole, 12.2, 100)


