import sys
import copy
import math

import numpy as np

"""This file contains various gradient optimisers"""


# class for simple gradient descent
class SimpleGradientDescent:
    def __init__(self, eta, layers):
        # learning rate
        self.eta = eta
        # historical loss, will be required for rate annealing
        self.hist_loss = sys.float_info.max
        # number of layers
        self.layers = layers

    # function for gradient descending
    def descent(self, network, gradient):
        for i in range(self.layers):
            network[i]['weight'] -= self.eta * gradient[i]['weight']
            network[i]['bias'] -= self.eta * gradient[i]['bias']

    # function for learning rate annealing
    def anneal(self, loss):
        # if loss increases decrease learning rate
        if loss > self.hist_loss:
            self.eta = self.eta / 2.0
        self.hist_loss = loss


# class for Momentum gradient descent
class MomentumGradientDescent:
    def __init__(self, eta, layers, gamma):
        # learning rate
        self.eta = eta
        self.gamma = gamma
        # historical loss, will be required for rate annealing
        self.hist_loss = sys.float_info.max
        # number of layers
        self.layers = layers
        # number of calls
        self.calls = 1
        # historical momentum
        self.momentum = None

    # function for gradient descending
    def descent(self, network, gradient):
        gamma = min(1 - 2 ** (-1 - math.log((self.calls / 250.0) + 1, 2)), self.gamma)

        if self.momentum is None:
            # copy the structure
            self.momentum = copy.deepcopy(gradient)
            # initialize momentum
            for i in range(self.layers):
                self.momentum[i]['weight'] = self.eta * gradient[i]['weight']
                self.momentum[i]['bias'] = self.eta * gradient[i]['bias']
        else:
            # update momentum
            for i in range(self.layers):
                self.momentum[i]['weight'] = gamma * self.momentum[i]['weight'] + self.eta * gradient[i]['weight']
                self.momentum[i]['bias'] = gamma * self.momentum[i]['bias'] + self.eta * gradient[i]['bias']
        # the descent
        for i in range(self.layers):
            network[i]['weight'] -= self.momentum[i]['weight']
            network[i]['bias'] -= self.momentum[i]['bias']

        self.calls += 1

    # function for learning rate annealing
    def anneal(self, loss):
        # if loss increases decrease learning rate
        if loss > self.hist_loss:
            self.eta = self.eta / 2.0
        self.hist_loss = loss


# class for NAG
class NAG:
    def __init__(self, eta, layers, gamma):
        # learning rate
        self.eta = eta
        self.gamma = gamma
        # historical loss, will be required for rate annealing
        self.hist_loss = sys.float_info.max
        # number of layers
        self.layers = layers
        # number of calls
        self.calls = 1
        # historical momentum
        self.momentum = None

    # function for lookahead. Call this before forward propagation.
    def lookahead(self, network):
        # case when no momentum has been generated yet.
        if self.momentum is None:
            pass
        else:
            # update the gradient using momentum
            for i in range(self.layers):
                network[i]['weight'] -=  self.momentum[i]['weight']
                network[i]['bias'] -= self.momentum[i]['bias']

    # function for gradient descending
    def descent(self, network, gradient):

        # the descent
        for i in range(self.layers):
            network[i]['weight'] -= self.eta * gradient[i]['weight']
            network[i]['bias'] -= self.eta * gradient[i]['bias']

        # from the lecture
        gamma = min(1 - 2 ** (-1 - math.log((self.calls / 250.0) + 1, 2)), self.gamma)

        # generate momentum for the next time step next

        if self.momentum is None:
            # copy the structure
            self.momentum = copy.deepcopy(gradient)
            # initialize momentum
            for i in range(self.layers):
                self.momentum[i]['weight'] = self.eta * gradient[i]['weight']
                self.momentum[i]['bias'] = self.eta* gradient[i]['bias']
        else:
            # update momentum
            for i in range(self.layers):
                self.momentum[i]['weight'] = gamma * self.momentum[i]['weight'] + self.eta * gradient[i][
                    'weight']
                self.momentum[i]['bias'] = gamma * self.momentum[i]['bias'] + self.eta * gradient[i]['bias']

        self.calls += 1

    # function for learning rate annealing
    def anneal(self, loss):
        # if loss increases decrease learning rate
        if loss > self.hist_loss:
            self.eta = self.eta / 2.0
        self.hist_loss = loss


# class for ADAM
class ADAM:
    def __init__(self, eta, layers, beta1=0.9, beta2=0.999, eps=1):
        # learning rate
        self.eta = eta
        self.beta1 = beta1
        self.beta2 = beta2
        # number of layers
        self.layers = layers
        # number of calls
        self.calls = 1
        # momentum
        self.momentum = None
        # second momentum
        self.second_momentum = None
        # epsilon
        self.eps = eps

    # function for gradient descending
    def descent(self, network, gradient):

        if self.momentum is None:
            # copy the structure
            self.momentum = copy.deepcopy(gradient)
            self.second_momentum = copy.deepcopy(gradient)
            # initialize momentums
            for i in range(self.layers):
                # first momentum initialization
                self.momentum[i]['weight'] = (1 - self.beta1) * gradient[i]['weight']
                self.momentum[i]['bias'] = (1 - self.beta1) * gradient[i]['bias']
                # second momentum initialization
                self.second_momentum[i]['weight'] = (1 - self.beta2) * np.power(gradient[i]['weight'], 2)
                self.second_momentum[i]['bias'] = (1 - self.beta2) * np.power(gradient[i]['bias'], 2)
        else:
            for i in range(self.layers):
                # momentum update
                self.momentum[i]['weight'] = self.beta1 * self.momentum[i]['weight'] + (1 - self.beta1) * gradient[i][
                    'weight']
                self.momentum[i]['bias'] = self.beta1 * self.momentum[i]['bias'] + (1 - self.beta1) * gradient[i]['bias'
                ]
                # rate adjusting parameter update
                self.second_momentum[i]['weight'] = self.beta2 * self.second_momentum[i]['weight'] + (1 - self.beta2) * np.power(gradient[i][
                                                                                                         'weight'], 2)
                self.second_momentum[i]['bias'] = self.beta2 * self.second_momentum[i]['bias'] + (1 - self.beta2) * np.power(gradient[i]['bias'
                                                                                                 ], 2)
        # bias correction
        for i in range(self.layers):
            self.momentum[i]['weight'] = (1 / (1 - (self.beta1 ** self.calls))) * self.momentum[i]['weight']
            self.momentum[i]['bias'] = (1 / (1 - (self.beta1 ** self.calls))) * self.momentum[i]['bias']

            self.second_momentum[i]['weight'] = (1 / (1 - (self.beta2 ** self.calls))) * self.second_momentum[i]['weight']
            self.second_momentum[i]['bias'] = (1 / (1 - (self.beta2 ** self.calls))) * self.second_momentum[i]['bias']

        # the descent
        for i in range(self.layers):
            # temporary variable for calculation
            temp = np.sqrt(self.second_momentum[i]['weight'])
            # add epsilon to square root of temp
            temp_eps = temp + self.eps
            # inverse everything
            temp_inv = 1 / temp_eps
            # perform descent for weight
            network[i]['weight'] = network[i]['weight'] - self.eta * (
                        np.multiply(temp_inv, self.momentum[i]['weight']) + .5 * network[i]['weight'])

            # now we do the same for bias
            # temporary variable for calculation
            temp = np.sqrt(self.second_momentum[i]['bias'])
            # add epsilon to square root of temp
            temp_eps = temp + self.eps
            # inverse everything
            temp_inv = 1 / temp_eps
            # perform descent for weight
            network[i]['bias'] -= self.eta * np.multiply(temp_inv, self.momentum[i]['bias'])

        self.calls += 1