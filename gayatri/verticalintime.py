# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 02:29:56 2019

@author: Gayatri
"""

import numpy as np
from scipy.io import wavfile
from scipy.io import loadmat
import scipy.signal
from scipy import signal


fs, data = wavfile.read('audio.wav')

read_mat = loadmat('large_pinna_frontal.mat')

left = read_mat.get('left')
right = read_mat.get('right')


left_final = np.array([],np.int16)
right_final = np.array([],np.int16)
for i in range (13,85):
    
    left_column=left[:,i]
    right_column=right[:,i]
    
    audio_data = data[(i-13)*12250:(i-12)*12250]
    
    convolved_left = signal.convolve(audio_data,left_column)
    convolved_right = signal.convolve(audio_data,left_column)
    
    left_final = np.append(left_final,convolved_left)
    right_final = np.append(right_final,convolved_right)


    
output_data=np.transpose(np.vstack((left_final,right_final)))      
int_output_data = np.int16(output_data)
scipy.io.wavfile.write('vertical_time.wav', fs, int_output_data)