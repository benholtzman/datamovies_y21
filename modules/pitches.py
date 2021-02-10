# functions for defining tone intervals and sequences...
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==========================================================
# calculate frequecy for intervals (equal temperament!)
# k is the integer element in a chromatic scale
# v is the shift in octave, up(+) or down(-)
# f0 is the root note of the scale.
def note2freq(k,v,f0):
    freqs = np.round(f0*2**(v+k/12),2)
    return freqs

def intervals2elements(intervals):
    x = np.cumsum(intervals)
    elements = [0]
    for val in x[:-1]:
        elements.append(val)
    elements = np.array(elements)
    return elements

# ==========================================================
# data base for pitches to connect names to pitches,
# C4 is just a handy reference note:
pitch_classes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def pitch_dict():
    C4 = 440.0 * 2**(3/12-1)
    # print('C4 = '+str(C4))

    ints = np.arange(12)
    # octaves
    v_ref = 4
    v_vec = [-2,-1,0,1,2]

    names_ref = []
    pitches_ref = []
    for dv in v_vec:
        oct = v_ref + dv
        #print('octave = ' + str(oct))
        ref_scale_freqs = note2freq(ints,dv,C4)
        for ind,pname in enumerate(pitch_classes):
            notename = pname + str(oct)
            names_ref.append(notename)
            pitches_ref.append(np.round(ref_scale_freqs[ind],2))

    NameFreq_dict = dict((zip(names_ref,np.round(pitches_ref,2))))
    return NameFreq_dict


# ==========================================================
# Define the modes / keys !
#>>> d = {}
#>>> d['dict1'] = {}
#>>> d['dict1']['innerkey'] = 'value'
#>>> d
#{'dict1': {'innerkey': 'value'}}

def modes():
    modes_dict = {}
    modes_dict['modes7'] = {
        'ionian':[2,2,1,2,2,2,1],
        'dorian':[2,1,2,2,2,1,2],
        'phrygian':[1,2,2,2,1,2,2],
        'lydian':[2,2,2,1,2,2,1],
        'mixolydian':[2,2,1,2,2,1,2],
        'aeolian':[2,1,2,2,1,2,2],
        'lochrian':[1,2,2,1,2,2,2]
    }

    modes_dict['modes8'] = {
        '21':[2,1,2,1,2,1,2,1],
        '12':[1,2,1,2,1,2,1,2]
    }

    #modes_dict = {'modes7':modes7, 'modes8':modes8}
    return modes_dict

# ==========================================================
# Draw the pitch ring !

def makePitchRing(indexes):
    circle = np.linspace(0,2*np.pi,64)
    r = 1.0
    x = r*np.sin(circle)
    y = r*np.cos(circle)

    # the note locations.
    base_dots = np.linspace(0,2*np.pi,13)
    xd = r*np.sin(base_dots)
    yd = r*np.cos(base_dots)

    # the text locations
    r = 1.15
    xt = r*np.sin(base_dots)
    yt = r*np.cos(base_dots)

    # ========================
    # THIS probably won't let it be embedded in another figure !
    #fig1 = plt.figure()
    #ax1 = fig1.add_subplot(111, aspect='equal')
    ax1 = plt.add_subplot(111, aspect='equal')
    # (0) plot a filled square with a filled circle in it...
    # patches.Rectangle((x,y,lower left corner),width,height)
    #ax1.add_patch(patches.Rectangle((0.1, 0.1),0.5,0.5,facecolor="red"))

    ax1.add_patch(patches.Rectangle((-1.25, -1.25),2.5,2.5,facecolor=[0.6, 0.6, 0.6]))
    ax1.plot(x,y,'k-')
    ax1.plot(xd,yd,'w.')

    radius_norm = 0.08  # radius normalized, scaled to size of box

    for ind,interval in enumerate(indexes):
        # print(ind,interval)
        ax1.add_patch(patches.Circle((xd[interval], yd[interval]),radius_norm,facecolor="red"))
        ax1.text(xt[interval], yt[interval],pitch_classes[interval])

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    #plt.show()
    return ax1
