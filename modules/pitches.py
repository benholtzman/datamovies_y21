# functions for defining tone intervals and sequences...
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ==========================================================
# calculate frequecy for intervals (equal temperament!)
# k is the integer element in a chromatic scale
# v is the shift in octave, up(+) or down(-)
# f0 is the root note of the scale.
def note2freq(k, v, f0):
    """
    Convert a note number (given as key and value) to a frequency.

    Parameters
    ----------
    k : float
        The number of semitones from the reference frequency (in units of half-steps).
    v : float
        The reference note number (usually in the range of 0 to 11), where 0 represents
        the starting note and 11 the ending note in an octave.
    f0 : float
        The frequency of the reference note.

    Returns
    -------
    freqs : ndarray
        The resulting frequency (in Hertz) for each note specified by `k` and `v`.
    """
    freqs = np.round(f0 * 2 ** (v + k / 12), 2)
    return freqs


def intervals2elements(intervals):
    """
    Convert a sequence of intervals to a sequence of elements.

    Parameters
    ----------
    intervals : ndarray
        An array of intervals representing the differences between consecutive elements.

    Returns
    -------
    elements : ndarray
        An array of elements with the same length as `intervals`, where each element is
        the sum of all preceding intervals and the starting element is assumed to be 0.
    """
    x = np.cumsum(intervals)
    elements = [0]
    for val in x:
        elements.append(val)
    elements = np.array(elements)
    return elements


# ==========================================================
# data base for pitches to connect names to pitches,
# C4 is just a handy reference note:
def make_pitch_classes():
    """
    Create a list of pitch classes.

    Returns
    -------
    pitch_classes : list of str
        A list of twelve strings representing the names of the twelve pitch classes.
    """
    pitch_classes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return pitch_classes


pitch_classes = make_pitch_classes()


def pitch_dict():
    """
    Creates a dictionary with the names of musical notes (in the format of note name
    followed by octave number, e.g. "C4" for middle C) as keys and their corresponding 
    frequencies (in Hz) as values, assuming A4 = 440 Hz.

    Returns:
    --------
    dict: A dictionary with musical note names (e.g. "C4") as keys and their corresponding 
          frequencies (in Hz) as values.

    Examples:
    ---------
    >>> pitch_freq_dict = pitch_dict()
    >>> pitch_freq_dict['A4']
    440.0
    >>> pitch_freq_dict['C3']
    130.81
    """
    a4_freq = 440.0 * 2 ** (3 / 12 - 1)

    intervals = np.arange(12)
    # octaves
    ref_octave = 4
    octave_diffs = [-2, -1, 0, 1, 2]

    pitch_names = []
    pitch_frequencies = []
    for diff in octave_diffs:
        octave = ref_octave + diff
        ref_scale_freqs = note2freq(intervals, diff, a4_freq)
        for ind, pitch_name in enumerate(pitch_classes):
            note_name = pitch_name + str(octave)
            pitch_names.append(note_name)
            pitch_frequencies.append(np.round(ref_scale_freqs[ind], 2))

    name_freq_dict = dict((zip(pitch_names, np.round(pitch_frequencies, 2))))
    return name_freq_dict


# ==========================================================
# Define the modes / keys !
# >>> d = {}
# >>> d['dict1'] = {}
# >>> d['dict1']['innerkey'] = 'value'
# >>> d
# {'dict1': {'innerkey': 'value'}}


def modes():
    """
    Return a dictionary of dictionaries containing the intervals of each mode.
    The dictionary has two keys, 'modes7' and 'modes8', which correspond to the 7-tone and 8-tone modes.
    The value of each key is a dictionary with keys corresponding to the names of each mode and values
    corresponding to the intervals between the notes in that mode.

    Returns
    -------
    dict
        A dictionary of dictionaries containing the intervals of each mode.

    Examples
    --------
    >>> modes_dict = modes()
    >>> modes_dict['modes7']['ionian']
    [2, 2, 1, 2, 2, 2, 1]
    >>> modes_dict['modes8']['21']
    [2, 1, 2, 1, 2, 1, 2, 1]
    """
    modes_dict = {}
    modes_dict["modes7"] = {
        "ionian": [2, 2, 1, 2, 2, 2, 1],
        "dorian": [2, 1, 2, 2, 2, 1, 2],
        "phrygian": [1, 2, 2, 2, 1, 2, 2],
        "lydian": [2, 2, 2, 1, 2, 2, 1],
        "mixolydian": [2, 2, 1, 2, 2, 1, 2],
        "aeolian": [2, 1, 2, 2, 1, 2, 2],
        "lochrian": [1, 2, 2, 1, 2, 2, 2],
    }

    modes_dict["modes8"] = {
        "21": [2, 1, 2, 1, 2, 1, 2, 1],
        "12": [1, 2, 1, 2, 1, 2, 1, 2],
    }

    # modes_dict = {'modes7':modes7, 'modes8':modes8}
    return modes_dict


# ==========================================================
# Draw the pitch ring !


def makePitchRing(indexes):
    """
    Plot a ring of musical pitches.

    Parameters
    ----------
    indexes : array-like
        The indexes of the pitches to plot.

    Returns
    -------
    None

    Notes
    -----
    The function creates a ring of musical pitches, with the pitches indicated
    by filled circles in yellow. The pitch classes are indicated by text labels,
    which are also shown in the ring. The first pitch is highlighted by a red circle.

    The pitch ring is plotted in a figure and displayed using pyplot.show().

    Examples
    --------
    >>> makePitchRing([0, 2, 4, 5, 7, 9, 11])
    """

    circle = np.linspace(0, 2 * np.pi, 64)
    r = 1.0
    x = r * np.sin(circle)
    y = r * np.cos(circle)

    # the note locations.
    base_dots = np.linspace(0, 2 * np.pi, 13)
    xd = r * np.sin(base_dots)
    yd = r * np.cos(base_dots)

    # the text locations
    r = 1.15
    xt = r * np.sin(base_dots)
    yt = r * np.cos(base_dots)

    # ========================
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect="equal")

    # (0) plot a filled square with a filled circle in it...
    # patches.Rectangle((x,y,lower left corner),width,height)
    # ax1.add_patch(patches.Rectangle((0.1, 0.1),0.5,0.5,facecolor="red"))

    ax1.add_patch(
        patches.Rectangle((-1.25, -1.25), 2.5, 2.5, facecolor=[0.6, 0.6, 0.6])
    )
    ax1.plot(x, y, "k-")
    ax1.plot(xd, yd, "w.")

    radius_norm = 0.08  # radius normalized, scaled to size of box

    for ind, key_ind in enumerate(indexes):
        # print(ind,interval)
        ax1.add_patch(
            patches.Circle((xd[key_ind], yd[key_ind]), radius_norm, facecolor="yellow")
        )
        ax1.text(xt[key_ind], yt[key_ind], pitch_classes[key_ind])
        if ind == 0:
            ax1.add_patch(
                patches.Circle((xd[key_ind], yd[key_ind]), radius_norm, facecolor="red")
            )
            ax1.text(xt[key_ind], yt[key_ind], pitch_classes[key_ind])

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    plt.show()


# Object version for multiple rings in subplots:
# def makePitchRing(indexes):
#     circle = np.linspace(0,2*np.pi,64)
#     r = 1.0
#     x = r*np.sin(circle)
#     y = r*np.cos(circle)

#     # the note locations.
#     base_dots = np.linspace(0,2*np.pi,13)
#     xd = r*np.sin(base_dots)
#     yd = r*np.cos(base_dots)

#     # the text locations
#     r = 1.15
#     xt = r*np.sin(base_dots)
#     yt = r*np.cos(base_dots)

#     # ========================
#     # THIS probably won't let it be embedded in another figure !
#     #fig1 = plt.figure()
#     #ax1 = fig1.add_subplot(111, aspect='equal')
#     ax1 = plt.add_subplot(111, aspect='equal')
#     # (0) plot a filled square with a filled circle in it...
#     # patches.Rectangle((x,y,lower left corner),width,height)
#     #ax1.add_patch(patches.Rectangle((0.1, 0.1),0.5,0.5,facecolor="red"))

#     ax1.add_patch(patches.Rectangle((-1.25, -1.25),2.5,2.5,facecolor=[0.6, 0.6, 0.6]))
#     ax1.plot(x,y,'k-')
#     ax1.plot(xd,yd,'w.')

#     radius_norm = 0.08  # radius normalized, scaled to size of box

#     for ind,interval in enumerate(indexes):
#         # print(ind,interval)
#         ax1.add_patch(patches.Circle((xd[interval], yd[interval]),radius_norm,facecolor="red"))
#         ax1.text(xt[interval], yt[interval],pitch_classes[interval])

#     ax1.get_xaxis().set_visible(False)
#     ax1.get_yaxis().set_visible(False)
#     #plt.show()
#     return ax1
