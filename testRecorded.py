import time
from bsl import StreamRecorder, StreamPlayer, StreamReceiver, StreamViewer
from bsl.triggers import SoftwareTrigger
import pylsl
import os

STREAM_NAME = 'Unicorn'


if __name__ == "__main__":
    save_dir = "data"
    idx = 0
    recorder = StreamRecorder(record_dir=os.path.join(os.getcwd(), 'data'),
                            fname = f'test{idx}',
                            stream_name = STREAM_NAME,
                            verbose = True)
    recorder.start()
    
    print(recorder)
    trigger = SoftwareTrigger(recorder)
    
    trigger.signal(1)
    
    receiver = StreamReceiver(bufsize=2, winsize=1, stream_name=STREAM_NAME)
    time.sleep(2)  # wait 2 seconds to fill LSL inlet.
    receiver.acquire()
    data1, timestamps1 = receiver.get_window(STREAM_NAME)
    
    
    
    # receiver = StreamReceiver(bufsize=1, winsize=1, stream_name=STREAM_NAME)
    # # time.sleep(2)  # wait 2 seconds to fill LSL inlet.
    # receiver.acquire()
    
    trigger.close()
    recorder.stop()
    
    # # {fname}-[stream_name]-raw.pcl
    # filename = f'test{idx}-{STREAM_NAME}-raw.fif'
    # player = StreamPlayer(stream_name=STREAM_NAME, fif_file=filename)
    # player.start()
        
    
    

