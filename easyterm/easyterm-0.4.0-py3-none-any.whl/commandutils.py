import os, hashlib, subprocess, uuid
from .commandlineopt import NoTracebackError

__all__ = ["md5sum_of_file", "check_file_presence", "checksum_of_file", "random_folder"]

def check_file_presence(input_file, descriptor='input_file', exception_raised=NoTracebackError):
    """Check if file exists. If it doesn't, raises a IOError exception

    Parameters
    ----------
    input_file : str
        string of file to check, any relative or absolute path

    descriptor : str
        used for meaningful error message if file is absent

    exception_raised : class
        Exception class to be raised

    Returns
    -------
    None
        None
    """
    if not input_file or not os.path.isfile(input_file):
        raise(exception_raised(f"ERROR {descriptor}: {input_file} not defined or not found. Run with option -h for help."))
    
def md5sum_of_file(filename, chunksize=4096):
    """Gets md5sum of content of a file

    Parameters
    ----------
    filename : str
        file to be read

    Returns
    -------    
    md5sum : str
        md5sum of file
    """    
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(chunksize), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def checksum_of_file(filename):
    """ Gets checksum of content of a file, using program 'sum'

    Parameters
    ----------
    filename : str
        file to be read

    Returns
    -------
    (sum1, sum2) : (int, int)
        checksum of file
    """        
    p = subprocess.run(['sum', filename],
                       capture_output=True,
                       check=True)
    int1, int2=map(int, p.stdout.decode().strip().split())
    return( (int1, int2) )



def random_folder(parent_folder='./', mkdir=True):
    """Generate a random folder name, create it inside parent_folder, and return the path to it

    Parameters
    ----------
    parent_folder : str
        folder inside which the random_folder is desired

    mkdir : bool
        whether the random folder should be created (by default: True)

    Returns
    -------
    rnd_folder : str
        path to newly created random folder (whose name will look like 57eb3f2416bc4c5d9d34a17751c97362)

    """
    parent_folder=parent_folder.rstrip('/')+'/'
    if not os.path.isdir(parent_folder):
        raise Exception(f'random folder ERROR the parent folder does not exist: {parent_folder}')
    
    random_name=uuid.uuid4().hex # style: 57eb3f2416bc4c5d9d34a17751c97362
    random_folder_created=parent_folder + random_name
    
    if mkdir:
        os.mkdir( random_folder_created )
        
    return random_folder_created
    
