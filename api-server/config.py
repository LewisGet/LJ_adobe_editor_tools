# 服務 ip
host_ip = "127.0.0.1"

# http port
http_port = 8000

name_lists = ['lewis', 'kevin', 'gold', 'else']

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

model_default = './model.ckpt'
