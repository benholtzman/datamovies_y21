import pandas as pd
import numpy as np 
from datetime import datetime
import time
import pickle

#initializing
time_interval=0.1
velocity=0.5
s=pd.Series([], [])
time=0.0
position=0.0
RIGHTBOUND=3
LEFTBOUND=0
#to deal with the inaccuracy python has in floating point calculation
P=5

def initialize(init_position):
    global s, position
    position=init_position
    s=s.append(pd.Series([init_position],[0]))
    
#this is the only method you need to call; the other methods below are helping methods
#input a list of desired positions. e.g. move([1,1,0.5])
def move(lst):
    global RIGHTBOUND, LEFTBOUND
    for i in lst:
        if i<=RIGHTBOUND and i>=LEFTBOUND:
            move_once(i)
        else:
            print('At least one position you entered is out of bounds.')
            break
                                
def move_once(r):
    if position<r:
        rightmost(r)
    elif position>r:
        leftmost(r)
    else:
        stay()

def stay():
    global position, time, s, e
    time=round(time+time_interval,5)
    s=s.append(pd.Series([position],[time]))
    
def rightmost(r):
    global position,time,s,e
    while position<r:
        position=round(position+velocity*time_interval,P)
        if position<=r:
            time=round(time+time_interval,P)
            s=s.append(pd.Series([position],[time]))

def leftmost(r):
    global position, time, s,e
    while position>r:
        position=round(position-velocity*time_interval,P)
        if position>=r:
            time=round(time+time_interval,P)
            s=s.append(pd.Series([position],[time]))