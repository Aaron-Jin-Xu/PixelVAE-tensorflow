
default_config = {
    'img_size': 64,
    'z_dim': 32,
    'lam': 1.0,
    'beta': 1.0,
    'data_dir': '/tmp',
    'save_dir': '/tmp',
    'data_set': 'cifar',
    'save_interval': 5,
    'load_params': False,
    'nr_resnet': 5,
    'nr_filters': 100,
    'nr_logistic_mix': 10,
    'learning_rate': 0.001,
    'lr_decay': 0.999995,
    'batch_size': 16,
    'init_batch_size': 64,
    'dropout_p': 0.5,
    'max_epochs': 1000,
    'nr_gpu': 1,
    'seed': 1,
    'context_conditioning': False,
    'debug': False,
    'nr_final_feature_maps': 32,
}


configs = {}

configs['cifar'] = {
    "img_size": 32,
    'beta': 100.0,
    "data_dir": "/data/ziz/not-backed-up/jxu/cifar",
    "save_dir": "/data/ziz/jxu/models/cifar-test",
    "nr_filters": 100,
    "nr_resnet": 6,
    "data_set": "cifar",
    "batch_size": 8,
    "init_batch_size": 8,
    'learning_rate': 0.0001,
    "save_interval": 10,
    "nr_gpu": 4,
}

configs['pixelvae-celeba64'] = {
    "img_size": 64,
    "z_dim": 256,
    "lam": 0.0,
    'beta': 1000.0,
    "data_dir": "/data/ziz/not-backed-up/jxu/CelebA",
    "save_dir": "/data/ziz/jxu/models/pixelvae-celeba64",
    "nr_filters": 100,
    "nr_resnet": 5,
    "data_set": "celeba64",
    "batch_size": 8,
    "init_batch_size": 8,
    'learning_rate': 1e-5,
    "save_interval": 5,
    'nr_final_feature_maps': 64,
    "nr_gpu": 4,
}

configs['pixelvae-celeba64-deep'] = {
    "img_size": 64,
    "z_dim": 64,
    "lam": 0.0,
    'beta': 1e7,
    "data_dir": "/data/ziz/not-backed-up/jxu/CelebA",
    "save_dir": "/data/ziz/jxu/models/pixelvae-celeba64-deep",
    "nr_filters": 80,
    "nr_resnet": 4,
    "data_set": "celeba64",
    "batch_size": 8,
    "init_batch_size": 8,
    'learning_rate': 2e-5,
    "save_interval": 5,
    'nr_final_feature_maps': 32,
    "nr_gpu": 4,
}

configs['pixelvae-celeba32'] = {
    "img_size": 32,
    "z_dim": 128,
    "lam": 0.0,
    'beta': 500.0,
    "data_dir": "/data/ziz/not-backed-up/jxu/CelebA",
    "save_dir": "/data/ziz/jxu/models/pixelvae-celeba32",
    "nr_filters": 100,
    "nr_resnet": 4,
    "data_set": "celeba32",
    "batch_size": 8,
    "init_batch_size": 8,
    'learning_rate': 0.0001,
    "save_interval": 10,
    'nr_final_feature_maps': 64,
    "nr_gpu": 4,
}



def get_config(config_name):
    config = {}
    for key, value in default_config.items():
        if key in configs[config_name]:
            config[key] = configs[config_name][key]
        else:
            config[key] = value
    return config
