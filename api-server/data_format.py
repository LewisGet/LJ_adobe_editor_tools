from pydub import AudioSegment
import numpy as np
import os
import config

def load(path, start):
    # start is millisecond
    audio = AudioSegment.from_file(path)

    audio = audio.set_frame_rate(config.sampling_rate)
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2)

    # cut one second audio
    audio = audio[start: start + 1000]

    audio_array = audio.get_array_of_samples()

    return world_decompose(np.array(audio_array), config.sampling_rate)


def world_decompose(wav, fs, frame_period = 5.0):

    # Decompose speech signal into f0, spectral envelope and aperiodicity using WORLD
    wav = wav.astype(np.float64)
    f0, timeaxis = pw.harvest(wav, fs, frame_period = frame_period, f0_floor = 71.0, f0_ceil = 800.0)
    sp = pw.cheaptrick(wav, f0, timeaxis, fs)
    ap = pw.d4c(wav, f0, timeaxis, fs)

    return f0, timeaxis, sp, ap

def world_encode_spectral_envelop(sp, fs, dim = 24):

    # Get Mel-cepstral coefficients (MCEPs)

    #sp = sp.astype(np.float64)
    coded_sp = pw.code_spectral_envelope(sp, fs, dim)

    return coded_sp

def logf0_statistics(f0s):

    log_f0s_concatenated = np.ma.log(np.concatenate(f0s))
    log_f0s_mean = log_f0s_concatenated.mean()
    log_f0s_std = log_f0s_concatenated.std()

    return log_f0s_mean, log_f0s_std

def coded_sps_normalization_fit_transoform(coded_sps):

    coded_sps_concatenated = np.concatenate(coded_sps, axis = 1)
    coded_sps_mean = np.mean(coded_sps_concatenated, axis = 1, keepdims = True)
    coded_sps_std = np.std(coded_sps_concatenated, axis = 1, keepdims = True)

    coded_sps_normalized = list()
    for coded_sp in coded_sps:
        coded_sps_normalized.append((coded_sp - coded_sps_mean) / coded_sps_std)
    
    return coded_sps_normalized, coded_sps_mean, coded_sps_std
