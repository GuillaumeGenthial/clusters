from core.utils.features_utils import LayerExtractor

# general
exp_name = "plots_2k"
config_file = "config.py"

# data
data_path = "data/ntuple_v3_2000k.root"
data_verbosity = 2
max_events = 10
export_data_path = "data/ntuple_v3"
load_from_export_data_path = True # speedup x2000
tree_name = "SimpleJet"
batch_size = 20
dev_size = 0.1
test_size = 0.2
max_eta = 0.5
min_energy = 20
modes = ["e", "vol"]

# features
tops = 10
feature_mode = 3
output_size = 3
layer_extractors = dict()
for l in range(24):
    layer_extractors[l] = LayerExtractor(l, 1.5, 0.1, 1.5, 0.1)

# model
output_path = None
dropout = 0.5
lr = 0.001
reg = 0.001
n_epochs = 20
