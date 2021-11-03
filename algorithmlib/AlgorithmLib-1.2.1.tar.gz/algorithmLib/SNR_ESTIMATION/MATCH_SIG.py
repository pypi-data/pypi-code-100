# -*- coding: UTF-8 -*-
import copy
import sys
import wave

sys.path.append('../')
from ctypes import *
from commFunction import emxArray_real_T,get_data_of_ctypes_
import  ctypes
import numpy as np

# DLL_EXPORT void matchsig_2(const emxArray_real_T *ref, const emxArray_real_T *sig, double
#                 fs, double type,emxArray_real_T *sig_out, double *delay, double *err)

def match_sig(refFile=None,targetFile=None,outFile=None):
    """
    """

    refstruct, refsamplerate,reflen = get_data_of_ctypes_(refFile)
    teststruct, testsamplerate,testlen = get_data_of_ctypes_(targetFile)
    outlen = max(reflen,testlen)
    data =  np.array([0.0 for _ in range(outlen)])
    data = data.astype(np.float64)

    outStruct = emxArray_real_T()
    #outStruct = create_string_buffer(20)
    outStruct.pdata =  (c_double * outlen)(*data)
    outStruct.psize = (c_int * 1)(*[outlen])
    outStruct.allocSize = outlen
    outStruct.NumDimensions = 1
    outStruct.canFreeData = 1

    if refsamplerate != testsamplerate :
        raise TypeError('Different format of ref and test files!')
    mydll = ctypes.windll.LoadLibrary(sys.prefix + '/matchsig.dll')
    mydll.matchsig_2.argtypes = [POINTER(emxArray_real_T), POINTER(emxArray_real_T), POINTER(emxArray_real_T),c_double,c_double,
                                     POINTER(c_double), POINTER(c_double)]
    delay, err = c_double(0.0), c_double(0.0)
    mydll.matchsig_2(byref(refstruct), byref(teststruct), byref(outStruct),c_double(refsamplerate),c_double(1),byref(delay), byref(err))
    if err.value > 0.0:
        return None
    else:
        if outFile is not None:
            outf = wave.open(outFile,'wb')
            outf.setnchannels(1)
            outf.setsampwidth(2)
            outf.setframerate(refsamplerate)
            # 将wav_data转换为二进制数据写入文件
            outlist=[]
            for a in range(outStruct.psize[0]):
                outlist.append(int(outStruct.pdata[a]))
            outarray = np.array(outlist)
            outarray = outarray.astype(np.int16)
            outf.writeframes(bytes(outarray))
            outf.close()
        return delay.value




if __name__ == '__main__':
    print(match_sig(refFile='speech.wav', targetFile='test.wav', outFile='outfile.wav'))

    pass