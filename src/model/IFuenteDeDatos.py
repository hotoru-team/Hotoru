import abc

class IFuenteDeDatos(abc.ABC):
    @abc.abstractmethod
    def getData(self):
        pass