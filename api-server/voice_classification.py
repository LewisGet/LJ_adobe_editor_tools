import numpy as np
import tensorflow as tf
import config

input_X = tf.placeholder(tf.float32, [None, 24 * 33])
input_Y = tf.placeholder(tf.float32, [None, labels])

layer_size_1 = 48
layer_size_2 = 24
layer_size_3 = labels

weight_1 = tf.Variable(tf.truncated_normal([24 * 33, layer_size_1]))
weight_2 = tf.Variable(tf.truncated_normal([layer_size_1, layer_size_2]))
weight_3 = tf.Variable(tf.truncated_normal([layer_size_2, layer_size_3]))

biases_1 = tf.Variable(tf.truncated_normal([layer_size_1]))
biases_2 = tf.Variable(tf.truncated_normal([layer_size_2]))
biases_3 = tf.Variable(tf.truncated_normal([layer_size_3]))

layer_1 = tf.add(tf.matmul(input_X, weight_1), biases_1)
layer_1 = tf.nn.sigmoid(layer_1)

layer_2 = tf.add(tf.matmul(layer_1, weight_2), biases_2)
layer_2 = tf.nn.sigmoid(layer_2)

layer_3 = tf.add(tf.matmul(layer_2, weight_3), biases_3)
layer_3 = tf.nn.sigmoid(layer_3)

_f = layer_3
f = input_Y

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=_f, labels=f))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

saver = tf.train.Saver()
saver.restore(sess, config.model_default)
