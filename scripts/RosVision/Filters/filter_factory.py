import importlib
import os
import pkgutil
from filter import Filter


class FilterFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_filter(name, filter_type, params={}):
        pkgpath = os.path.dirname(os.path.realpath(__file__))
        for _, module, _ in pkgutil.iter_modules([pkgpath]):
            if module.lower() == filter_type.lower():
                i = importlib.import_module("RosVision.Filters.%s.filter" % module)
                if hasattr(i, "__dict__"):
                    for n, c in i.__dict__.items():
                        print n, c
                        try:
                            if issubclass(c, Filter):
                                return c(name, params)
                        except:
                            pass

    @staticmethod
    def list_filters():
        return [name for name in os.listdir(os.path.dirname(__file__)) if os.path.isdir(os.path.join(os.path.dirname(__file__), name))]
