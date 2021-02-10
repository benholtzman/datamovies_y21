# make chords from the data.. output of owecianizer...
# a better approach 
# pitches are the list of notes to find in the data(mapped to frequency)
# notes is the list of when they occur in the data
import numpy as np

def makeDataChord(pitches,time,times,data_notes):
    t_end = time[len(time)-1]
    ch_notes = []
    ch_times = []
    ch_durs = []
    grad_notes = np.gradient(data_notes)

    for i,note in enumerate(pitches):
    #for note in pitches:
        note_times = []
        note_times = times[data_notes==note]
        note_inds = np.where(data_notes==note)[0] # funny shape coming out of here... a tuple of an array and empty dim (or something)
        #print('now looping over the next note_times:')
        #print(note_times)
        #print(note_inds)
        
        
        for ind_nt, t in enumerate(note_times):            
            #print('ind_nt = ' + str(ind_nt))
            #print('t_note = ' + str(t))
            
            ind_local = int(note_inds[ind_nt])
            #print(ind_local)
            local_grad = float(grad_notes[ind_local])
            #print(local_grad)
            
            # positive slope
            if local_grad > 0.0 and ind_nt < (len(note_times)-1):
                #print('grad_notes is POS. ')
                dur = note_times[ind_nt+1] - t 
                
                #print('dur = '+ str(dur))  
                ch_notes.append(note)
                ch_times.append(t)
                ch_durs.append(dur)
                # if it is the last note: 
            elif local_grad > 0.0 and ind_nt == (len(note_times)-1):
                dur = t_end-t
                    
                #print('dur = '+ str(dur))  
                ch_notes.append(note)
                ch_times.append(t)
                ch_durs.append(dur)
                    
            # negative slope      
            elif local_grad < 0.0 and ind_nt==0: # dn_next < data_notes[ind_time]:
                #print('grad_notes is NEG. AND its the first note. ')
                dur = t

                #print('dur = '+ str(dur)) 
                ch_notes.append(note)
                ch_times.append(time[0])
                ch_durs.append(dur)

        
    return ch_notes, ch_times, ch_durs
