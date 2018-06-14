import tensorflow as tf
import numpy as np
data_type = tf.bool
X = tf.placeholder(data_type, shape=[1])
Y = tf.distributions.Bernoulli(probs = 0.5, dtype = data_type).sample(1)
Z = tf.logical_and(X, Y)

tf.train.export_meta_graph(filename="myGraph.txt", as_text="true")
tf.train.export_meta_graph(filename="myGraph.meta")


