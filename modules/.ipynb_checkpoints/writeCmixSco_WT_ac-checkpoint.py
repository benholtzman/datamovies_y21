# GENERATE THE RTcmix score ! (alternate to generating the midi score)
import subprocess as sp

def writesco(tones_dict,base_name):
    # ====================
    score_name = base_name + '.sco'
    print(score_name)
    f_out = open("./" + score_name , 'w')
    # YOU MUST DELETE THE SOUND FILE BEFORE RUNNING (either with python or with -clobber )
    f_out.write("set_option(\"clobber = on\")")
    f_out.write("rtsetparams(44100, 2)\n")
    f_out.write("reset(44100)\n")
    f_out.write("load(\"WAVETABLE\")\n")

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
        f_out.write(output_string)
    else:
        print("CMIX not found; rtoutput() will not be used in score.")
#-------------------------------------------------------------------------------
    #output_string = 'rtoutput(\"' + base_name + '.wav\")\n'
    # don't need the brackets to make it an array !
    #f_out.write(output_string)

    f_out.write("waveform = maketable(\"wave\", 1000, 1.0, 0.4, 0.2)\n")
    f_out.write("ampenv = maketable(\"window\", 1000, \"hamming\")\n")
    # write out the score !
    # (start time, duration, amplitude, frequency, channel mix [0 left, 1.0 right],
    # table_handle (which waveform to use)

    # for now, constants:

    # reset(44100) makes it very very smooth...

    tab_han = 'waveform'

    times = tones_dict['times']
    notes = tones_dict['notes']
    durs = tones_dict['durs']
    amps = tones_dict['amps']
    pans = tones_dict['pans']

    for i,note_val in enumerate(notes):
        t_start = times[i]
        dur = durs[i]
        freq = note_val # coming in from enumerate
        amp = amps[i]
        pan = pans[i]

        note_string = 'WAVETABLE(' + str(t_start) + ', ' \
                      + str(dur)  + ', ' + str(amp) + '*ampenv' + ', ' \
                      + str(freq)  + ', ' + str(pan)  + ', ' \
                      +  tab_han + ')\n'
        f_out.write(note_string)
    f_out.close()
    return score_name
