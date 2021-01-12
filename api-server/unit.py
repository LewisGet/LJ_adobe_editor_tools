from pydub import AudioSegment
import numpy as np
import config
import time
import os


cycleGAN2_config = config.cycleGAN2()


def save_clip_research(path, start, end, clip_type):
    audio = get_clip_from_file(path, start, end)

    org_name = get_file_name(path)
    tmp_name = filename_timestamp(org_name)
    tmp_16k_name = filename_timestamp(org_name + "-16k")

    save_path = config.lewis_org_data_path
    save_16k_path = config.lewis_zip_16k_data_path

    if clip_type == "kevin":
        save_path = config.kevin_org_data_path
        save_16k_path = config.kevin_zip_16k_data_path

    if clip_type == "gold":
        save_path = config.gold_org_data_path
        save_16k_path = config.gold_zip_16k_data_path

    p1 = save_audio(audio, save_path, tmp_name)
    p2 = save_audio(convert_to_input(audio), save_16k_path, tmp_16k_name)

    return p1, p2


def get_clip_from_file(path, start, end):
    audio = AudioSegment.from_file(path)
    start = int(start * 1000)
    end = int(end * 1000)

    if start < 0:
        start = 0

    if end > len(audio):
        end = len(audio)

    audio = audio[start:end]

    return audio


def save_audio(audio, path, rename = None):
    name = os.path.basename(path)
    name, _ = os.path.splitext(os.path.basename(name))

    if rename is not None:
        name = rename

    path = "%s.wav" % os.path.sep.join([path, name])

    audio.export(path, format="wav")

    return path


def get_file_name(path):
    name, _ = os.path.splitext(os.path.basename(path))

    return name


def filename_timestamp(org_name = None, wav = False):
    timestamp = str(time.time())

    name = timestamp

    if org_name is not None:
        name = name + "-" + org_name

    if wav:
        name = name + ".wav"

    return str(time.time()) + "-" + org_name + ".wav"


def convert_to_input(audio):
    input_audio = audio.set_frame_rate(cycleGAN2_config.sampling_rate)
    input_audio = input_audio.set_channels(1)
    input_audio = input_audio.set_sample_width(2)

    return input_audio
