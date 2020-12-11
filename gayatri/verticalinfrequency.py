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
    
    pad_data=np.zeros(12249,np.int16) #length(left_column)+length(audio_data)-1
    left_column_to_fft=np.append(left_column,pad_data)
    right_column_to_fft=np.append(right_column,pad_data)
    
    left_column_fft=scipy.fftpack.fft(left_column_to_fft)
    right_column_fft=scipy.fftpack.fft(right_column_to_fft)
    
    audio_data = data[(i-13)*12250:(i-12)*12250]
    
    pad_audio=np.zeros(199,np.int16) #length(left_column)+length(audio_data)-1
    audio_to_fft=np.append(audio_data,pad_audio)
    
    audio_fft=scipy.fftpack.fft(audio_to_fft)
    
    left_convolved_fft=left_column_fft*audio_fft
    right_convolved_fft=right_column_fft*audio_fft
    
    left_convolved_time=scipy.fftpack.ifft(left_convolved_fft)
    right_convolved_time=scipy.fftpack.ifft(right_convolved_fft)
    
    left_final = np.append(left_final,left_convolved_time)
    right_final = np.append(right_final,right_convolved_time)


    
output_data=np.transpose(np.vstack((left_final,right_final)))      
int_output_data = np.int16(output_data)
scipy.io.wavfile.write('vertical_frequency.wav', fs, int_output_data)