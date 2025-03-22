import numpy as np
import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()

w = tf.Variable(0,dtype = tf.float32)
cost = w**2 - 10*w + 25
train = tf.train.GradientDescentOptimizer(0.01).minimize(cost)
init = tf.global_variables_initializer()
session = tf.Session()#这样就开启了一个TensorFlow session。
session.run(init)#来初始化全局变量。
for i in range(1000):
    session.run(train)
print(session.run(w))
