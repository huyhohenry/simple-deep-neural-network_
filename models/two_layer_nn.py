

# Do not use packages that are not in standard distribution of python
import numpy as np

np.random.seed(1024)
from ._base_network import _baseNetwork


class TwoLayerNet(_baseNetwork):
    def __init__(self, input_size=28 * 28, num_classes=10, hidden_size=128):
        super().__init__(input_size, num_classes)

        self.hidden_size = hidden_size
        self._weight_init()

    def _weight_init(self):
        """
        initialize weights of the network
        :return: None; self.weights is filled based on method
        - W1: The weight matrix of the first layer of shape (num_features, hidden_size)
        - b1: The bias term of the first layer of shape (hidden_size,)
        - W2: The weight matrix of the second layer of shape (hidden_size, num_classes)
        - b2: The bias term of the second layer of shape (num_classes,)
        """

        # initialize weights
        self.weights['b1'] = np.zeros(self.hidden_size)
        self.weights['b2'] = np.zeros(self.num_classes)
        np.random.seed(1024)
        self.weights['W1'] = 0.001 * np.random.randn(self.input_size, self.hidden_size)
        np.random.seed(1024)
        self.weights['W2'] = 0.001 * np.random.randn(self.hidden_size, self.num_classes)

        # initialize gradients to zeros
        self.gradients['W1'] = np.zeros((self.input_size, self.hidden_size))
        self.gradients['b1'] = np.zeros(self.hidden_size)
        self.gradients['W2'] = np.zeros((self.hidden_size, self.num_classes))
        self.gradients['b2'] = np.zeros(self.num_classes)

    def forward(self, X, y, mode='train'):
        """
        The forward pass of the two-layer net. The activation function used in between the two layers is sigmoid, which
        is to be implemented in self.,sigmoid.
        The method forward should compute the loss of input batch X and gradients of each weights.
        Further, it should also compute the accuracy of given batch. The loss and
        accuracy are returned by the method and gradients are stored in self.gradients

        :param X: a batch of images (N, input_size)
        :param y: labels of images in the batch (N,)
        :param mode: if mode is training, compute and update gradients;else, just return the loss and accuracy
        :return:
            loss: the loss associated with the batch
            accuracy: the accuracy of the batch
            self.gradients: gradients are not explicitly returned but rather updated in the class member self.gradients
        """
        loss = None
        accuracy = None

        Z1 = np.dot(X, self.weights['W1']) + self.weights['b1']
        y_sig = self.sigmoid(Z1)
        Z2 = np.dot(y_sig, self.weights['W2']) + self.weights['b2']
        y_pred = self.softmax(Z2)
        loss = self.cross_entropy_loss(y_pred, y)
        accuracy = self.compute_accuracy(y_pred, y)

        N = len(y)
        y_pred[range(N), y] -= 1
        y_pred /= N
        self.gradients['W2'] = np.matmul(y_sig.T, y_pred)
        self.gradients['b2'] = np.sum(y_pred, axis=0)
        d2 = np.dot(y_pred, np.transpose(self.weights['W2']))
        gradient_sigmoid = y_sig * (1 - y_sig)
        grad1 = d2 * gradient_sigmoid
        self.gradients['W1'] = np.matmul(X.T, grad1)
        self.gradients['b1'] = np.sum(grad1, axis=0)

        return loss, accuracy
