import abc

class IFuenteDeDatos(abc.ABC):
    @abc.abstractmethod
    def getData(self):
        """
        Obtiene mediciones desde un servidor
        """
        pass