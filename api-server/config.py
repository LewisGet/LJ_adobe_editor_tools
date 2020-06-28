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

classification_model_default = './classification.ckpt'
cycleGAN_model_default = './cycleGAN.ckpt'

input_device_index = 1
org_audio_save_path = './resource/org'
vc_audio_save_path = './resource/vc'

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
