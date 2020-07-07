from recorder import Recorder
from pydub import AudioSegment
from cycle_gan import CycleGAN
from cycle_gan_preprocess import *
import numpy as np
import config
import wave
import os


cycleGAN_config = config.cycleGAN()

num_features = 24
sampling_rate = 16000
frame_period = 5.0

model_dir = os.path.dirname(config.cycleGAN_model_default)
model_name = os.path.basename(config.cycleGAN_model_default)

model = CycleGAN(num_features = num_features, mode = 'test')

model.load(filepath = config.cycleGAN_model_default)

mcep_normalization_params = np.load(os.path.join(model_dir, 'mcep_normalization.npz'))
mcep_mean_A = mcep_normalization_params['mean_A']
mcep_std_A = mcep_normalization_params['std_A']
mcep_mean_B = mcep_normalization_params['mean_B']
mcep_std_B = mcep_normalization_params['std_B']

logf0s_normalization_params = np.load(os.path.join(model_dir, 'logf0s_normalization.npz'))
logf0s_mean_A = logf0s_normalization_params['mean_A']
logf0s_std_A = logf0s_normalization_params['std_A']
logf0s_mean_B = logf0s_normalization_params['mean_B']
logf0s_std_B = logf0s_normalization_params['std_B']


def file_to_input(path):
    audio = AudioSegment.from_file(path)

    audio = convert_to_input(audio)

    return audio.get_array_of_samples()

def convert_to_input(audio):
    input_audio = audio.set_frame_rate(cycleGAN_config.sampling_rate)
    input_audio = input_audio.set_channels(1)
    input_audio = input_audio.set_sample_width(2)

    return input_audio

def conversion(wav, model_dir, model_name, conversion_direction, output_dir, save_name):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    wav = wav_padding(wav = np.array(wav), sr = sampling_rate, frame_period = frame_period, multiple = 4)
    f0, timeaxis, sp, ap = world_decompose(wav = wav, fs = sampling_rate, frame_period = frame_period)
    coded_sp = world_encode_spectral_envelop(sp = sp, fs = sampling_rate, dim = num_features)
    coded_sp_transposed = coded_sp.T

    if conversion_direction == 'A2B':
        f0_converted = pitch_conversion(f0 = f0, mean_log_src = logf0s_mean_A, std_log_src = logf0s_std_A, mean_log_target = logf0s_mean_B, std_log_target = logf0s_std_B)
        #f0_converted = f0
        coded_sp_norm = (coded_sp_transposed - mcep_mean_A) / mcep_std_A
        coded_sp_converted_norm = model.test(inputs = np.array([coded_sp_norm]), direction = conversion_direction)[0]
        coded_sp_converted = coded_sp_converted_norm * mcep_std_B + mcep_mean_B
    else:
        f0_converted = pitch_conversion(f0 = f0, mean_log_src = logf0s_mean_B, std_log_src = logf0s_std_B, mean_log_target = logf0s_mean_A, std_log_target = logf0s_std_A)
        #f0_converted = f0
        coded_sp_norm = (coded_sp_transposed - mcep_mean_B) / mcep_std_B
        coded_sp_converted_norm = model.test(inputs = np.array([coded_sp_norm]), direction = conversion_direction)[0]
        coded_sp_converted = coded_sp_converted_norm * mcep_std_A + mcep_mean_A

    coded_sp_converted = coded_sp_converted.T
    coded_sp_converted = np.ascontiguousarray(coded_sp_converted)
    decoded_sp_converted = world_decode_spectral_envelop(coded_sp = coded_sp_converted, fs = sampling_rate)
    wav_transformed = world_speech_synthesis(f0 = f0_converted, decoded_sp = decoded_sp_converted, ap = ap, fs = sampling_rate, frame_period = frame_period)
    librosa.output.write_wav(os.path.join(output_dir, os.path.basename(save_name)), wav_transformed, sampling_rate)

def conversion_with_config(wav, save_name):

    model_dir = os.path.dirname(config.cycleGAN_model_default)
    model_name = os.path.basename(config.cycleGAN_model_default)
    conversion_direction = config.vc_conversion_direction
    output_dir = config.vc_audio_save_path

    conversion(wav, model_dir = model_dir, model_name = model_name, conversion_direction = conversion_direction, output_dir = output_dir, save_name = save_name)
