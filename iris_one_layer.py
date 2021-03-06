import tensorflow as tf
import numpy as np
from numpy import random

import matplotlib.pyplot as plt


# Translate a list of labels into an array of 0's and one 1.
# i.e.: 4 -> [0,0,0,0,1,0,0,0,0,0] 
def one_hot(x, n):
    if type(x) == list:
        x = np.array(x)
    x = x.flatten()
    o_h = np.zeros((len(x), n))
    o_h[np.arange(len(x)), x] = 1
    return o_h


data = np.genfromtxt('iris.data', delimiter=",")
np.random.shuffle(data)
x_data = data[:, 0:4].astype('f4')
y_data = one_hot(data[:, 4].astype(int), 3)

print y_data

print "\nSome samples..."
for i in range(20):
    print x_data[i], " -> ", y_data[i]
print

x = tf.placeholder("float", [None, 4])
y_ = tf.placeholder("float", [None, 3])

"""parte que nos dan
W = tf.Variable(np.float32(np.random.rand(4, 3))*0.1)
b = tf.Variable(np.float32(np.random.rand(3))*0.1)

y = tf.nn.softmax((tf.sigmoid(tf.matmul(x, W) + b)))
parte que nos dan"""

neuronas = 6


peso_capa_interna = tf.Variable(np.float32(random.rand(4, neuronas)) * 0.1)
bias_capa_interna = tf.Variable(np.float32(random.rand(neuronas)) * 0.1)

peso_capa_externa = tf.Variable(np.float32(random.rand(neuronas, 3)) * 0.1)
bias_capa_externa = tf.Variable(np.float32(random.rand(3)) * 0.1)

salida_capa_interna = tf.sigmoid(tf.matmul(x, peso_capa_interna) + bias_capa_interna)
y = tf.nn.softmax(tf.matmul(salida_capa_interna, peso_capa_externa) + bias_capa_externa)


cross_entropy = tf.reduce_sum(tf.square(y_ - y))
# cross_entropy = -tf.reduce_sum(y_*tf.log(y))

train = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

print "----------------------"
print "   Start training...  "
print "----------------------"

batch_size = 20


y_axis = []
error = 0

for step in xrange(1000):
    for jj in xrange(len(x_data) / batch_size):

        batch_xs = x_data[jj*batch_size : jj*batch_size+batch_size]
        batch_ys = y_data[jj*batch_size : jj*batch_size+batch_size]

        sess.run(train, feed_dict={x: batch_xs, y_: batch_ys})

        if jj == 0:
            error = sess.run(cross_entropy, feed_dict={x: batch_xs, y_: batch_ys})
            y_axis.append(error)

        if step % 50 == 0:
            error = sess.run(cross_entropy, feed_dict={x: batch_xs, y_: batch_ys})
            print "Iteration #:", step, "Error: ", error
            result = sess.run(y, feed_dict={x: batch_xs})
            for b, r in zip(batch_ys, result):
                print b, "-->", r
            print "----------------------------------------------------------------------------------"




x_axis = xrange(len(y_axis))

plt.plot(x_axis, y_axis)
plt.grid(True)
plt.title('NN with ' + str(neuronas) + ' neurons in layer1')
plt.xlabel('Iteration')
plt.ylabel('Error')
plt.show()
