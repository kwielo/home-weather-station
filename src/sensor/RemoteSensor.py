import abc


class RemoteSensor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                (hasattr(subclass, 'get_outside_temperature') and callable(subclass.get_outside_temperature)) and
                (hasattr(subclass, 'get_air_pollution_pm_10') and callable(subclass.get_air_pollution_pm_10)) and
                (hasattr(subclass, 'get_air_pollution_pm_2_5') and callable(subclass.get_air_pollution_pm_2_5)) and
                (
                        hasattr(subclass, 'get_air_pollution_index_name') and
                        callable(subclass.get_air_pollution_index_name)
                ) and
                (hasattr(subclass, 'get_air_pollution_index') and callable(subclass.get_air_pollution_index))
        )

    @abc.abstractmethod
    def get_outside_temperature(self) -> float:
        pass

    @abc.abstractmethod
    def get_air_pollution_pm_2_5(self) -> float:
        pass

    @abc.abstractmethod
    def get_air_pollution_pm_10(self) -> float:
        pass

    @abc.abstractmethod
    def get_air_pollution_index(self) -> float:
        pass

    @abc.abstractmethod
    def get_air_pollution_index_name(self) -> str:
        pass

