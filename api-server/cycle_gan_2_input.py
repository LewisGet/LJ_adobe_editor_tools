from recorder import Recorder
from pydub import AudioSegment
import tensorflow as tf
from cycle_gan_2.cyclegan_vc2 import CycleGAN2
from cycle_gan_2_speech_tools import *
import numpy as np
import config
import os


cycleGAN2_config = config.cycleGAN2()

src_speaker = cycleGAN2_config.src_speaker
trg_speaker = cycleGAN2_config.trg_speaker

exp_A_dir = os.path.join(config.cycleGAN_2_audio_cache, src_speaker)
exp_B_dir = os.path.join(config.cycleGAN_2_audio_cache, trg_speaker)

sampling_rate = cycleGAN2_config.sampling_rate
num_mcep = cycleGAN2_config.num_mcep
frame_period = cycleGAN2_config.frame_period
n_frames = cycleGAN2_config.n_frames

print('Loading cached data...')
coded_sps_A_norm, coded_sps_A_mean, coded_sps_A_std, log_f0s_mean_A, log_f0s_std_A = load_pickle(
    os.path.join(exp_A_dir, 'cache{}.p'.format(num_mcep)))
coded_sps_B_norm, coded_sps_B_mean, coded_sps_B_std, log_f0s_mean_B, log_f0s_std_B = load_pickle(
    os.path.join(exp_B_dir, 'cache{}.p'.format(num_mcep)))

sess_config = tf.ConfigProto()
sess_config.gpu_options.allow_growth = True

model = CycleGAN2(num_features=num_mcep, batch_size=1, mode='test', sess_config=sess_config)
model.load(config.cycleGAN_2_model_default)

def conversion_with_config(wav, file_name):
    wav = wav_padding(wav=np.array(wav), sr=sampling_rate, frame_period=frame_period, multiple=4)
    f0, timeaxis, sp, ap = world_decompose(wav=wav, fs=sampling_rate, frame_period=frame_period)
    f0_converted = pitch_conversion(f0=f0, mean_log_src=log_f0s_mean_A, std_log_src=log_f0s_std_A,
                                    mean_log_target=log_f0s_mean_B, std_log_target=log_f0s_std_B)
    coded_sp = world_encode_spectral_envelop(sp=sp, fs=sampling_rate, dim=num_mcep)
    coded_sp_transposed = coded_sp.T
    coded_sp_norm = (coded_sp_transposed - coded_sps_A_mean) / coded_sps_A_std
    coded_sp_converted_norm = model.test(inputs=np.array([coded_sp_norm]), direction='A2B')[0]
    if coded_sp_converted_norm.shape[1] > len(f0):
        coded_sp_converted_norm = coded_sp_converted_norm[:, :-1]
    coded_sp_converted = coded_sp_converted_norm * coded_sps_B_std + coded_sps_B_mean
    coded_sp_converted = coded_sp_converted.T
    coded_sp_converted = np.ascontiguousarray(coded_sp_converted)
    decoded_sp_converted = world_decode_spectral_envelop(coded_sp=coded_sp_converted, fs=sampling_rate)
    wav_transformed = world_speech_synthesis(f0=f0_converted, decoded_sp=decoded_sp_converted, ap=ap, fs=sampling_rate,
                                             frame_period=frame_period)
    librosa.output.write_wav(os.path.join(config.vc_2_audio_save_path, file_name), wav_transformed,
                             sampling_rate)

def file_to_input(path, backup = False, start = None, end = None):
    audio = AudioSegment.from_file(path)

    if start is not None and end is not None:
        start = int(start * 1000)
        end = int(end * 1000)

        if start < 0:
            start = 0

        if end > len(audio):
            end = len(audio)

        audio = audio[start:end]

    audio = convert_to_input(audio)

    if backup:
        save_pre_execute(audio, path)

    return audio.get_array_of_samples()

def convert_to_input(audio):
    input_audio = audio.set_frame_rate(cycleGAN2_config.sampling_rate)
    input_audio = input_audio.set_channels(1)
    input_audio = input_audio.set_sample_width(2)

    return input_audio

def save_pre_execute(audio, path):
    name, _ = os.path.splitext(os.path.basename(path))
    path = config.pre_vc_2_audio_save_path

    audio.export("%s.wav" % os.path.join(path, name), format="wav")
