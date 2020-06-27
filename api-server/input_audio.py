from recorder import Recorder
from pydub import AudioSegment
import numpy as np
import config
import wave


cycleGAN_config = config.cycleGAN()

def convert_to_input(audio):
    input_audio = audio.set_frame_rate(cycleGAN_config.sampling_rate)
    input_audio = input_audio.set_channels(1)
    input_audio = input_audio.set_sample_width(2)

    return input_audio


class basic_recorder(Recorder):

    def start(self):
        self.record_stop = False
        self.cache_wave = []
        self.cache_frames = []

        wave_data = np.empty((self._channels, 0))

        while True:

            frames = self._read_frames()
            data = self._convert_frames(frames)
            wave_data = np.concatenate((wave_data, data), axis=1)

            self.cache_frames.append(frames)

            if self.record_stop == True:
                self.cache_wave = wave_data

                return wave_data

    def end(self):
        self.record_stop = True

    def save(self, path):
        file = wave.open(path, 'wb')
        file.setframerate(self._rate)
        file.setnchannels(self._channels)
        file.setsampwidth(self._sample_size)

        for frame in self.cache_frames:
            file.writeframes(frame)

        file.close()

        return file
