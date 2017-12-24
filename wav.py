#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 18:29:11 2017

@author: zak
"""

import numpy as np
import scipy.io.wavfile as siow




class sec(object):
    def __init__(self, wav_segment):
        self.wav_segment = wav_segment
    def __getitem__(self, key):
        start=None
        stop=None
        step= None
        if isinstance(key, tuple):
            if len(key)>1:
                self.wav_segment = self.wav_segment[:, key[1]]
                key = key[0]
            else:
                key = key[0]
        if key.start:
            start = int(key.start*self.wav_segment.fs)
        if key.stop:
            stop = int(key.stop*self.wav_segment.fs)
        if key.step:
            step = int(key.step*self.wav_segment.fs)
        key = slice(start, stop, step)
        return self.wav_segment.__getitem__(key)

class msec(object):
    def __init__(self, wav_segment):
        self.wav_segment = wav_segment
    def __getitem__(self, key):
        start=None
        stop=None
        step= None
        if isinstance(key, tuple):
            if len(key)>1:
                self.wav_segment = self.wav_segment[:, key[1]]
                key = key[0]
            else:
                key = key[0]
        if key.start:
            start = int(key.start*self.wav_segment.fs*10**(-3))
        if key.stop:
            stop = int(key.stop*self.wav_segment.fs*10**(-3))
        if key.step:
            step = int(key.step*self.wav_segment.fs*10**(-3))
        key = slice(start, stop, step)
        return self.wav_segment.__getitem__(key)

class WavSegment(object):
    def __init__(self, filename=None, data=None, **kwargs):
        if data is not None and kwargs.get("fs"):
            self.data = data
            self.fs = kwargs.get('fs')
        if filename:
            self.fs, self.data = siow.read(filename)
        shape = self.data.shape
        self.data.shape = sorted(shape, reverse=True) if len(shape)>1 else shape + (1,)
        self.nchannels = self.data.shape[1]
        self.duration = float(self.data.shape[0])/float(self.fs)
        self.sec = sec(self)

    def __getitem__(self, key):
        return self.__class__(data=self.data[key], fs=self.fs)

    def __add__(self, wav_seg):
        if self.nchannels != wav_seg.nchannels:
            raise ValueError("operands could not be broadcast together")
        if self.fs != wav_seg.fs:
            raise ValueError("sampling frequencies must be the same")
        data = np.concatenate((self.data, wav_seg.data))
        return self.__class__(data=data, fs=self.fs)

    def __lt__(self, wav_seg):
        return self.duration.__lt__(wav_seg.duration)

    def __gt__(self, wav_seg):
        return wav_seg.__lt__(self)

    def __eq__(self, wav_seg):
        return self.duration == wav_seg.duration

    def __mul__(self, coef):
        coef_i = int(np.floor(coef))
        coef_rn = int((coef-coef_i)*self.data.shape[0])
        data = reduce(lambda x, y: x+y, [self.data]*coef_i)
        data = data + data[:coef_rn]
        return self.__class__(data=data, fs=self.fs)

    def loop(self, ntimes=2):
        return self*ntimes

    def add_channels(self, wav_seg=None, inplace=True):
        data = None
        if wav_seg and self.fs != wav_seg.fs:
            raise ValueError("sampling frequencies must be the same")
        if wav_seg and inplace:
            self.nchannels += wav_seg.nchannels
            self.data = np.concatenate((self.data, wav_seg.data), axis=1)
        elif wav_seg and not inplace:
            data = self.__class__(data=np.concatenate((self.data,
                                                       wav_seg.data),
                                                       axis=1),
                                  fs=self.fs)
        if inplace:
            self.data = data
        else:
            return data

    def play(self, channels_idx, blocking=False, **kwargs):
        pass
    
        
        
        
        
        
