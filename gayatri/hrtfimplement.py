# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:32:10 2019

@author: prthp
"""
import numpy as np

import scipy.signal
import math
from scipy.io import wavfile
from scipy import signal


# FIR filter design
a = 0.08 # head radius 0.12m
c = 343 # sound speed 340m/s (15 degree centigrade)
N = 200 # N is sample amount,200
t = (1/2) * (a/c)
 
left = np.zeros((200,36)) 
right = np.zeros((200,36))

for theta in range(36):
    for k in range(200):
        alpha = 1 + math.sin(math.radians(-90+theta*2.5)) # theta is azimuth,0~71,-90~90 based on reaseard paper
        w = 2 * math.pi * k * 44100 / N 
        tr = (1 - alpha)*t
        tl = alpha * t
        right[k][theta] = np.abs((complex( 1,2* (1-alpha) * w *t) / complex( 1 , w * t)) * np.exp(complex(0,-w * tl)))
        right[k][theta] = np.abs((complex( 1,2* alpha * w * t) / complex( 1 , w * t)) * np.exp(complex(0,-w * tr)))

fs, data = wavfile.read('audio.wav')


left_final = np.array([],np.int16)
right_final = np.array([],np.int16)
for i in range (36):
    
    left_column=left[:,i]
    right_column=right[:,i]
    
    audio_data = data[i*24500:(i+1)*24500]
    
    convolved_left = signal.convolve(audio_data,left_column)
    convolved_right = signal.convolve(audio_data,left_column)
    
    left_final = np.append(left_final,convolved_left)
    right_final = np.append(right_final,convolved_right)


    
output_data=np.transpose(np.vstack((left_final,right_final)))      
int_output_data = np.int16(output_data)
scipy.io.wavfile.write('hrtf_time.wav', fs, int_output_data)