from recorder import Recorder
from pydub import AudioSegment
import config

r = Recorder(input_device_index=config.input_device_index)

audio = r._audio
# todo: add audio input for cycleGAN
