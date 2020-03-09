import configparser
from generate_benchmarking_sequences import generate_benchmarking_sequences
from train_momma_dragonn import train_momma_dragonn

cfg = configparser.ConfigParser()
cfg.read('config.properties')

generate_benchmarking_sequences(cfg)
train_momma_dragonn(cfg)



