import numpy as np
from core.utils.features_utils import LayerExtractor

# general
exp_name = "plots_2k"
config_file = "config.py"
exp_mode = "test"

# data
data_path = "data/ntuple_v3_2000k.root"
data_verbosity = 2
max_events = 100
export_data_path = "data/ntuple_v3_cnn"
tree_name = "SimpleJet"
batch_size = 20
dev_size = 0.1
test_size = 0.2
max_eta = 0.5
min_energy = 20
modes = ["e", "vol"]
featurized = True

# features
tops = 2
feature_mode = 3
output_size = 3
output_sizes = range(3, 7)
layer_extractors = dict()
for l in range(24):
    layer_extractors[l] = LayerExtractor(l, 1.5, 0.1, 1.5, 0.1)

# model
output_path = None
dropout = 1
lr = 0.001
reg = 0.01
n_epochs = 10
reg_values = np.logspace(-6,0.1,20)
# hidden_sizes = [20, 40, 60, 60, 40, 20, 10]
hidden_sizes = [100, 20]

