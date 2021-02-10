import numpy as np
import subprocess as sp

# need to do this to all parameters that will be time series for pfields... 
# do they all need to have the index? (seems like it)
def make_pf_string(pf_array):
    indexes = np.arange(len(pf_array))
    #print(len(pf_array), len(indexes))
    pf_withind = np.zeros(2*len(pf_array))
    pf_withind[1::2] = pf_array
    pf_withind[0:-1:2] = indexes
    pf_string = str(pf_withind.tolist()).strip('[').strip(']')
    return pf_string


# GENERATE THE RTcmix score !
def writeCmixSco_GRAN(tones_dict):
    # ====================
    base_name = tones_dict['base_name']
    score_name = base_name + '.sco'
    
    # ===========================================================================
    # add parameters to write out here:
    
    # fixed single values: 
    #pitchjitter = tones_dict['pitchjitter']
    #pitchjitter_cmd = 'pitchjitter = ' + str(pitchjitter) + '\n'
    
    hopjitter = tones_dict['hopjitter']
    hopjitter_cmd = 'hopjitter = ' + str(hopjitter) + '\n'
    
    # P-field time series: 
    
    pitch = tones_dict['p1']
    pitch_string = make_pf_string(pitch)
    pitch_cmd = "pitch = maketable(\"line\", \"nonorm\", 1000, " + pitch_string + ')\n'
    
    dur = tones_dict['dur_sound']
    dur_string = 'dur = ' + str(dur) + '\n'
    print(dur_string)
    
    amp = tones_dict['amplitude']
    print(len(amp))
    if len(amp)==1:
        amp_string = str(amp.tolist()).strip('[').strip(']')
        amp_cmd = 'amp = ' + amp_string + '  \n'
        print('Amplitude is a fixed value: ' + amp_string )
    elif len(amp)>1:
        amp_string = make_pf_string(amp)
        amp_cmd = 'amp = maketable(\"line\", \"nonorm\", 1000, ' + amp_string + ')\n'
        print('Amplitude is time varying (p-field)')
    
    pitchjtr = tones_dict['pitchjitter']
    print(len(pitchjtr))
    if len(pitchjtr)==1:
        pitchjtr_string = str(pitchjtr.tolist()).strip('[').strip(']')
        pitchjitter_cmd = 'pitchjitter = ' + pitchjtr_string + '  \n'
        print('Pitchjitter is a fixed value: ' + pitchjtr_string )
    elif len(pitchjtr)>1:
        pitchjtr_string = make_pf_string(pitchjtr)
        #amp_cmd = "pitch = maketable(\"line\", \"nonorm\", 1000, " + amp_string + ')\n'
        pitchjitter_cmd = 'pitchjitter = maketable(\"line\", \"nonorm\", 1000, ' + pitchjtr_string + ')\n'
        print('Pitchjitter is time varying (p-field)')

    # ===========================================================================
    
    
    #----------------------CHECK IF CMIX COMMAND IS INSTALLED-----------------------
    #only use rtoutput if CMIX command is found.
    cmixStatus, cmixResult = sp.getstatusoutput("CMIX")
    #the cmixInstalled variable can also be passed from the notebook
    #in that is case, the output of sp.getstatusoutput("CMIX") is overridden
    if 'cmixInstalled' in tones_dict:
        if tones_dict['cmixInstalled']:
            cmixStatus = 0
        else:
            cmixStatus = 127

    if cmixStatus == 0:
        output_string = 'rtoutput(\"' + base_name + '.wav\")\n'
        # don't need the brackets to make it an array !
        print("CMIX found.")
        print(output_string)
        #f_out.write(output_string)
    else:
        print("CMIX not found; rtoutput() will not be used in score.")
    #-------------------------------------------------------------------------------

    # ===========================================================================
    # START WRITING THE SCORE FILE: =========================
    f_out = open("./" + score_name , 'w')
    # MUST DELETE THE SOUND FILE BEFORE RUNNING (either with python or with -clobber )
    f_out.write("set_option(\"clobber = on\")\n") #"\n" added
    f_out.write("rtsetparams(44100, 1)\n") # mono sound ! 
    # f_out.write("rtsetparams(44100, 2)\n") # stereo sound
    f_out.write("reset(44100)\n")
    f_out.write("load(\"GRANSYNTH\")\n")
    f_out.write(dur_string)

    #output_string = 'rtoutput(\"' + base_name + '.wav\")\n'
    # don't need the brackets to make it an array !
    #print(output_string)
    if cmixStatus == 0:
        f_out.write(output_string)

    #f_out.write("waveform = maketable(\"sine\", 1000, 1.0, 0.4, 0.2)\n")
    #f_out.write("ampenv = maketable(\"window\", 1000, \"hamming\")\n")

    # AMPLITUDE
    #f_out.write("amp = maketable(\"line\", 500, 0,0, 1,1, 2,0.5, 3,1, 4,0)\n")
    #f_out.write("amp = 7000 \n")
    f_out.write(amp_cmd)
    
    #f_out.write("wave = maketable(\"wave\", 2000, 1, 0, 0.7, 0, 0.4)\n") ?????????? no indexes?
    f_out.write("wave = maketable(\"wave\", 2000, \"sine\")\n")
    f_out.write("granenv = maketable(\"window\", 2000, \"hanning\")\n")
    #f_out.write("hoptime = maketable(\"line\", \"nonorm\", 1000, 0,0.01, 1,0.002, 2,0.05)\n")
    f_out.write("hoptime = 0.01\n") # "maketable(\"line\", \"nonorm\", 1000, 0,0.01, 1,0.002, 2,0.05)\n")
    #f_out.write("hoptime = maketable(\"line\", \"nonorm\", 1000, 0,0.01, 1,0.002, 2,0.05)\n")

    # can these be pfields? 
    #f_out.write("hopjitter = 0.0001\n") # randomness around hoptime !
    #f_out.write("hopjitter = 0.00\n") 
    
    f_out.write("mindur = .05\n")
    f_out.write("maxdur = .05\n")
    #f_out.write("mindur = .04\n")
    #f_out.write("maxdur = .06\n")
    f_out.write("minamp = maxamp = 0.9\n")
    
    # PITCH: 
    #f_out.write("pitch = maketable(\"line\", \"nonorm\", 1000, 0,1, 1,20)\n")
    f_out.write(pitch_cmd)
    
    # TRANSPCOLL (not sure what this does)
    #f_out.write("transpcoll = maketable(\"literal\", \"nonorm\", 0, 0, .02, .03, .05, .07, .10)\n")
    f_out.write("transpcoll = maketable(\"literal\", \"nonorm\", 0, 0)\n")
    
    # PITCH JITTER
    #f_out.write("pitchjitter = 1\n")
    f_out.write(pitchjitter_cmd)
    # HOP JITTER
    f_out.write(hopjitter_cmd)
    
    
    f_out.write("st = 0\n")  # what does this do ?  NEED it there, whatever it is :) 
    f_out.write("GRANSYNTH(st, dur, amp, wave, granenv, hoptime, hopjitter, mindur, maxdur, minamp, maxamp, 1.0*pitch, transpcoll, pitchjitter, 14, 1)\n") # mono
    #f_out.write("GRANSYNTH(st, dur, amp, wave, granenv, hoptime, hopjitter, mindur, maxdur, minamp, maxamp, 1.0*pitch, transpcoll, pitchjitter, 14, 0, 1)\n") # stereo
    print("RTcmix score created.")
    
    return
