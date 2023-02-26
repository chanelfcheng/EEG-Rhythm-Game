import time
from bsl import StreamRecorder, StreamPlayer, StreamReceiver, StreamViewer
from bsl.triggers import SoftwareTrigger
import os
import scipy as sp
import numpy as np
import pandas as pd


STREAM_NAME = 'Unicorn'

def filtereeg(eeg, sfreq=250, high_band=1, low_band=30, notch=60, padlen=27):
    """
    eeg: EEG data
    high: high-pass cut off frequency
    low: low-pass cut off frequency
    sfreq: sampling frequency
    notch: notch frequency
    """
    # Zero mean eeg signal
    eeg = eeg - eeg.mean()
    
    # normalise cut-off frequencies to sampling frequency
    high_band = high_band/(sfreq/2)
    low_band = low_band/(sfreq/2)
    high_stop = (notch - 1)/(sfreq/2)
    low_stop = (notch + 1)/(sfreq/2)
    
    # create notch filter for EEG
    b0, a0 = sp.signal.butter(4, [high_stop, low_stop], btype='bandstop', analog=True)
    
    # filter EEG signal
    eeg_filtered = sp.signal.filtfilt(b0, a0, eeg, padlen=padlen)
    
    # rectify EEG signal
    eeg_rectified = abs(eeg_filtered)
    
    # create bandpass filter for EEG
    b1, a1 = sp.signal.butter(4, [high_band,low_band], btype='bandpass', analog=True)
    
    # filter EEG signal
    eeg_envelope = sp.signal.filtfilt(b1, a1, eeg_rectified, padlen=padlen) 
    
    return eeg_envelope

def init_stream(bufsize=1, winsize=0.25):
    idx = 0

    # Record a data stream
    recorder = StreamRecorder(record_dir=os.path.join(os.getcwd(), 'data'),
                            fname = f'test{idx}',
                            stream_name = STREAM_NAME,
                            verbose = True)
    recorder.start()
    print(recorder)

    # Create a software trigger
    trigger = SoftwareTrigger(recorder)
    trigger.signal(1)
    
    # Receive data from stream
    receiver = StreamReceiver(bufsize=bufsize, winsize=winsize, stream_name=STREAM_NAME)
    time.sleep(2)  # wait 2 seconds to fill LSL inlet.
    receiver.acquire()

    return recorder, trigger, receiver

def filter_data(receiver, seconds_sleep=2, padlen=27):
    data1, timestamps1 = receiver.get_window(STREAM_NAME)
    data1 = np.delete(data1, np.s_[9:], axis=1)
    data1 = np.delete(data1, 0, axis=1)
    df = pd.DataFrame(data1, columns=['EEG_1', 'EEG_2', 'EEG_3',
                                        'EEG_4', 'EEG_5', 'EEG_6', 
                                        'EEG_7', 'EEG_8'])
    eeg_keys = ['EEG_' + str(i) for i in range(1, 9)]
    filt_eeg = df.copy()
    filt_eeg[eeg_keys] = filt_eeg[eeg_keys].apply(filtereeg, raw=True, padlen=padlen)
    print(filt_eeg)
    time.sleep(seconds_sleep)

    return filt_eeg

def average_voltage(filt_eeg):
    filt_eeg = (filt_eeg-filt_eeg.mean())/filt_eeg.std()
    eeg_keys = ['EEG_' + str(i) for i in range(1, 9)]
    avg_voltage = np.nanmean(filt_eeg[eeg_keys])
    print(avg_voltage)
    return avg_voltage

def close_stream():
    trigger.close()
    recorder.stop()

if __name__ == "__main__":
    idx = 0

    # Record a data stream
    recorder = StreamRecorder(record_dir=os.path.join(os.getcwd(), 'data'),
                            fname = f'test{idx}',
                            stream_name = STREAM_NAME,
                            verbose = True)
    recorder.start()
    print(recorder)

    # Create a software trigger
    trigger = SoftwareTrigger(recorder)
    trigger.signal(1)
    
    # Receive data from stream
    receiver = StreamReceiver(bufsize=1, winsize=0.25, stream_name=STREAM_NAME)
    time.sleep(2)  # wait 2 seconds to fill LSL inlet.
    receiver.acquire()
    
    ### Filter the eeg data
    for t in range(10):
        data1, timestamps1 = receiver.get_window(STREAM_NAME)
        data1 = np.delete(data1, np.s_[9:], axis=1)
        data1 = np.delete(data1, 0, axis=1)
        df = pd.DataFrame(data1, columns=['EEG_1', 'EEG_2', 'EEG_3',
                                          'EEG_4', 'EEG_5', 'EEG_6', 
                                          'EEG_7', 'EEG_8'])
        eeg_keys = ['EEG_' + str(i) for i in range(1, 9)]
        filt_eeg = df.copy()
        filt_eeg[eeg_keys] = filt_eeg[eeg_keys].apply(filtereeg, raw=True)
        print(filt_eeg)
        time.sleep(2)
    
    
    ### View the stream in real-time (optional)
    # viewer = StreamViewer(stream_name=STREAM_NAME)
    # viewer.start()
    
    trigger.close()
    recorder.stop()
    
    # Play data from a file (optional)
    # # {fname}-[stream_name]-raw.pcl
    # filename = f'test{idx}-{STREAM_NAME}-raw.fif'
    # player = StreamPlayer(stream_name=STREAM_NAME, fif_file=filename)
    # player.start()