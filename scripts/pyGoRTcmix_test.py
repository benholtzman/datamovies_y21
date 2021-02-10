# test the pyGoRTcmix method without the notebook checker.. 
import numpy as np

from subprocess import Popen
import subprocess as sp
import os


def makeSimpleScore(base_name,time,freqs,durations):
    # ====================
    score_name = base_name + '.sco'
    print(score_name)
    f_out = open("./" + score_name , 'w')
    # YOU MUST DELETE THE SOUND FILE BEFORE RUNNING (either with python or with -clobber )
    f_out.write("set_option(\"clobber = on\")")

    f_out.write("rtsetparams(44100, 2)\n")
    f_out.write("load(\"WAVETABLE\")\n")


#     #----------------------CHECK IF CMIX COMMAND IS INSTALLED-----------------------
#     #see notebook for what goes in here... 
#     #------------------------------------------------------------------------------
    
    f_out.write("waveform = maketable(\"wave\", 1000, 1.0)\n")
    # to add overtones, just add amplitude weights
    #f_out.write("waveform = maketable(\"wave\", 1000, 1.0, 0.4, 0.2)\n")

    f_out.write("ampenv = maketable(\"window\", 10000, \"hamming\")\n")    

    # write out the score ! 
    # (start time, duration, amplitude, frequency, channel mix [0 left, 1.0 right],
    # table_handle (which waveform to use)

    # for now, constants: 
            
    # reset(44100) makes it very very smooth... 
            
    amp = 10000 
    mix = 0.5 # 0 = left, 1 = right, but here just 1 channel
    tab_han = 'waveform'

    for i,freq_val in enumerate(freqs):
        t_start = time[i]
        print(t_start)
        dur = durations[i] #
        freq = freq_val
        print(freq_val)
        note_string = 'WAVETABLE(' + str(t_start) + ', ' \
                  + str(dur)  + ', ' + str(amp)+ '*ampenv' + ', ' \
                  + str(freq)  + ', ' + str(mix)  + ', ' \
                  +  tab_han + ')\n' 
        f_out.write(note_string)
        
    f_out.close()
    return score_name

# now generate the list of frequencies: 
# any value larger than 10 is read as a frequency. 
# otherwise it is read as a [   ]

freq_rats = np.asarray([1,6/5,3/2,4/3,2.0]) # 5/4 = major third, 6/5 = minor third, 4/3 = perfect fourth
root0 = 220
list_freqs = [root0, 3/2*root0, 3/2*(3/2*root0), 3/2*root0, root0]
root_freqs = np.asarray(list_freqs)

freq_seq = []
for iff,root in enumerate(root_freqs):
    print(root)
    for i,freq_rat in enumerate(freq_rats):
        freq = root*freq_rat
        freq_seq.append(freq)

freq_seq = np.asarray(freq_seq)
# ADD THE TIMES: =============================================
beepdur = 0.4 # has to match the 
sound_dur = len(freq_seq)*beepdur
time_sco = np.linspace(0,sound_dur,len(freq_seq))
durations = np.ones(len(freq_seq))*beepdur
#print(len(freq_seq),len(time_sco))
#print(time_sco)
abitextra = 0.5
dur_sound = time_sco[-1] + abitextra 


base_name = 'scale1_pygoCMIX_test'
score_name = makeSimpleScore(base_name,time_sco,freq_seq,durations)

dur = str(dur_sound)
cmix_cmd = '../pyGoRTcmix/Contents/MacOS/pyGoRTcmix -inputscore ' + os.path.abspath(base_name + '.sco ') + '-output ' + os.path.abspath(base_name + '.wav ') +'-dur ' + dur
print(cmix_cmd)

runCMIX = sp.Popen(cmix_cmd, shell=True) # if can only be called from a shell, use shell=True

runCMIX.wait()
print('\nhopefully i just wrote your sound file (' + base_name + '.wav); is it here?')
