#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 12:24:47 2017

@author: gautham
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('./data/', one_hot=True)


pixels = 784
n_nodes_HL1 = 700
n_nodes_HL2 = 700
n_nodes_HL3 = 700

n_classes = 10
batch_size = 100

x = tf.placeholder('float', [None, pixels])
y = tf.placeholder('float')


def neural_network_model(data, pixels):

    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([pixels, n_nodes_HL1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_HL1]))}

    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_HL1, n_nodes_HL2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_HL2]))}

    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_HL2, n_nodes_HL3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_HL3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_HL3, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}

    # ( input * weights ) + biases

    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

    return output


def train_neural_network(x, pixels):
    prediction = neural_network_model(x, pixels)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    hm_epochs = 10

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_cost = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_cost += c
            print('Epoch', epoch + 1, 'completed of', hm_epochs, 'and epoch loss:', epoch_cost)
        # pred = sess.run(prediction, feed_dict={x: epoch_x[0]})
        saver = tf.train.Saver()
        saver.save(sess, 'predictor')

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:', accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))


train_neural_network(x, pixels)
