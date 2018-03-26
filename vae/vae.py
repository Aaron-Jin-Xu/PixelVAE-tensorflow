import numpy as np
import os
import tensorflow as tf
from tensorflow.contrib.framework.python.ops import arg_scope


kernel_initializer = None
nonlinearity = tf.nn.elu

def generative_network(z, z_dim, img_size=64, output_feature_maps=False, nr_final_feature_maps=32):
    assert img_size in [32, 64, 128, 256], "only support values in [32, 64, 128, 256]"
    kernel_initializer = None
    with tf.variable_scope("generative_network"):
        net = tf.reshape(z, [-1, 1, 1, z_dim])
        net = tf.layers.conv2d_transpose(net, 2**4*nr_final_feature_maps, 4, strides=1, padding='VALID', kernel_initializer=kernel_initializer)
        net = tf.layers.batch_normalization(net)
        net = nonlinearity(net)
        for i in range(np.rint(np.log2(img_size)).astype(np.int32)-2):
            net = tf.layers.conv2d_transpose(net, 2**3*nr_final_feature_maps, 5, strides=2, padding='SAME', kernel_initializer=kernel_initializer)
            net = tf.layers.batch_normalization(net)
            net = nonlinearity(net)
        if output_feature_maps:
            return net
        net = tf.layers.conv2d_transpose(net, 3, 1, strides=1, padding='SAME', kernel_initializer=kernel_initializer)
        net = tf.nn.sigmoid(net)

    return net


def inference_network(x, z_dim, img_size=64, nr_final_feature_maps=32):
    assert img_size in [32, 64, 128, 256], "only support values in [32, 64, 128, 256]"
    kernel_initializer = None
    with tf.variable_scope("inference_network"):
        net = tf.reshape(x, [-1, img_size, img_size, 3]) # 64x64
        for i in range(np.rint(np.log2(img_size)).astype(np.int32)-2):
            net = tf.layers.conv2d(net, nr_final_feature_maps, 5, strides=2, padding='SAME', kernel_initializer=kernel_initializer)
            net = tf.layers.batch_normalization(net)
            net = nonlinearity(net)
        net = tf.layers.conv2d(net, 2**4*nr_final_feature_maps, 4, strides=1, padding='VALID', kernel_initializer=kernel_initializer)
        net = tf.layers.batch_normalization(net)
        net = nonlinearity(net) # 1x1
        net = tf.reshape(net, [-1, 2**4*nr_final_feature_maps])
        net = tf.layers.dense(net, z_dim * 2, activation=None, kernel_initializer=kernel_initializer)
        loc = net[:, :z_dim]
        log_var = net[:, z_dim:]
    return loc, log_var


def sample_z(loc, log_var, z_dim, seed=None):
    with tf.variable_scope("sample_z"):
        scale = tf.sqrt(tf.exp(log_var))
        dist = tf.distributions.Normal(loc=0., scale=1.)
        z = dist.sample(sample_shape=(args.batch_size, z_dim), seed=None)
        z = loc + tf.multiply(z, scale)
        return z

def vae_model(x, z_dim, img_size=64, output_feature_maps=False, nr_final_feature_maps=32, seed=None):
    with tf.variable_scope("vae"):
        loc, log_var = inference_network(x, z_dim)
        z = sample_z(loc, log_var, z_dim, seed=seed)
        x_hat = generative_network(z, z_dim)
        return loc, log_var, z, x_hat
