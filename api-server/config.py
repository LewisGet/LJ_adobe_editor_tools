import os

# 服務 ip
host_ip = "127.0.0.1"

# http port
http_port = 8000

name_lists = ['lewis', 'kevin', 'gold', 'else']

input_device_index = 1

sampling_rate = 16000
num_mcep = 24
frame_period = 5.0
n_frames = 32 #org_value 128
lambda_cycle = 10
lambda_identity = 5
learning_rate = 0.05
labels = len(name_lists)

def load_vocab():
    name2id = {char: idx for idx, char in enumerate(name_lists)}
    id2name = {idx: char for idx, char in enumerate(name_lists)}
    
    return name2id, id2name

name2id, id2name = load_vocab()

def p(v):
    return os.path.sep.join(v.split('/'))

classification_model_default = p('./mod/classification.ckpt')
cycleGAN_model_default = p('./mod/vec')
cycleGAN_2_model_default = p('./cycle_gan_2_mod/cyclegan_vc2_two_step_75000.ckpt')
cycleGAN_2_audio_cache = p('./cycle_gan_2_cache')

input_device_index = 1
org_audio_save_path = p('./resource/org')
vc_audio_save_path = p('./resource/vc')
vc_2_audio_save_path = p('./resource/vc2')
pre_vc_2_audio_save_path = p('./resource/pre_vc2_org')
vc_conversion_direction = p('B2A')

# 原始紀錄
lewis_org_data_path = p('./resource/org/lewis')
kevin_org_data_path = p('./resource/org/kevin')
gold_org_data_path = p('./resource/org/gold')

# 壓縮訓練用
lewis_zip_16k_data_path = p('./resource/zip_16k/lewis')
kevin_zip_16k_data_path = p('./resource/zip_16k/kevin')
gold_zip_16k_data_path = p('./resource/zip_16k/gold')

class cycleGAN:
    def __init__(self):
        self.num_epochs = 3000
        self.mini_batch_size_org, mini_batch_size = [20] * 2 # mini_batch_size = 1 is better
        self.generator_learning_rate = 0.0002
        self.generator_learning_rate_decay = self.generator_learning_rate / 200000
        self.discriminator_learning_rate = 0.0001
        self.discriminator_learning_rate_decay = self.discriminator_learning_rate / 200000
        self.sampling_rate = 16000
        self.num_mcep = 24
        self.frame_period = 5.0
        self.n_frames = 32 #org_value 128
        self.lambda_cycle = 10
        self.lambda_identity = 5


class cycleGAN2:
    def __init__(self):
        self.sampling_rate = 16000
        self.num_mcep = 36
        self.frame_period = 5.0
        self.n_frames = 128
        self.src_speaker = 'b'
        self.trg_speaker = 'a'
