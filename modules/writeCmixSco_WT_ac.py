# GENERATE THE RTcmix score ! (alternate to generating the midi score)
import subprocess as sp


def writesco(tones_dict: dict, base_name: str) -> str:
    """
    Generate an RTcmix score file based on the input parameters.

    Parameters
    ----------
    tones_dict : dict
        A dictionary containing the parameters to be used to generate the score.
        It should have the following keys:
        - "times" : array-like
            A list of start times for each note in the score.
        - "notes" : array-like
            A list of note frequencies for each note in the score.
        - "durs" : array-like
            A list of note durations for each note in the score.
        - "amps" : array-like
            A list of note amplitudes for each note in the score.
        - "pans" : array-like
            A list of note pan values (0 for left, 1 for right) for each note in the score.
        - "cmixInstalled" : bool, optional
            A flag to indicate whether the CMIX command is installed on the system.
            If not provided, it will be detected using the `sp.getstatusoutput()` function.

    base_name : str
        The base name of the score file. The output score file will be saved with
        the extension ".sco" appended to the base name.

    Returns
    -------
    str
        The name of the generated score file.

    Notes
    -----
    This function uses the subprocess module to check whether the CMIX command is
    installed on the system. If the `cmixInstalled` flag is not provided, it will
    use `sp.getstatusoutput()` to check for the command. If the command is found,
    it will use the `rtoutput()` function to output the score as a WAV file. If
    the command is not found, `rtoutput()` will not be used and the score will be
    generated without any audio output.
    """

    # ====================
    score_name = base_name + ".sco"
    print(score_name)
    f_out = open("./" + score_name, "w")
    # YOU MUST DELETE THE SOUND FILE BEFORE RUNNING (either with python or with -clobber )
    f_out.write('set_option("clobber = on")')
    # for Linux users:
    # run `aplay --list-devices` in the terminal 
    # find which card # and device # your 'speaker' is
    # then uncomment the following line and replace the two numbers
    # with card # and device #
    #f_out.write('set_option("device=plughw:0,2")')
    f_out.write("rtsetparams(44100, 2)\n")
    f_out.write("reset(44100)\n")
    f_out.write('load("WAVETABLE")\n')

    # ----------------------CHECK IF CMIX COMMAND IS INSTALLED-----------------------
    # only use rtoutput if CMIX command is found.
    cmixStatus, cmixResult = sp.getstatusoutput("CMIX")
    # the cmixInstalled variable can also be passed from the notebook
    # in that is case, the output of sp.getstatusoutput("CMIX") is overridden
    if "cmixInstalled" in tones_dict:
        if tones_dict["cmixInstalled"]:
            cmixStatus = 0
        else:
            cmixStatus = 127

    if cmixStatus == 0:
        output_string = 'rtoutput("' + base_name + '.wav")\n'
        # don't need the brackets to make it an array !
        print("CMIX found.")
        print(output_string)
        f_out.write(output_string)
    else:
        print("CMIX not found; rtoutput() will not be used in score.")
    # -------------------------------------------------------------------------------
    # output_string = 'rtoutput(\"' + base_name + '.wav\")\n'
    # don't need the brackets to make it an array !
    # f_out.write(output_string)

    f_out.write('waveform = maketable("wave", 1000, 1.0, 0.4, 0.2)\n')
    f_out.write('ampenv = maketable("window", 1000, "hamming")\n')
    # write out the score !
    # (start time, duration, amplitude, frequency, channel mix [0 left, 1.0 right],
    # table_handle (which waveform to use)

    # for now, constants:

    # reset(44100) makes it very very smooth...

    tab_han = "waveform"

    times = tones_dict["times"]
    notes = tones_dict["notes"]
    durs = tones_dict["durs"]
    amps = tones_dict["amps"]
    pans = tones_dict["pans"]

    for i, note_val in enumerate(notes):
        t_start = times[i]
        dur = durs[i]
        freq = note_val  # coming in from enumerate
        amp = amps[i]
        pan = pans[i]

        note_string = (
            "WAVETABLE("
            + str(t_start)
            + ", "
            + str(dur)
            + ", "
            + str(amp)
            + "*ampenv"
            + ", "
            + str(freq)
            + ", "
            + str(pan)
            + ", "
            + tab_han
            + ")\n"
        )
        f_out.write(note_string)
    f_out.close()
    return score_name
