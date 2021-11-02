
"""
Welcome to scalabis, a fast sequence mismatch matching python package
"""

from numba import njit
import numpy as np

def storage(search=None,
            template=None,
            search_bin=None,
            template_bin=None,
            location=None,
            mismatches=None,
            found=None):
    
    return {"search":search,
             "template":template,
             "search_bin":search_bin,
             "template_bin":template_bin,
             "location":location,
             "mismatches":mismatches,
             "found":template[location:],
             "found_array":found}

def seq2bin(sequence):
    
    """ Converts any string to a binary array, 
    and then to an int8 format numpy array 
    
    Parameters:
    -----------------
    sequence : Any string
    
    -----------------
    
    Returns: 
    -----------------
    out : np.array in int format"""
    
    if type(sequence) == str:
        byte_list = bytearray(sequence,'utf8')
    else:
        raise Exception ("input must be in str format")
        
    return np.array((byte_list), dtype=np.int8)

@njit
def border_finder(array1,array2,mismatch): 
    
    """ searches for one sequence in another based on the number of mismatches. 
    Used for searching for a specific start/end place in a sequence.
    Return the index of the found search sequence in the template
    
    Parameters:
    -----------------
    array1 : np.array in int format
    array2 : np.array in int format
    mismatch : number of allowed mismatches
    
    -----------------
    
    Returns: 
    -----------------
    i : if found, the location of the found feature
    None : if not found, None type """
    
    s=array1.size
    r=array2.size
    for i,bp in enumerate(array2):
        comparison = array2[i:s+i]
        finder = mismatch_subtract(array1,comparison,mismatch)
        if finder != 0:
            return i
        if i > r-s:
            return None

@njit
def mismatch_subtract(array1,array2,mismatch):
    
    """ Used for matching 2 sequences based on the allowed mismatches.
    Breaks iteration as soon as the number of found mismatches is larger than
    the allowed mismatches.
    
    Parameters:
    -----------------
    array1 : np.array in int format
    array2 : np.array in int format
    mismatch : number of allowed mismatches
    
    -----------------
    
    Returns: 
    -----------------
    0 : if the number of misses is greater than the number of allowed mismatches
    1 : if the number of misses is less then the number of allowed mismatches """
    
    miss=0
    for arr1,arr2 in zip(array1,array2):
        if arr1-arr2 != 0:
            miss += 1
        if miss>mismatch:
            return 0
    return 1

@njit
def array_subtract(array1,array2):
    
    """ Used for quickly calculating number of mismatches between any 2 sequences.
    
    Parameters:
    -----------------
    array1 : np.array in int format
    array2 : np.array in int format

    -----------------
    
    Returns: 
    -----------------
    miss : total number of mismatches between two sequences"""
    
    miss=0
    for arr1,arr2 in zip(array1,array2):
        if arr1-arr2 != 0:
            miss += 1
    return miss

@njit
def array_index_find(array, tracer=1):
    
    """ returns the index location of all tracer elements in a numpy array.
    
    Parameters:
    -----------------
    array : np.array in int format
    tracer : the element to be tracked. By default this is 1, as this is the
    default mismatch flag in this module.

    -----------------
    
    Returns: 
    -----------------
    positions : np array with the index of all positions of the tracer element """
    
    positions = np.array((),dtype=np.int64)
    for i,match in enumerate(array):
        if match == tracer:
            positions=np.append(positions,np.int64(i))
    return positions

@njit
def full_array_subtract(array1,array2,array_length,start=0):
    
    """ Used for fully matching 2 sequences.
    Requires the sequences to be in numpy int form
    
    Parameters:
    -----------------
    array1 : np.array in int format
    array2 : np.array in int format
    array_length : length of the largest array
    start : index position in which the search starts on array

    -----------------
    
    Returns: 
    -----------------
    compared_array : np array with the index of all positions of the tracer element """
    
    compared_array = np.zeros(array_length-start)
    for i,(arr1,arr2) in enumerate(zip(array1,array2[start:])):
        if arr1-arr2 != 0:
            compared_array[i] = 1
    return compared_array

def compare(search=None,template=None,start=0,dict_return=True):
    
    """ position wise full sequence comparison. An entire sequence is compared 
    against another. Non equal positions are returned as 1, equals are 
    returned as 0.
    
    Parameters:
    -----------------
    search : A search sequence
    template : A template sequence where the search will take place
    start : index position in which the search starts in array
    dict_return : returns a dictionary using the storage() function.
    If set to False, only returns a tupple with the full comparison array.

    -----------------
    
    Returns: 
    -----------------
    dict_return : returns a dictionary using the storage() function. 
    Its slower, but easier to interpret and perform calls.
    set as dict_return=True
    
    found : np.array with the full sequence position wise comparison.
    Faster approach. ideal for multiple comparison calls. 
    set as dict_return=False """
    
    array_length = max(len(search),len(template))
    array1_bin,array2_bin=seqs2bin(search,template)
    found = full_array_subtract(array1_bin,array2_bin,array_length,start=start)
    if dict_return:
        return storage(search,template,array1_bin,array2_bin,start,np.sum(found),found)
    else:
        return found
    
def comparefromfound(search=None,template=None,mismatch=0,start=0,dict_return=True):
    
    """ Built on compare(). Does the same as this latter, but searches the template
    sequence for a key search sequence before starting a comparison from the index
    corresponding to the found search sequence.
    
    Parameters:
    -----------------
    search : A search sequence
    template : A template sequence where the search will take place
    start : index position in which the search starts in array
    dict_return : returns a dictionary using the storage() function.
    If set to False, returns a start position corresponding to the search index;
    A tupple with the full comparison array; The template sequence in the 
    orginal format starting at the index of the found search sequence.

    -----------------
    
    Returns: 
    -----------------
    dict_return : returns a dictionary using the storage() function. 
    Its slower, but easier to interpret and perform calls.
    set as dict_return=True
    
    found : np.array with the full sequence position wise comparison.
    Faster approach. ideal for multiple comparison calls. 
    set as dict_return=False 
    
    None : If no search sequence are found in the template"""
    
    start=find(search,template,mismatch=mismatch,dict_return=False)
    if start is not None:
        if dict_return:
            return compare(search,template,start=start[1])
        else:
            return start, compare(search,template,start=start[1],dict_return=False), template[start[1]:]
    else:
        return None
    
def compareandlocate(start=0,search=None,template=None):
    
    """ Built on compare(). Does the same as this latter, but returns all the
    indexes in the template in which the 2 sequences diverge. If both sequences
    are of different lenghts, defining a start position in the template might
    be advisable as comparison is always performed from index 0 on both sequences.
    
    Parameters:
    -----------------
    search : A search sequence
    template : A template sequence where the search will take place
    start : index position in which the search starts in array
    
    -----------------
    
    Returns: 
    -----------------

    found : np.array with the full sequence position wise comparison."""
    
    array=compare(search,template[start:],dict_return=False)
    return array_index_find(array)

def seqs2bin(array1,array2):
    
    """ Uses seq2bin() to convert 2 sequences from str to np.arrays.
    
    Parameters:
    -----------------
    array1 : sequence in str format
    array2 : sequence in str format

    -----------------
    
    Returns: 
    -----------------
    bin1 : np.array in int format of sequence 1
    bin2 : np.array in int format of sequence 2"""
    
    bin1=seq2bin(array1)
    bin2=seq2bin(array2)
    return bin1,bin2

def mismatch_counter(array1,array2,start=0):
    
    """ Uses array_subtract(). Count by how many mismatches 2 sequences diverge
    
    Parameters:
    -----------------
    array1 : sequence in str format
    array2 : sequence in str format
    start : index position in which the comparison starts on array2

    -----------------
    
    Returns: 
    -----------------
    out : number of mismatches between 2 sequences."""
    
    array1,array2=seqs2bin(array1,array2[start:])
    return array_subtract(array1,array2)

def find(search_seq,template,mismatch=0,start=0,dict_return=True):
    
    """ Uses border_finder(). Searches the template for a search sequence with
    the input number of mismatches
    
    Parameters:
    -----------------
    array1 : sequence in str format
    array2 : sequence in str format
    start : index position in which the comparison starts on array2

    -----------------
    
    Returns: 
    -----------------
    
    dict_return : returns a dictionary using the storage() function. 
    Its slower, but easier to interpret and perform calls.
    set as dict_return=True
    
    found : tupple with the located search word in the template, and the index.
    Faster approach. ideal for multiple comparison calls. 
    set as dict_return=False 

    None : If no search sequence are found in the template"""
    
    search_seq_bin,template_bin=seqs2bin(search_seq,template[start:])
    i=border_finder(search_seq_bin,template_bin,mismatch=mismatch)
    if i is not None:
        found = template[i:i+len(search_seq)]
        if dict_return:
            return storage(search_seq,template,search_seq_bin,template_bin,i,mismatch,found)
        else:
            return found,i
    else:
        return None

# regex test
#def find(search_seq,template,mismatch=0,dict_return=True,return_template=False):
#    search_seq_bin,template_bin=seqs2bin(search_seq,template)
#    i=regex.search("("+search_seq+"){e<=4}", f"{template}").span(0)[0]
#    if i is not None:
#        found = template[i:i+len(search_seq)]
#    else:
#        found = None
#    if dict_return:
#        return storage(search_seq,template,search_seq_bin,template_bin,i,mismatch,found)
#    else:
#        return found,i

### test code

sequence1 = "pihton"
sequence2 = "Hello there, this is a test for a fast & easy mismatch matching python module. Allegedly, it is efficient"

#count by how many mismatches 2 same lenght sequences diverge:
mismatch_counter(sequence1,sequence2)

#find one sequence in another, with mismatches. return_template=True returns 
found = find(sequence1,sequence2,mismatch=1)
#without return in a class
found = find(sequence1,sequence2,mismatch=2,dict_return=False)

#compare two sequences, searching from the search sequence from a specified starting point (default=0), 
#returning the full aligned matrix. Mismatches are the total mismatches in the compared matrix
found = comparefromfound(sequence1,sequence2,mismatch=0,start=0,dict_return=True)

#compare two sequences, returning all the locations in which they differ
found = compareandlocate(start=0,search=sequence1,template=sequence2)

#compare two sequences, returning the full aligned matrix. starting point can be specified
found = compare(search=sequence1,template=sequence2,start=0,dict_return=False)
    