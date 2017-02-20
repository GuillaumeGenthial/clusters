import tensorflow as tf
from model import Model
from utils.tf_utils import xavier_weight_init, conv2d, \
        max_pool_2x2, weight_variable, bias_variable

class Regression(Model):
    def __init__(self, config, input_size):
        super(self.__class__, self).__init__(config)
        self.config.input_size = input_size
        self.build()

    def add_placeholder(self):
        """
        Defines self.x and self.y, tf.placeholders
        """
        self.x = tf.placeholder(tf.float32, shape=[None, self.config.input_size])
        self.y = tf.placeholder(tf.int32, shape=[None, self.config.output_size])

    def add_prediction_op(self):
        """
        Defines self.pred
        """
        W = weight_variable('W', [self.config.input_size, self.config.hidden_size])
        b = bias_variable('b', [self.config.hidden_size])
        self.pred = tf.matmul(self.x, W) + b

    def add_loss_op(self):
        """
        Defines self.loss
        """
        losses = tf.nn.softmax_cross_entropy_with_logits(self.pred, self.y)
        self.loss = tf.reduce_mean(losses)
