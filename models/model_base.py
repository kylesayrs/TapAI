from typing import Optional

from abc import ABC, abstractmethod

class ModelBase(ABC):
    @abstractmethod
    def load_weights(self, weights_path: Optional[str] = None):
        raise NotImplementedError()

    @abstractmethod
    def save_weights(self, weights_path: Optional[str] = None):
        raise NotImplementedError()

    @abstractmethod
    def train(self, x_train, y_train):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, text: str):
        raise NotImplementedError()
