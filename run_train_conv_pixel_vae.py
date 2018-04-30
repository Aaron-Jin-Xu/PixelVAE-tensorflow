import os
import sys
import json
import argparse
import time
import numpy as np
import tensorflow as tf
from blocks.helpers import Recorder, visualize_samples, get_nonlinearity, int_shape, get_trainable_variables
from blocks.optimizers import adam_updates
import data.load_data as load_data
from models.conv_pixel_vae import ConvPixelVAE
from masks import RandomRectangleMaskGenerator, RectangleMaskGenerator, CenterMaskGenerator

parser = argparse.ArgumentParser()

cfg_default = {
    "img_size": 64,
    "data_dir": "/data/ziz/not-backed-up/jxu/CelebA",
    "data_set": "celeba64",
    "nonlinearity":"relu",
    "batch_size": 32,
    "learning_rate": 0.0001,
    "lam": 0.0,
    "save_interval": 10,
    "nr_resnet": 5,
    "nr_filters": 100,
    "nr_logistic_mix": 10,
    "sample_range": 3.0,
}


# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 32,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd",
#     "beta": 1e5,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "medium",
#     "masked": False,
# })

# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 32,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_large1",
#     "beta": 1e5,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "large1",
#     "masked": False,
# })

# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 32,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_large1_mask",
#     "beta": 1e5,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "random rec",
#     "batch_size": 64,
#     "network_size": "large1",
#     "masked": True,
# })
#
# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 32,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_tc-dwmmd_medium",
#     "beta": 5,
#     "reg": "tc-dwmmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "medium",
#     "masked": False,
# })

# 01
# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 24,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_medium_01",
#     "beta": 1e5,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "medium",
#     "masked": False,
# })

# 01
# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 24,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd_large_01",
#     "beta": 5e5,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "large",
#     "masked": False,
# })

# # 02
# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 24,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd_large_02",
#     "beta": 1e6,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "large",
#     "masked": False,
# })
#
# # 03
# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 24,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd_large1_03",
#     "beta": 5e5,
#     "reg": "mmd",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "large1",
#     "masked": False,
# })

# cfg = cfg_default
# cfg.update({
#     "img_size": 32,
#     "data_set": "celeba32",
#     "z_dim": 24,
#     "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd-tc",
#     "beta": 5,
#     "reg": "mmd-tc",
#     "use_mode": "train",
#     "mask_type": "full",
#     "batch_size": 64,
#     "network_size": "medium",
#     "masked": False,
# })




cfg = cfg_default
cfg.update({
    "img_size": 32,
    "data_set": "celeba32",
    "z_dim": 24,
    "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd_large1_elu_3",
    "beta": 3e5,
    "reg": "mmd",
    "use_mode": "train",
    "mask_type": "full",
    "batch_size": 64,
    "network_size": "large1",
    "masked": False,
    "nonlinearity": "elu",
})

cfg = cfg_default
cfg.update({
    "img_size": 32,
    "data_set": "celeba32",
    "z_dim": 24,
    "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd_large1_elu_7",
    "beta": 7e5,
    "reg": "mmd",
    "use_mode": "train",
    "mask_type": "full",
    "batch_size": 64,
    "network_size": "large1",
    "masked": False,
    "nonlinearity": "elu",
})


cfg = cfg_default
cfg.update({
    "img_size": 32,
    "data_set": "celeba32",
    "z_dim": 32,
    "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_medium_elu_5",
    "beta": 5e5,
    "reg": "mmd",
    "use_mode": "train",
    "mask_type": "full",
    "batch_size": 64,
    "network_size": "medium",
    "masked": False,
    "nonlinearity": "elu",
    "use_input_masks": False,
})

#################

## MMD (Masking)

cfg = cfg_default
cfg.update({
    "img_size": 32,
    "data_set": "celeba32",
    "z_dim": 32,
    "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_medium_elu_5",
    "beta": 5e5,
    "reg": "mmd",
    "use_mode": "train",
    "mask_type": "full",
    "batch_size": 64,
    "network_size": "medium",
    "masked": False,
    "nonlinearity": "elu",
    "use_input_masks": True,
})

cfg = cfg_default
cfg.update({
    "img_size": 32,
    "data_set": "celeba32",
    "z_dim": 32,
    "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_large1_elu_5",
    "beta": 5e5,
    "reg": "mmd",
    "use_mode": "train",
    "mask_type": "full",
    "batch_size": 64,
    "network_size": "large1",
    "masked": False,
    "nonlinearity": "elu",
    "use_input_masks": True,
})

cfg = cfg_default
cfg.update({
    "img_size": 32,
    "data_set": "celeba32",
    "z_dim": 24,
    "save_dir": "/data/ziz/jxu/models/pvae_celeba32_z24_mmd_large1_elu_5_mask",
    "beta": 5e5,
    "reg": "mmd",
    "use_mode": "train",
    "mask_type": "full",
    "batch_size": 64,
    "network_size": "large1",
    "masked": False,
    "nonlinearity": "elu",
    "use_input_masks": True,
})

## KLD

## TC

## TC-MMD

# -MI --- distribution of means and stds

##################







parser.add_argument('-is', '--img_size', type=int, default=cfg['img_size'], help="size of input image")
# data I/O
parser.add_argument('-dd', '--data_dir', type=str, default=cfg['data_dir'], help='Location for the dataset')
parser.add_argument('-sd', '--save_dir', type=str, default=cfg['save_dir'], help='Location for parameter checkpoints and samples')
parser.add_argument('-ds', '--data_set', type=str, default=cfg['data_set'], help='Can be either cifar|imagenet')
parser.add_argument('-r', '--reg', type=str, default=cfg['reg'], help='regularization type')
parser.add_argument('-si', '--save_interval', type=int, default=cfg['save_interval'], help='Every how many epochs to write checkpoint/samples?')
parser.add_argument('-lp', '--load_params', dest='load_params', action='store_true', help='Restore training from previous model checkpoint?')
parser.add_argument('-bs', '--batch_size', type=int, default=cfg['batch_size'], help='Batch size during training per GPU')
parser.add_argument('-ng', '--nr_gpu', type=int, default=0, help='How many GPUs to distribute the training across?')
parser.add_argument('-g', '--gpus', type=str, default="", help='GPU No.s')
parser.add_argument('-n', '--nonlinearity', type=str, default=cfg['nonlinearity'], help='')
parser.add_argument('-lr', '--learning_rate', type=float, default=cfg['learning_rate'], help='Base learning rate')
parser.add_argument('-b', '--beta', type=float, default=cfg['beta'], help="strength of the KL divergence penalty")
parser.add_argument('-l', '--lam', type=float, default=cfg['lam'], help="")
parser.add_argument('-zd', '--z_dim', type=float, default=cfg['z_dim'], help="")
parser.add_argument('-nr', '--nr_resnet', type=float, default=cfg['nr_resnet'], help="")
parser.add_argument('-nf', '--nr_filters', type=float, default=cfg['nr_filters'], help="")
parser.add_argument('-nlm', '--nr_logistic_mix', type=float, default=cfg['nr_logistic_mix'], help="")
parser.add_argument('-sr', '--sample_range', type=float, default=cfg['sample_range'], help="")
parser.add_argument('-s', '--seed', type=int, default=1, help='Random seed to use')
# new features
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Under debug mode?')
parser.add_argument('-um', '--use_mode', type=str, default=cfg['use_mode'], help='')
parser.add_argument('-mt', '--mask_type', type=str, default=cfg['mask_type'], help='')

args = parser.parse_args()
if args.use_mode == 'test':
    args.debug = True

args.nr_gpu = len(args.gpus.split(","))
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpus
print('input args:\n', json.dumps(vars(args), indent=4, separators=(',',':'))) # pretty print args
if not os.path.exists(args.save_dir):
    os.makedirs(args.save_dir)

tf.set_random_seed(args.seed)
batch_size = args.batch_size * args.nr_gpu
data_set = load_data.CelebA(data_dir=args.data_dir, batch_size=batch_size, img_size=args.img_size)
if args.debug:
    train_data = data_set.train(shuffle=True, limit=batch_size*2)
    eval_data = data_set.train(shuffle=True, limit=batch_size*2)
    test_data = data_set.test(shuffle=False, limit=batch_size*1)
else:
    train_data = data_set.train(shuffle=True, limit=-1)
    eval_data = data_set.train(shuffle=True, limit=batch_size*10)
    test_data = data_set.test(shuffle=False, limit=-1)

# masks
if args.mask_type=="none":
    masks = [None for i in range(args.nr_gpu)]
else:
    masks = [tf.placeholder(tf.float32, shape=(args.batch_size, args.img_size, args.img_size)) for i in range(args.nr_gpu)]
    if args.mask_type=="random rec":
        train_mgen = RandomRectangleMaskGenerator(args.img_size, args.img_size, min_ratio=0.125, max_ratio=1.0)
    elif args.mask_type=="full":
        train_mgen = CenterMaskGenerator(args.img_size, args.img_size, ratio=1.0)
    elif args.mask_type=="center rec":
        train_mgen = CenterMaskGenerator(args.img_size, args.img_size, ratio=0.5)
if "masked" in cfg and cfg['masked']:
    test_mgen = CenterMaskGenerator(args.img_size, args.img_size, ratio=0.5)
else:
    test_mgen = CenterMaskGenerator(args.img_size, args.img_size, ratio=1.)


input_masks = [None for i in range(args.nr_gpu)]
input_mgen = RandomRectangleMaskGenerator(args.img_size, args.img_size, min_ratio=1./16, max_ratio=.75)
input_test_mgen = RectangleMaskGenerator(args.img_size, args.img_size, rec=[8, 31, 18, 1])
if "use_input_masks" in cfg and cfg["use_input_masks"]:
    input_masks = [tf.placeholder(tf.float32, shape=(args.batch_size, args.img_size, args.img_size)) for i in range(args.nr_gpu)]

xs = [tf.placeholder(tf.float32, shape=(args.batch_size, args.img_size, args.img_size, 3)) for i in range(args.nr_gpu)]
x_bars = [tf.placeholder(tf.float32, shape=(args.batch_size, args.img_size, args.img_size, 3)) for i in range(args.nr_gpu)]
is_trainings = [tf.placeholder(tf.bool, shape=()) for i in range(args.nr_gpu)]
dropout_ps = [tf.placeholder(tf.float32, shape=()) for i in range(args.nr_gpu)]

pvaes = [ConvPixelVAE(counters={}) for i in range(args.nr_gpu)]
model_opt = {
    "use_mode": args.use_mode,
    "z_dim": args.z_dim,
    "reg": args.reg,
    "beta": args.beta,
    "lam": args.lam,
    "N": 200000,
    "nonlinearity": get_nonlinearity(args.nonlinearity),
    "bn": True,
    "kernel_initializer": tf.contrib.layers.xavier_initializer(),
    "kernel_regularizer": None,
    "nr_resnet": args.nr_resnet,
    "nr_filters": args.nr_filters,
    "nr_logistic_mix": args.nr_logistic_mix,
    "sample_range": args.sample_range,
    "network_size": cfg['network_size'],
}


model = tf.make_template('model', ConvPixelVAE.build_graph)

for i in range(args.nr_gpu):
    with tf.device('/gpu:%d' % i):
        model(pvaes[i], xs[i], x_bars[i], is_trainings[i], dropout_ps[i], masks=masks[i], input_masks=input_masks[i], **model_opt)

if args.use_mode == 'train':
    if "masked" in cfg and cfg['masked']:
        all_params = get_trainable_variables(["conv_pixel_cnn", "context_encoder"])
    else:
        all_params = get_trainable_variables(["conv_encoder", "conv_decoder", "conv_pixel_cnn"])
    grads = []
    for i in range(args.nr_gpu):
        with tf.device('/gpu:%d' % i):
            grads.append(tf.gradients(pvaes[i].loss, all_params, colocate_gradients_with_ops=True))
    with tf.device('/gpu:0'):
        for i in range(1, args.nr_gpu):
            for j in range(len(grads[0])):
                grads[0][j] += grads[i][j]

        record_dict = {}
        record_dict['total loss'] = tf.add_n([v.loss for v in pvaes]) / args.nr_gpu
        record_dict['recon loss'] = tf.add_n([v.loss_ae for v in pvaes]) / args.nr_gpu
        if args.reg=='tc':
            record_dict['mi reg'] = tf.add_n([v.mi for v in pvaes]) / args.nr_gpu
            record_dict['tc reg'] = tf.add_n([v.tc for v in pvaes]) / args.nr_gpu
            record_dict['dwkld reg'] = tf.add_n([v.dwkld for v in pvaes]) / args.nr_gpu
        elif args.reg=='mmd':
            record_dict['mmd'] = tf.add_n([v.mmd for v in pvaes]) / args.nr_gpu
        elif args.reg=='kld':
            record_dict['kld'] = tf.add_n([v.kld for v in pvaes]) / args.nr_gpu
        elif args.reg=='tc-dwmmd':
            record_dict['tc reg'] = tf.add_n([v.tc for v in pvaes]) / args.nr_gpu
            record_dict['dwmmd'] = tf.add_n([v.dwmmd for v in pvaes]) / args.nr_gpu
        elif args.reg=='mmd-tc':
            record_dict['mmd'] = tf.add_n([v.mmd for v in pvaes]) / args.nr_gpu
            record_dict['tc'] = tf.add_n([v.tc for v in pvaes]) / args.nr_gpu
        else:
            raise Exception("unknown reg type")
        recorder = Recorder(dict=record_dict, config_str=str(json.dumps(vars(args), indent=4, separators=(',',':'))), log_file=args.save_dir+"/log_file")
        train_step = adam_updates(all_params, grads[0], lr=args.learning_rate)



def make_feed_dict(data, is_training=True, dropout_p=0.5, mgen=None):
    if mgen is None:
        mgen = train_mgen
    data = np.cast[np.float32]((data - 127.5) / 127.5)
    ds = np.split(data, args.nr_gpu)
    feed_dict = {is_trainings[i]: is_training for i in range(args.nr_gpu)}
    feed_dict.update({dropout_ps[i]: dropout_p for i in range(args.nr_gpu)})
    feed_dict.update({ xs[i]:ds[i] for i in range(args.nr_gpu) })
    feed_dict.update({ x_bars[i]:ds[i] for i in range(args.nr_gpu) })
    if masks[0] is not None:
        feed_dict.update({masks[i]:mgen.gen(args.batch_size) for i in range(args.nr_gpu)})
    if input_masks[0] is not None:
        feed_dict.update({input_masks[i]:input_mgen.gen(args.batch_size) for i in range(args.nr_gpu)})
    return feed_dict

def sample_from_model(sess, data, fill_region=None, mgen=None):
    if mgen is None:
        mgen = test_mgen
    data = np.cast[np.float32]((data - 127.5) / 127.5)
    ds = np.split(data, args.nr_gpu)
    feed_dict = {is_trainings[i]: False for i in range(args.nr_gpu)}
    feed_dict.update({dropout_ps[i]: 0. for i in range(args.nr_gpu)})
    feed_dict.update({ xs[i]:ds[i] for i in range(args.nr_gpu) })
    if masks[0] is not None:
        feed_dict.update({masks[i]:mgen.gen(args.batch_size) for i in range(args.nr_gpu)})
    if input_masks[0] is not None:
        feed_dict.update({input_masks[i]:input_test_mgen.gen(args.batch_size) for i in range(args.nr_gpu)})

    x_gen = [ds[i].copy() for i in range(args.nr_gpu)]
    #x_gen = [x_gen[i]*np.stack([tm for t in range(3)], axis=-1) for i in range(args.nr_gpu)]
    for yi in range(args.img_size):
        for xi in range(args.img_size):
            if fill_region is None or fill_region[yi, xi]==0:
                feed_dict.update({x_bars[i]:x_gen[i] for i in range(args.nr_gpu)})
                x_hats = sess.run([pvaes[i].x_hat for i in range(args.nr_gpu)], feed_dict=feed_dict)
                for i in range(args.nr_gpu):
                    x_gen[i][:, yi, xi, :] = x_hats[i][:, yi, xi, :]
    return np.concatenate(x_gen, axis=0)

def generate_samples(sess, data, fill_region=None, mgen=None):
    if mgen is None:
        mgen = test_mgen
    data = np.cast[np.float32]((data - 127.5) / 127.5)
    ds = np.split(data, args.nr_gpu)
    feed_dict = {is_trainings[i]:False for i in range(args.nr_gpu)}
    feed_dict.update({dropout_ps[i]: 0. for i in range(args.nr_gpu)})
    feed_dict.update({xs[i]:ds[i] for i in range(args.nr_gpu)})
    if input_masks[0] is not None:
        feed_dict.update({input_masks[i]:input_test_mgen.gen(args.batch_size) for i in range(args.nr_gpu)})
    z_mu = np.concatenate(sess.run([pvaes[i].z_mu for i in range(args.nr_gpu)], feed_dict=feed_dict), axis=0)
    z_log_sigma_sq = np.concatenate(sess.run([pvaes[i].z_log_sigma_sq for i in range(args.nr_gpu)], feed_dict=feed_dict), axis=0)
    z_sigma = np.sqrt(np.exp(z_log_sigma_sq))
    z = np.random.normal(loc=z_mu, scale=z_sigma)
    #z[:, 1] = np.linspace(start=-5., stop=5., num=z.shape[0])
    z = np.split(z, args.nr_gpu)
    feed_dict.update({pvaes[i].z:z[i] for i in range(args.nr_gpu)})

    if masks[0] is not None:
        feed_dict.update({masks[i]:mgen.gen(args.batch_size) for i in range(args.nr_gpu)})


    x_gen = [ds[i].copy() for i in range(args.nr_gpu)]
    #x_gen = [x_gen[i]*np.stack([tm for t in range(3)], axis=-1) for i in range(args.nr_gpu)]

    for yi in range(args.img_size):
        for xi in range(args.img_size):
            if fill_region is None or fill_region[yi, xi]==0:
                print(yi, xi)
                feed_dict.update({x_bars[i]:x_gen[i] for i in range(args.nr_gpu)})
                x_hats = sess.run([pvaes[i].x_hat for i in range(args.nr_gpu)], feed_dict=feed_dict)
                for i in range(args.nr_gpu):
                    x_gen[i][:, yi, xi, :] = x_hats[i][:, yi, xi, :]
    return np.concatenate(x_gen, axis=0)

def latent_traversal(sess, image, traversal_range=[-6, 6], num_traversal_step=13, fill_region=None, mgen=None):
    if mgen is None:
        mgen = test_mgen
    image = np.cast[np.float32]((image - 127.5) / 127.5)
    num_instances = num_traversal_step * args.z_dim
    assert num_instances <= args.nr_gpu * args.batch_size, "cannot feed all the instances into GPUs"
    data = np.stack([image.copy() for i in range(args.nr_gpu * args.batch_size)], axis=0)
    ds = np.split(data, args.nr_gpu)
    feed_dict = {is_trainings[i]:False for i in range(args.nr_gpu)}
    feed_dict.update({dropout_ps[i]: 0. for i in range(args.nr_gpu)})
    feed_dict.update({xs[i]:ds[i] for i in range(args.nr_gpu)})
    if input_masks[0] is not None:
        feed_dict.update({input_masks[i]:input_test_mgen.gen(args.batch_size) for i in range(args.nr_gpu)})
    z_mu = np.concatenate(sess.run([pvaes[i].z_mu for i in range(args.nr_gpu)], feed_dict=feed_dict), axis=0)
    z_log_sigma_sq = np.concatenate(sess.run([pvaes[i].z_log_sigma_sq for i in range(args.nr_gpu)], feed_dict=feed_dict), axis=0)
    z_sigma = np.sqrt(np.exp(z_log_sigma_sq))
    z = z_mu.copy() # np.random.normal(loc=z_mu, scale=z_sigma)
    for i in range(z.shape[0]):
        z[i] = z[0].copy()
    for i in range(args.z_dim):
        z[i*num_traversal_step:(i+1)*num_traversal_step, i] = np.linspace(start=traversal_range[0], stop=traversal_range[1], num=num_traversal_step)
    z = np.split(z, args.nr_gpu)
    feed_dict.update({pvaes[i].z:z[i] for i in range(args.nr_gpu)})

    if masks[0] is not None:
        feed_dict.update({masks[i]:mgen.gen(args.batch_size) for i in range(args.nr_gpu)})


    x_gen = [ds[i].copy() for i in range(args.nr_gpu)]
    #x_gen = [x_gen[i]*np.stack([tm for t in range(3)], axis=-1) for i in range(args.nr_gpu)]
    for yi in range(args.img_size):
        for xi in range(args.img_size):
            if fill_region is None or fill_region[yi, xi]==0:
                print(yi, xi)
                feed_dict.update({x_bars[i]:x_gen[i] for i in range(args.nr_gpu)})
                x_hats = sess.run([pvaes[i].x_hat for i in range(args.nr_gpu)], feed_dict=feed_dict)
                for i in range(args.nr_gpu):
                    x_gen[i][:, yi, xi, :] = x_hats[i][:, yi, xi, :]
    return np.concatenate(x_gen, axis=0)[:num_instances]

initializer = tf.global_variables_initializer()
saver = tf.train.Saver()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:

    sess.run(initializer)

    if args.load_params:
        ckpt_file = args.save_dir + '/params_' + args.data_set + '.ckpt'
        print('restoring parameters from', ckpt_file)
        saver.restore(sess, ckpt_file)

    ## restore part of parameters
    # var_list = get_trainable_variables(["conv_encoder", "conv_decoder", "conv_pixel_cnn"])
    # pretraining_dir = "/data/ziz/jxu/models/pvae_celeba32_z32_mmd_large1"
    # saver1 = tf.train.Saver(var_list=var_list)
    # ckpt_file = pretraining_dir + '/params_' + args.data_set + '.ckpt'
    # print('restoring parameters from', ckpt_file)
    # saver1.restore(sess, ckpt_file)

    # fill_region = CenterMaskGenerator(args.img_size, args.img_size, ratio=0.5).gen(1)[0]
    fill_region = CenterMaskGenerator(args.img_size, args.img_size, ratio=1.0).gen(1)[0]

    max_num_epoch = 200
    for epoch in range(max_num_epoch+1):
        tt = time.time()
        for data in train_data:
            feed_dict = make_feed_dict(data, is_training=True, dropout_p=0.5)
            sess.run(train_step, feed_dict=feed_dict)

        for data in eval_data:
            feed_dict = make_feed_dict(data, is_training=False, dropout_p=0.)
            recorder.evaluate(sess, feed_dict)

        recorder.finish_epoch_and_display(time=time.time()-tt, log=True)

        if epoch % args.save_interval == 0:
            saver.save(sess, args.save_dir + '/params_' + args.data_set + '.ckpt')
            data = next(test_data)
            test_data.reset()
            #data = next(eval_data)
            sample_x = sample_from_model(sess, data, fill_region=fill_region)
            visualize_samples(sample_x, os.path.join(args.save_dir,'%s_vae_sample%d.png' % (args.data_set, epoch)), layout=(4, 4))
            print("------------ saved")
            sys.stdout.flush()
