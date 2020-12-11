# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 02:29:56 2019

@author: Gursharan
"""

import numpy as np
from os.path import join as pjoin
import os
from scipy.io import wavfile
from scipy.io import loadmat
from scipy import signal
import winsound #to play sound


data_dir = pjoin(os.getcwd(), 'input', 'audio')
wav_fname = pjoin(data_dir, 'helicopter.wav')
fs, data = wavfile.read(wav_fname)

data_dir = pjoin(os.getcwd(), 'input', 'datafiles')
mat_fname = pjoin(data_dir, 'large_pinna_final.mat')
read_mat = loadmat(mat_fname)

left = read_mat.get('left')
right = read_mat.get('right')


left_final = np.array([],np.int16)
right_final = np.array([],np.int16)
for i in range (72):
    
    left_column=left[:,i]
    right_column=right[:,i]
    
    audio_data = data[i*12250:(i+1)*12250]
    
    convolved_left = signal.convolve(audio_data,left_column)
    convolved_right = signal.convolve(audio_data,left_column)
    
    left_final = np.append(left_final,convolved_left)
    right_final = np.append(right_final,convolved_right)


    
output_data=np.transpose(np.vstack((left_final,right_final)))      
int_output_data = np.int16(output_data)
scipy.io.wavfile.write('output/horizontal_time.wav', fs, int_output_data)
winsound.PlaySound('output/horizontal_time.wav', winsound.SND_ASYNC)