import json

import numpy as np
from numpy import ndarray


class InputVector:
    def __init__(self, x: float, y: float, rot: float, speed: float, out_of_track: bool, sensors: list[float]):
        self.sensors = sensors

        if len(self.sensors) != 5:
            raise ValueError('Incorrect number of sensors')

    def into_vector(self) -> list[float]:
        return [*self.sensors]


class CarNeuralNetwork:
    INPUTS_SIZE = 5
    H1_SIZE = 10
    H2_SIZE = 7
    OUTPUTS_SIZE = 2
    
    def __init__(self):
        # 5 inputs, 10 hidden neurons in 1st layer, 7 hidden neruons in 2nd layer, 2 outputs
        self.weights = np.random.normal(size=(self.INPUTS_SIZE + 1, self.H1_SIZE))
        self.weights2 = np.random.normal(size=(self.H1_SIZE + 1, self.H2_SIZE))
        self.weights3 = np.random.normal(size=(self.H2_SIZE + 1, self.OUTPUTS_SIZE))

    def activate(self, inputs: InputVector) -> list[float]:
        def sigmoid(x: np.ndarray) -> np.ndarray:
            return 1 / (1 + np.exp(-x))

        inputs = np.array(inputs.into_vector() + [1.0])

        layer1 = np.dot(inputs.T, self.weights)
        layer1 = np.concatenate((sigmoid(layer1), [1.0]))

        layer2 = np.dot(layer1.T, self.weights2)
        layer2 = np.concatenate((sigmoid(layer2), [1.0]))

        layer3 = np.dot(layer2.T, self.weights3)
        layer3 = sigmoid(layer3)

        return list(layer3)

    def mutate(self, mutation_rate: float, mutation_amount: float):
        def mutate(x: float) -> float:
            if np.random.rand() < mutation_rate:
                return x * (1 + np.random.normal(0, mutation_amount))
            return x

        self.weights = np.array([mutate(x) for x in self.weights.flatten()]).reshape(self.weights.shape)
        self.weights2 = np.array([mutate(x) for x in self.weights2.flatten()]).reshape(self.weights2.shape)
        self.weights3 = np.array([mutate(x) for x in self.weights3.flatten()]).reshape(self.weights3.shape)

    def __str__(self) -> str:
        return f'{json.dumps(self.weights.tolist())}@{json.dumps(self.weights2.tolist())}@{json.dumps(self.weights3.tolist())}'
    
    def from_string(self, string: str):
        weights, weights2, weights3 = string.split('@')
        self.weights = np.array(json.loads(weights)).reshape((self.INPUTS_SIZE + 1, self.H1_SIZE))
        self.weights2 = np.array(json.loads(weights2)).reshape((self.H1_SIZE + 1, self.H2_SIZE))
        self.weights3 = np.array(json.loads(weights3)).reshape((self.H2_SIZE + 1, self.OUTPUTS_SIZE))
